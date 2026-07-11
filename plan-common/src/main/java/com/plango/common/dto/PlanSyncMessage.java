package com.plango.common.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PlanSyncMessage {
    private Long planId;
    private String operation; // CREATE, UPDATE, DELETE
}
