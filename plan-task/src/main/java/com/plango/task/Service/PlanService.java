package com.plango.task.Service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.plango.task.entity.Plan;

public interface PlanService extends IService<Plan> {
    void createPlanAndSendMessage(Plan plan);

}
