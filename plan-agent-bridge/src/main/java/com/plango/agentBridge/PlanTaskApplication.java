package com.plango.agentBridge;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class PlanTaskApplication {

    public static void main(String[] args) {
        SpringApplication.run(PlanTaskApplication.class, args);
    }
}
