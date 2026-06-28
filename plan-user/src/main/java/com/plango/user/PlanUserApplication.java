package com.plango.user;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.r2dbc.R2dbcAutoConfiguration;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.web.context.annotation.ApplicationScope;

@SpringBootApplication(exclude = { R2dbcAutoConfiguration.class })
@EnableDiscoveryClient
public class PlanUserApplication
{
    public static void main(String[] args) {
        System.out.println("com.plango.user.PlanUserApplication start");
        SpringApplication.run(PlanUserApplication.class, args);
    }
}
