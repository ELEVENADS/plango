package com.plango.bridge.client;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class PlanAgentResponse {
    @JsonProperty("natural_output")
    private String naturalOutput;
}
