package com.plango.task.Service.Impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.plango.task.Service.PlanService;
import com.plango.task.config.RabbitMQConfig;
import com.plango.task.dto.PlanGenerateMessage;
import com.plango.task.entity.Plan;
import com.plango.task.mapper.PlanMapper;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PlanServiceImpl extends ServiceImpl<PlanMapper,Plan> implements PlanService {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Override
    public void createPlanAndSendMessage(Plan plan) {
        save(plan);
        if(Boolean.TRUE.equals(plan.getAiGenerated())){
            PlanGenerateMessage message = new PlanGenerateMessage();
            message.setPlanId(plan.getId());
            message.setUserId(plan.getUserId());
            message.setTitle(plan.getTitle());
            message.setDescription(plan.getDescription());
            rabbitTemplate.convertAndSend(RabbitMQConfig.PLAN_GENERATE_QUEUE, message);
        }
    }
}
