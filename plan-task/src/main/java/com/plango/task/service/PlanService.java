package com.plango.task.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.plango.task.entity.Plan;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.data.domain.Page;

import java.util.List;

public interface PlanService extends IService<Plan> {
//    void createPlanAndSendMessage(Plan plan);

    IPage<Plan> listByUser(Long userId, int page, int size);

    void createPlan(Plan plan);

    Plan selectById(Long id);

    void updatePlan(Plan plan);

    void deletePlan(Plan plan);

}
