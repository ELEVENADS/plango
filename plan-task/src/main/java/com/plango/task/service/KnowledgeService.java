package com.plango.task.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.plango.task.entity.Knowledge;

public interface KnowledgeService extends IService<Knowledge> {

    IPage<Knowledge> listByUser(Long userId, int page, int size);

    void createKnowledge(Knowledge knowledge);

    void updateKnowledge(Knowledge knowledge);

    void deleteKnowledge(Knowledge knowledge);
}
