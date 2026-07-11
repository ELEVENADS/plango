package com.plango.task.service.Impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.plango.task.service.PlanService;
import com.plango.task.config.RabbitMQConfig;
import com.plango.common.dto.PlanGenerateMessage;
import com.plango.common.dto.PlanSyncMessage;
import com.plango.task.entity.Plan;
import com.plango.task.mapper.PlanMapper;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class PlanServiceImpl extends ServiceImpl<PlanMapper,Plan> implements PlanService {

    @Autowired
    private RabbitTemplate rabbitTemplate;

//    @Override
//    public void createPlanAndSendMessage(Plan plan) {
//        save(plan);
//        if(Boolean.TRUE.equals(plan.getAiGenerated())){
//            PlanGenerateMessage message = new PlanGenerateMessage();
//            message.setPlanId(plan.getId());
//            message.setUserId(plan.getUserId());
//            message.setTitle(plan.getTitle());
//            message.setDescription(plan.getDescription());
//            rabbitTemplate.convertAndSend(RabbitMQConfig.PLAN_GENERATE_QUEUE, message);
//        }
//    }

    @CacheEvict(value = "planByUser", key = "#plan.userId")
    @Override
    public void createPlan(Plan plan){
//        保存计划
        save(plan);
//        发送 ES 同步消息
        rabbitTemplate.convertAndSend(RabbitMQConfig.PLAN_SYNC_QUEUE, new PlanSyncMessage(plan.getId(), "CREATE"));
//        检查ai标志，TRUE则发送到消息队列中
        if(Boolean.TRUE.equals(plan.getAiGenerated())){
            PlanGenerateMessage message = new PlanGenerateMessage();
            message.setPlanId(plan.getId());
            message.setUserId(plan.getUserId());
            message.setTitle(plan.getTitle());
            message.setDescription(plan.getDescription());
            rabbitTemplate.convertAndSend(RabbitMQConfig.PLAN_GENERATE_QUEUE, message);
        }
    }

    @Override
    public IPage<Plan> listByUser(Long userId, int page, int size) {
        Page<Plan> pageObj = new Page<>(page,size);
        return page(pageObj,new LambdaQueryWrapper<Plan>()
                .eq(Plan::getUserId,userId)
                .eq(Plan::getDeleted,false)
                .orderByDesc(Plan::getCreatedAt)
        );
    }

    @Cacheable(value = "planByUser", key = "#id")
    @Override
    public Plan selectById(Long id){
        return getById(id);
    }

    @CacheEvict(value = "planByUser", key = "#plan.userId")
    @Override
    public void updatePlan(Plan plan) {
        updateById(plan);
        rabbitTemplate.convertAndSend(RabbitMQConfig.PLAN_SYNC_QUEUE, new PlanSyncMessage(plan.getId(), "UPDATE"));
    }

    @CacheEvict(value = "planByUser", key = "#plan.userId")
    @Override
    public void deletePlan(Plan plan) {
        removeById(plan.getId());
        rabbitTemplate.convertAndSend(RabbitMQConfig.PLAN_SYNC_QUEUE, new PlanSyncMessage(plan.getId(), "DELETE"));
    }


}
