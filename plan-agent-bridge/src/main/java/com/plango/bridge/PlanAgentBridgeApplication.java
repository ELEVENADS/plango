package com.plango.bridge;

import org.apache.ibatis.annotations.Mapper;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
@MapperScan("com.plango.bridge.mapper")
public class PlanAgentBridgeApplication {

    public static void main(String[] args) {
        SpringApplication.run(PlanAgentBridgeApplication.class, args);
    }
}
