package com.plango.task.controller;


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
    public PlanMapper planMapper;

    @PostMapping
    public String create(@RequestBody Plan plan){
        planMapper.insert(plan);
        return "计划创建成功，ID：" + plan.getId();
    }

    @GetMapping("/user/{userId}")
    public List<Plan> listByUser(@PathVariable Long userId) {
        return planMapper.selectList(
                new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<Plan>()
                        .eq(Plan::getUserId, userId)
                        .eq(Plan::getDeleted, false)
        );
    }

}
