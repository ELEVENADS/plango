package com.plango.task.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.plango.task.service.PlanService;
import com.plango.task.entity.Plan;
import com.plango.task.mapper.PlanMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin
@RequestMapping("/plans")
public class PlanController {


    @Autowired
    public PlanService planService;

    @PostMapping
    public String create(@RequestBody Plan plan){
        planService.createPlan(plan);
        return "计划创建成功，ID：" + plan.getId();
    }

    @GetMapping("/user/{userId}")
    public IPage<Plan> listByUser(@PathVariable Long userId, @PathVariable int page, @PathVariable int size) {
        return  planService.listByUser(userId,page,size);
    }

}
