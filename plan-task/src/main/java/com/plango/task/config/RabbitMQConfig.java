package com.plango.task.config;

import org.springframework.amqp.core.Queue;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class RabbitMQConfig {
    //定义队列
    public static final String PLAN_GENERATE_QUEUE = "plan.generate.queue";
    public static final String PLAN_SYNC_QUEUE = "plan.sync.queue";
    public static final String KNOWLEDGE_SYNC_QUEUE = "knowledge.sync.queue";

    @Bean
    public Queue planGenerateQueue() {
        return new Queue(PLAN_GENERATE_QUEUE);
    }

    @Bean
    public Queue planSyncQueue() {
        return new Queue(PLAN_SYNC_QUEUE);
    }

    @Bean
    public Queue knowledgeSyncQueue() {
        return new Queue(KNOWLEDGE_SYNC_QUEUE);
    }

    @Bean
    public Jackson2JsonMessageConverter jackson2JsonMessageConverter() {
        return new Jackson2JsonMessageConverter();
    }

}
