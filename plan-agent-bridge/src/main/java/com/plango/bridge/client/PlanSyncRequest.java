package com.plango.bridge.client;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class PlanSyncRequest {
    @JsonProperty("plan_id")
    private Long planId;
    @JsonProperty("user_id")
    private Long userId;
    private String title;
    private String description;
    @JsonProperty("plan_date")
    private String planDate;
    @JsonProperty("start_time")
    private String startTime;
    @JsonProperty("end_time")
    private String endTime;
    private Integer priority;
    private String status;
    private String tags;
    @JsonProperty("ai_feedback")
    private String aiFeedback;
    @JsonProperty("ai_generated")
    private Boolean aiGenerated;
    private Boolean deleted;
    @JsonProperty("ext_info")
    private Object extInfo;
    @JsonProperty("created_at")
    private String createdAt;
    @JsonProperty("updated_at")
    private String updatedAt;

    public static PlanSyncRequest from(com.plango.bridge.entity.Plan plan) {
        PlanSyncRequest r = new PlanSyncRequest();
        r.planId = plan.getId();
        r.userId = plan.getUserId();
        r.title = plan.getTitle();
        r.description = plan.getDescription();
        r.planDate = plan.getPlanDate() != null ? plan.getPlanDate().toString() : null;
        r.startTime = plan.getStartTime() != null ? plan.getStartTime().toString() : null;
        r.endTime = plan.getEndTime() != null ? plan.getEndTime().toString() : null;
        r.priority = plan.getPriority();
        r.status = plan.getStatus();
        r.tags = plan.getTags();
        r.aiFeedback = plan.getAiFeedback();
        r.aiGenerated = plan.getAiGenerated();
        r.deleted = plan.getDeleted() != null && plan.getDeleted() != 0;
        r.extInfo = plan.getExtInfo();
        r.createdAt = plan.getCreatedAt() != null ? plan.getCreatedAt().toString() : null;
        r.updatedAt = plan.getUpdatedAt() != null ? plan.getUpdatedAt().toString() : null;
        return r;
    }
}
