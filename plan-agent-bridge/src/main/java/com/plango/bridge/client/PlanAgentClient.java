package com.plango.bridge.client;

import com.plango.bridge.entity.Knowledge;
import com.plango.bridge.entity.Plan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class PlanAgentClient {

    @Autowired
    private WebClient.Builder webClientBuilder;

    private static final String AGENT_BASE = "http://plan-agent/api/v1";

    public String generate(Plan plan) {
        PlanAgentRequest request = new PlanAgentRequest();
        request.setUserId(plan.getUserId().intValue());

        String content = "请帮我生成一个计划：\n标题：" + plan.getTitle() + "\n描述：" + plan.getDescription();
        PlanAgentRequest.ChatMessage msg = PlanAgentRequest.ChatMessage.of("user", content);
        request.setMessages(new PlanAgentRequest.ChatMessage[]{msg});

        PlanAgentResponse response = webClientBuilder.build()
                .post()
                .uri(AGENT_BASE + "/generate")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(PlanAgentResponse.class)
                .block();

        if (response == null || response.getNaturalOutput() == null) {
            return "";
        }
        return response.getNaturalOutput();
    }

    public void syncPlan(Plan plan) {
        PlanSyncRequest body = PlanSyncRequest.from(plan);
        webClientBuilder.build()
                .post()
                .uri(AGENT_BASE + "/rag/plans")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Void.class)
                .block();
    }

    public void deletePlanFromIndex(Long planId) {
        webClientBuilder.build()
                .delete()
                .uri(AGENT_BASE + "/rag/plans/" + planId)
                .retrieve()
                .bodyToMono(Void.class)
                .block();
    }

    public void syncKnowledge(Knowledge knowledge) {
        KnowledgeSyncRequest body = KnowledgeSyncRequest.from(knowledge);
        webClientBuilder.build()
                .post()
                .uri(AGENT_BASE + "/rag/knowledge")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Void.class)
                .block();
    }

    public void deleteKnowledgeFromIndex(String docId) {
        webClientBuilder.build()
                .delete()
                .uri(AGENT_BASE + "/rag/knowledge/" + docId)
                .retrieve()
                .bodyToMono(Void.class)
                .block();
    }
}
