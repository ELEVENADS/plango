package com.plango.task.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.plango.task.entity.Knowledge;
import com.plango.task.service.KnowledgeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin
@RequestMapping("/knowledge")
public class KnowledgeController {

    @Autowired
    private KnowledgeService knowledgeService;

    @PostMapping
    public String create(@RequestBody Knowledge knowledge) {
        knowledgeService.createKnowledge(knowledge);
        return "知识文档创建成功，ID：" + knowledge.getId();
    }

    @PutMapping
    public String update(@RequestBody Knowledge knowledge) {
        knowledgeService.updateKnowledge(knowledge);
        return "知识文档更新成功，ID：" + knowledge.getId();
    }

    @DeleteMapping("/{id}")
    public String delete(@PathVariable Long id) {
        Knowledge knowledge = new Knowledge();
        knowledge.setId(id);
        knowledgeService.deleteKnowledge(knowledge);
        return "知识文档删除成功，ID：" + id;
    }

    @GetMapping("/user/{userId}")
    public IPage<Knowledge> listByUser(@PathVariable Long userId,
                                       @RequestParam(defaultValue = "1") int page,
                                       @RequestParam(defaultValue = "20") int size) {
        return knowledgeService.listByUser(userId, page, size);
    }
}
