package com.plango.notification.listener;

import com.plango.common.dto.NotificationMessage;
import com.plango.notification.config.RabbitMQConfig;
import com.rabbitmq.client.Channel;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class NotifyListener  {

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    @RabbitListener(queues = RabbitMQConfig.NOTIFY_QUEUE)
    public void handleNotify(NotificationMessage message, Channel channel, @Header(AmqpHeaders.DELIVERY_TAG) long tag) throws IOException {
        try {
            System.out.println("收到通知消息:" + message);
//        点对点推送到 /user/{userId}/queue/notifications
            messagingTemplate.convertAndSendToUser(
                    message.getTargetUserId().toString(),
                    "/queue/notifications",
                    message
            );
            channel.basicAck(tag, false);
        } catch (Exception e) {
            System.err.println("通知推送异常：" + e.getMessage());
            channel.basicNack(tag, false, true);
        }
    }

}
