package com.plango.bridge.dto;
import lombok.Data;

@Data
public class PlanGenerateMessage {
    private Long planId;
    private Long userId;
    private String title;
    private String description;
}