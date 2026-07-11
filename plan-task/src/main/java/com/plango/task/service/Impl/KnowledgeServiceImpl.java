package com.plango.task.service.Impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.plango.common.dto.KnowledgeSyncMessage;
import com.plango.task.config.RabbitMQConfig;
import com.plango.task.entity.Knowledge;
import com.plango.task.mapper.KnowledgeMapper;
import com.plango.task.service.KnowledgeService;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.stereotype.Service;

@Service
public class KnowledgeServiceImpl extends ServiceImpl<KnowledgeMapper, Knowledge> implements KnowledgeService {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Override
    public IPage<Knowledge> listByUser(Long userId, int page, int size) {
        Page<Knowledge> pageObj = new Page<>(page, size);
        return page(pageObj, new LambdaQueryWrapper<Knowledge>()
                .eq(Knowledge::getUserId, userId)
                .eq(Knowledge::getDeleted, false)
                .orderByDesc(Knowledge::getCreatedAt)
        );
    }

    @CacheEvict(value = "knowledgeByUser", key = "#knowledge.userId")
    @Override
    public void createKnowledge(Knowledge knowledge) {
        save(knowledge);
        rabbitTemplate.convertAndSend(RabbitMQConfig.KNOWLEDGE_SYNC_QUEUE,
                new KnowledgeSyncMessage(String.valueOf(knowledge.getId()), "CREATE"));
    }

    @CacheEvict(value = "knowledgeByUser", key = "#knowledge.userId")
    @Override
    public void updateKnowledge(Knowledge knowledge) {
        updateById(knowledge);
        rabbitTemplate.convertAndSend(RabbitMQConfig.KNOWLEDGE_SYNC_QUEUE,
                new KnowledgeSyncMessage(String.valueOf(knowledge.getId()), "UPDATE"));
    }

    @CacheEvict(value = "knowledgeByUser", key = "#knowledge.userId")
    @Override
    public void deleteKnowledge(Knowledge knowledge) {
        removeById(knowledge.getId());
        rabbitTemplate.convertAndSend(RabbitMQConfig.KNOWLEDGE_SYNC_QUEUE,
                new KnowledgeSyncMessage(String.valueOf(knowledge.getId()), "DELETE"));
    }
}
