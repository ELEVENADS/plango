package com.plango.bridge.client;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.plango.bridge.entity.Knowledge;
import lombok.Data;

@Data
public class KnowledgeSyncRequest {
    @JsonProperty("doc_id")
    private String docId;
    @JsonProperty("user_id")
    private Long userId;
    @JsonProperty("doc_type")
    private String docType;
    private String title;
    private String content;
    private String tags;
    private String source;
    private Object metadata;
    private Boolean deleted;
    @JsonProperty("created_at")
    private String createdAt;
    @JsonProperty("updated_at")
    private String updatedAt;

    public static KnowledgeSyncRequest from(Knowledge k) {
        KnowledgeSyncRequest r = new KnowledgeSyncRequest();
        r.docId = String.valueOf(k.getId());
        r.userId = k.getUserId();
        r.docType = k.getDocType();
        r.title = k.getTitle();
        r.content = k.getContent();
        r.tags = k.getTags();
        r.source = k.getSource();
        r.metadata = k.getMetadata();
        r.deleted = k.getDeleted() != null && k.getDeleted() != 0;
        r.createdAt = k.getCreatedAt() != null ? k.getCreatedAt().toString() : null;
        r.updatedAt = k.getUpdatedAt() != null ? k.getUpdatedAt().toString() : null;
        return r;
    }
}
