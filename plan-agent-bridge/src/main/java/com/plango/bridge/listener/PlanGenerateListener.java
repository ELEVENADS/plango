package com.plango.bridge.listener;

import com.plango.bridge.entity.Plan;
import com.plango.bridge.mapper.PlanMapper;
import com.plango.bridge.dto.PlanGenerateMessage;
import com.rabbitmq.client.Channel;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class PlanGenerateListener {

    @Autowired
    private PlanMapper planMapper;

    @RabbitListener(queues = "plan.generate.queue")
    public void handleGenerate(PlanGenerateMessage message, Channel channel, @Header(AmqpHeaders.DELIVERY_TAG) long tag) throws IOException {
        System.out.println("收到 AI 生成请求：planId=" + message.getPlanId());
        try {
            Plan plan = planMapper.selectById(message.getPlanId());
            if (plan == null) {
                System.err.println("计划不存在");
                channel.basicAck(tag, false);
                return;
            }
            // TODO: 调用 Python Agent 生成内容
            // 模拟生成结果
            plan.setAiFeedback("Mock AI feedback for plan: " + plan.getTitle());
            planMapper.updateById(plan);

            System.out.println("AI 生成完成，planId=" + message.getPlanId());
            channel.basicAck(tag, false);
        } catch (Exception e) {
            e.printStackTrace();
            channel.basicNack(tag, false, true); // 重新入队
        }
    }
}