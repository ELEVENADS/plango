# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PlanGoDaily (PGO) is a distributed microservices daily planning assistant powered by LLM. Users create plans; AI generates feedback/suggestions asynchronously; notifications are pushed to the frontend in real time via WebSocket.

## Build & Run

### Infrastructure (Docker Compose)

```bash
docker compose up -d
```

Starts Nacos (8848), MySQL 8.0 (3307), Redis (6379), RabbitMQ (5672 + 15672 management), Elasticsearch (9200), XXL-JOB (8088), Prometheus (9090), Grafana (3000), Zipkin (9411).

### Java Services (Spring Boot 3.2, Java 21, Maven wrapper)

Build everything from root:

```bash
./mvnw clean package -DskipTests
```

Run individual services (each in its own terminal):

```bash
./mvnw -pl plan-gateway spring-boot:run       # port 8080
./mvnw -pl plan-auth spring-boot:run          # port 8081
./mvnw -pl plan-user spring-boot:run          # port 8082
./mvnw -pl plan-task spring-boot:run          # port 8083
./mvnw -pl plan-notification spring-boot:run  # port 8084
./mvnw -pl plan-agent-bridge spring-boot:run  # port 8085
```

All services register with Nacos at `localhost:8848`. The gateway uses `lb://<service-name>` for load-balanced routing and strips the `/api` prefix before forwarding.

### Python Agent (FastAPI + LangGraph)

```bash
cd plan-agent
cp .env.example .env   # fill in LLM API key
pip install -r requirements.txt
python -m app.main     # port 18000, hot-reload in dev
```

### Database Initialization

Execute `db/plango_task/init.sql` against the MySQL container to create the `plango_task` database and `plan` table.

## Architecture

### Module Map

```
plan-gateway (8080)        — Spring Cloud Gateway, routes /api/task/** → plan-task, /ws/** → plan-notification
plan-auth (8081)           — Authentication service (stub)
plan-user (8082)           — User service (stub)
plan-task (8083)           — Core plan CRUD + sends AI generation messages to RabbitMQ
plan-notification (8084)   — Consumes notification messages, pushes via STOMP WebSocket to clients
plan-agent-bridge (8085)   — Consumes plan generation messages, calls Python Agent via HTTP, writes back AI feedback
plan-common                — Shared DTOs: PlanGenerateMessage, NotificationMessage (no main class)
plan-agent (Python, 18000) — FastAPI + LangGraph, receives plan data, returns AI-generated feedback
```

### Message Flow (AI Generation)

1. Client `POST /api/task/plans` → Gateway strips `/api` → `plan-task` controller
2. `PlanServiceImpl.createPlan()` saves to MySQL; if `aiGenerated=true`, publishes `PlanGenerateMessage` to `plan.generate.queue` (RabbitMQ)
3. `PlanGenerateListener` in `plan-agent-bridge` picks up the message, acquires a Redisson distributed lock (`plan.generate.lock`), queries the plan, calls Python Agent (TODO: HTTP call not yet wired), writes `aiFeedback` back to MySQL
4. After updating, it publishes `NotificationMessage` to `plan.notify.queue`
5. `NotifyListener` in `plan-notification` consumes the notification and pushes it via `SimpMessagingTemplate.convertAndSendToUser()` over STOMP WebSocket (`/user/{userId}/queue/notifications`)

### Key Technical Details

- **MyBatis-Plus**: All mappers extend `BaseMapper<T>`; services extend `ServiceImpl<M, T>`. Logical delete is configured via `@TableLogic` on the `deleted` field and `mybatis-plus.global-config.db-config.logic-delete-field: deleted` in YAML.
- **Caching**: `PlanServiceImpl` uses `@Cacheable` / `@CacheEvict` with key `#plan.userId` on Redis.
- **Distributed Lock**: `PlanGenerateListener` uses Redisson's `RLock` with `tryLock(5, 10, SECONDS)` — wait up to 5s, hold max 10s.
- **JSON column**: `Plan.extInfo` is a MySQL JSON column mapped via `JacksonTypeHandler` to `Map<String, Object>`.
- **Entity duplication**: Both `plan-task` and `plan-agent-bridge` have their own `Plan` entity and `PlanMapper` because each module needs its own datasource/MyBatis-Plus configuration. Only `plan-agent-bridge`'s `PlanGenerateListener` writes AI feedback; `plan-task` handles all other CRUD.
- **Gateway routing**: `/api/task/**` → strips `/api`, forwards to `lb://plan-task`. So `/api/task/plans` arrives at `plan-task` as `/plans`. WebSocket at `/ws/**` goes directly to `plan-notification` without stripping.
