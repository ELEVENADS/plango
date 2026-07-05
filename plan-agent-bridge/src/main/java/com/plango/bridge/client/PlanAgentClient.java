package com.plango.bridge.client;

import com.plango.bridge.entity.Plan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class PlanAgentClient {

    @Autowired
    private WebClient.Builder webClientBuilder;

    public String generate(Plan plan) {
        PlanAgentRequest request = new PlanAgentRequest();
        request.setUserId(plan.getUserId().intValue());

        String content = "请帮我生成一个计划：\n标题：" + plan.getTitle() + "\n描述：" + plan.getDescription();
        PlanAgentRequest.ChatMessage msg = PlanAgentRequest.ChatMessage.of("user", content);
        request.setMessages(new PlanAgentRequest.ChatMessage[]{msg});

        PlanAgentResponse response = webClientBuilder.build()
                .post()
                .uri("http://plan-agent/api/v1/generate")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(PlanAgentResponse.class)
                .block();

        if (response == null || response.getNaturalOutput() == null) {
            return "";
        }
        return response.getNaturalOutput();
    }
}
