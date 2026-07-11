package com.plango.bridge.listener;

import com.plango.bridge.client.PlanAgentClient;
import com.plango.bridge.entity.Knowledge;
import com.plango.bridge.mapper.KnowledgeMapper;
import com.plango.common.dto.KnowledgeSyncMessage;
import com.rabbitmq.client.Channel;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class KnowledgeSyncListener {

    @Autowired
    private KnowledgeMapper knowledgeMapper;

    @Autowired
    private PlanAgentClient planAgentClient;

    @RabbitListener(queues = "knowledge.sync.queue")
    public void handleSync(KnowledgeSyncMessage message, Channel channel, @Header(AmqpHeaders.DELIVERY_TAG) long tag) throws IOException {
        try {
            String op = message.getOperation();
            System.out.println("收到知识库同步请求：docId=" + message.getDocId() + ", operation=" + op);

            if ("DELETE".equals(op)) {
                planAgentClient.deleteKnowledgeFromIndex(message.getDocId());
            } else {
                Long id = Long.valueOf(message.getDocId());
                Knowledge knowledge = knowledgeMapper.selectById(id);
                if (knowledge == null) {
                    System.err.println("知识库同步失败：文档不存在 docId=" + message.getDocId());
                    channel.basicAck(tag, false);
                    return;
                }
                planAgentClient.syncKnowledge(knowledge);
            }

            System.out.println("知识库同步完成：docId=" + message.getDocId() + ", operation=" + op);
            channel.basicAck(tag, false);
        } catch (Exception e) {
            System.err.println("知识库同步异常：docId=" + message.getDocId() + ", " + e.getMessage());
            channel.basicNack(tag, false, true);
        }
    }
}
