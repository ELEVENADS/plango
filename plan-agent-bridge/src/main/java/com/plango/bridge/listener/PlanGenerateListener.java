package com.plango.bridge.listener;

import com.plango.bridge.entity.Plan;
import com.plango.bridge.mapper.PlanMapper;
import com.plango.common.dto.PlanGenerateMessage;
import com.rabbitmq.client.Channel;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
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
//                    channel.basicAck(tag, false);
                        return;
                    }
                    // TODO: 调用 Python Agent 生成内容
                    // 模拟生成结果
                    plan.setAiFeedback("Mock AI feedback for plan: " + plan.getTitle());
                    planMapper.updateById(plan);

                    System.out.println("AI 生成完成，planId=" + message.getPlanId());
//                channel.basicAck(tag, false);
                } catch (Exception e) {
                    e.printStackTrace();
//                channel.basicNack(tag, false, true); // 重新入队
                } finally {
                    lock.unlock(); // 确保锁释放
                }
            } else {
//                获取锁失败
                System.out.println("获取锁失败，可能被占用"+ message.getPlanId());
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("加锁被中断");
            throw new RuntimeException(e);
        }
    }
}