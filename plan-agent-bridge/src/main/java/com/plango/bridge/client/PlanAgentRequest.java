package com.plango.bridge.client;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class PlanAgentRequest {
    @JsonProperty("user_id")
    private int userId;
    private ChatMessage[] messages;

    @Data
    public static class ChatMessage {
        private String role;
        private String content;

        public static ChatMessage of(String role, String content) {
            ChatMessage msg = new ChatMessage();
            msg.role = role;
            msg.content = content;
            return msg;
        }
    }
}
