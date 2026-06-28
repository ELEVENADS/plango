package com.plango.notification;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class PlanNotificationApplication {

    public static void main(String[] args) {
        SpringApplication.run(PlanNotificationApplication.class, args);
    }
}
