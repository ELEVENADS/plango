-- 创建 plan_task 数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS plango_task DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
USE plango_task;
-- 建立计划表
CREATE TABLE IF NOT EXISTS `plan` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `user_id` BIGINT NOT NULL COMMENT '用户ID',
    `title` VARCHAR(200) NOT NULL COMMENT '计划标题',
    `description` TEXT COMMENT '计划详细描述',
    `plan_date` DATE NOT NULL COMMENT '计划执行日期',
    `start_time` TIME COMMENT '计划开始时间',
    `end_time` TIME COMMENT '计划结束时间',
    `priority` TINYINT NOT NULL DEFAULT 0 COMMENT '优先级：0-低，1-中，2-高',
    `status` VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '状态：PENDING(待办), IN_PROGRESS(进行中), COMPLETED(已完成), CANCELLED(已取消)',
    `ai_generated` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否由AI生成：0-否，1-是',
    `ai_feedback` TEXT COMMENT 'AI生成的额外建议或反馈',
    `tags` VARCHAR(500) COMMENT '标签，逗号分隔',
    `ext_info` JSON COMMENT '扩展信息，存储临时或不确定的结构化数据（如提醒配置、来源等）',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除：0-正常，1-已删除',
    PRIMARY KEY (`id`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_plan_date` (`plan_date`),
    INDEX `idx_status` (`status`),
    INDEX `idx_deleted` (`deleted`),
    INDEX `idx_user_date` (`user_id`, `plan_date`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='每日计划表';