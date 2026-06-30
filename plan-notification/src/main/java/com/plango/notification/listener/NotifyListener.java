package com.plango.notification.listener;

import com.plango.common.dto.NotificationMessage;
import com.plango.notification.config.RabbitMQConfig;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Component;

@Component
public class NotifyListener  {

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    @RabbitListener(queues = RabbitMQConfig.NOTIFY_QUEUE)
    public void handleNotify(NotificationMessage message) {
        System.out.println("收到通知消息:" + message);
//        点对点推送到 /user/{userId}/queue/notifications
        messagingTemplate.convertAndSendToUser(
                message.getTargetUserId().toString(),
                "/queue/notifications",
                message
        );

    }

}
