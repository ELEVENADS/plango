package com.plango.auth;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class PlanAuthApplication {

    public static void main(String[] args) {

        SpringApplication.run(PlanAuthApplication.class, args);
    }
}
