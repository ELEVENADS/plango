package com.plango.common.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PlanGenerateMessage {
    private Long planId;
    private Long userId;
    private String title;
    private String description;
}
