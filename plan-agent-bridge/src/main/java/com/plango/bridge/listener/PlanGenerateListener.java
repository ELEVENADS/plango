package com.plango.bridge.listener;

import com.plango.bridge.client.PlanAgentClient;
import com.plango.bridge.entity.Plan;
import com.plango.bridge.mapper.PlanMapper;
import com.plango.common.dto.NotificationMessage;
import com.plango.common.dto.PlanGenerateMessage;
import com.rabbitmq.client.Channel;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

@Component
public class PlanGenerateListener {

    @Autowired
    private PlanMapper planMapper;

    @Autowired
    private RedissonClient redissonClient;

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Autowired
    private PlanAgentClient planAgentClient;

    @RabbitListener(queues = "plan.generate.queue")
    public void handleGenerate(PlanGenerateMessage message, Channel channel, @Header(AmqpHeaders.DELIVERY_TAG) long tag) throws IOException {
//        锁设置
        String lockKey = "plan.generate.lock";
        RLock lock = redissonClient.getLock(lockKey);

        try{
//          加锁
            if (lock.tryLock(5,10, TimeUnit.SECONDS)) {
                try {
                    System.out.println("收到 AI 生成请求：planId=" + message.getPlanId());
                    Plan plan = planMapper.selectById(message.getPlanId());
                    if (plan == null) {
                        System.err.println("计划不存在");
                        channel.basicAck(tag, false);
                        return;
                    }
                    String aiFeedback = planAgentClient.generate(plan);
                    plan.setAiFeedback(aiFeedback);
                    planMapper.updateById(plan);

                    System.out.println("AI 生成完成，planId=" + message.getPlanId());

                    NotificationMessage notificationMessage = new NotificationMessage(
                            plan.getUserId(),
                            "计划生成完成",
                            "您的计划「" + plan.getTitle() + "」已生成，请查看。",
                            "PLAN_GENERATED"
                    );
                    rabbitTemplate.convertAndSend("plan.notify.queue", notificationMessage);

                    channel.basicAck(tag, false);
                } catch (Exception e) {
                    e.printStackTrace();
                    channel.basicNack(tag, false, true); // 重新入队
                } finally {
                    lock.unlock(); // 确保锁释放
                }
            } else {
//                获取锁失败，重新入队
                System.out.println("获取锁失败，可能被占用"+ message.getPlanId());
                channel.basicNack(tag, false, true);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("加锁被中断");
            throw new RuntimeException(e);
        }
    }
}