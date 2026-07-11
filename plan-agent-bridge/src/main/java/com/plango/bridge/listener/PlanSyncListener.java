package com.plango.bridge.listener;

import com.plango.bridge.client.PlanAgentClient;
import com.plango.bridge.entity.Plan;
import com.plango.bridge.mapper.PlanMapper;
import com.plango.common.dto.PlanSyncMessage;
import com.rabbitmq.client.Channel;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class PlanSyncListener {

    @Autowired
    private PlanMapper planMapper;

    @Autowired
    private PlanAgentClient planAgentClient;

    @RabbitListener(queues = "plan.sync.queue")
    public void handleSync(PlanSyncMessage message, Channel channel, @Header(AmqpHeaders.DELIVERY_TAG) long tag) throws IOException {
        try {
            String op = message.getOperation();
            System.out.println("收到 ES 同步请求：planId=" + message.getPlanId() + ", operation=" + op);

            if ("DELETE".equals(op)) {
                planAgentClient.deletePlanFromIndex(message.getPlanId());
            } else {
                Plan plan = planMapper.selectById(message.getPlanId());
                if (plan == null) {
                    System.err.println("ES 同步失败：计划不存在 planId=" + message.getPlanId());
                    channel.basicAck(tag, false);
                    return;
                }
                planAgentClient.syncPlan(plan);
            }

            System.out.println("ES 同步完成：planId=" + message.getPlanId() + ", operation=" + op);
            channel.basicAck(tag, false);
        } catch (Exception e) {
            System.err.println("ES 同步异常：planId=" + message.getPlanId() + ", " + e.getMessage());
            channel.basicNack(tag, false, true);
        }
    }
}
