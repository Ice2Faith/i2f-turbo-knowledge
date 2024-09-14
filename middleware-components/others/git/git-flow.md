# Git 工作流规范


## 1. 名词定义
- PR: product request, 产需、产品需求，负责和客户明确需求，给出产品原型，输出需求文档
- PM: project manager, 产品管理/产品经理，负责管理项目运作，以及人力/时间等资源的协调
- PO: project owner, 产品拥有人，负责协调项目代码，包括代码审查(review)，代码分支管理等
- Dev: developer, 开发者，负责完成自己的开发任务(task)，并完成白盒测试（主要单元测试，其次集成测试）
- DevTeam: develop team, 开发团队，负责整个项目的开发工作
- Test: tester, 测试人员，负责对开发的功能进行测试，包括需求测试、功能测试（黑盒测试）、集成测试等
- Ops: operator, 运维人员，负责对各个运行环境的搭建和运维工作，包括环境搭建、日常运维、运维监控等
- Cfg: configurator, 配置人员，负责对代码仓库基线(baseline)的控制，以及项目文档的归档管理等
- request: 需求，指一个完整的功能或者模块，或者一系列相关联的功能
- task: 任务，是将需求拆分为多个独立编码任务的单元，分配给具体的开发者(developer)
- archive: 制品，是代码的输出结果，是可运行的程序，交付的产品


## 2. 敏捷开发(Scrum)项目管理体系
- Scrum 使用【故事/任务】+【阶段需求】来规范开发流程
- 【阶段需求】与【需求号】挂钩
- 上线以【需求号】为准
- 因此，结合实际的Scrum流程
- 串接Git工作流，才能实现最佳适配
- 下面，来制定Git工作流程
- 同时，敏捷开发，是当下主流的项目管理方式
- 可能会根据公司的实际情况，有一定的变体

### 2.1. 敏捷流程
- 产需(PR/PM)每周根据下阶段上线需求(request)拆分为任务(task)
- 在例会上，产需(PR/PM)给开发团队(DevTeam)讲解上线需求(request)，并将任务(task)分配给开发者(developer)
- 开发者(developer)进行编码、调试工作，完成自己的任务(task)，并将自己任务结果提交到测试环境(test)，并提交给测试人员(test)进行测试
- 测试人员(test)进行测试提出问题(issue)后反馈给开发者(developer)，开发者(developer)进行修复，测试人员(test)进行回归测试
- 直到，功能满足需求(request)描述，结束这个开发与测试的流程
- 在整个需求(request)完成测试之后，进入上线发布环节
- 项目管理(PM)编写上线材料，提交给配置人员(Cfg)，完成需求确认
- 配置人员对已确认的需求相关的代码分支合并到主分支(release/master)，完成基线(baseline)提升
- 配置人员(Cfg)通知运维人员(Ops)打包主分支(release/master)，生成制品程序(archive)
- 运维人员(Ops)将制品(archive)部署到生产环境，完成产品升级
- 测试人员(Test)对升级的产品进行验证测试，当验证出现问题时，需要通知开发团队(DevTeam)进行紧急修复(hotfix)
- 开发团队(DevTeam)完成紧急修复(hotfix)验证通过之后，整个需求完成上线发布
- 到此流程就完毕了

## 3. Git 工作流

### 3.1. 分支示例
- release
- test
- request
    - REQ26634-1
    - REQ16455-1
    - REQ17788-1
    - REQ17788-2
- feature
    - sms-notice
    - dashboard
    - scheduler
    - home-bigscreen
    - g-35548
- hotfix
    - 240808
- publish
    - 240808

### 3.2. 主要分支
- release: 别名 master/product， 主分支/基线分支
    - 基线分支，任何分支都应该从基线分支建立
    - 只允许request分支合并到此分支
    - 不允许删除此分支
    - 不允许在此分支提交代码
- test 测试分支
    - 测试分支，任何已开发的分支都允许合并到此分支
    - 只允许feature/hotfix合并到此分支
    - 不允许删除此分支
    - 不允许在此分支提交代码
- request 需求分支/阶段分支
    - 需求分支，每个阶段明确上线的内容
    - 只允许publish分支合并到此分支
    - 不建议删除此类分支，但需要定期清楚老旧分支
        - 此类分支数量需要保留一定的数量
        - 可根据自己团队情况，保留3个以上10个以内的近期需求
    - 不允许在此分支提交代码
        - 除非在还未上线时，通过项目团队人员确认之后
        - 可允许少量变更直接在此分支提交变更
    - 命名规则：request/需求号-阶段号
        - 例如：request/REQ26634-1
        - 表示需求26634的第1个阶段
    - 分支创建
        - 此分支，在上线申请填写完毕之后，由PM/PO给出需求号（例如REQ26634-1）
        - 并指定任意开发人员(或开发组长)，从release分支创建此需求分支 request/REQ26634-1
        - 并将指定的publish预发布分支，合并到此需求分支，完成分支内容合并
        - 最后，交由配置人员，打包编译发布
        - 由配置人员合并此分支到release分支
        - 完成上线
- feature: 别名 develop， 特性分支/开发分支
    - 特性分支，各个开发根据自己的开发任务/需求故事完成编码
    - 只允许release/hotfix分支合并到此分支，严禁feature分支之间相互合并
    - 建议删除此类分支，在完成合并到release分支之后
        - 在完成合并到release分支之后
        - 表示本次feature已经完成上线
        - 不应该再继续在此分支上继续修改
        - 而是应该从release分支建立新的feature分支继续开发
        - 保证与release的基线(baseline)一致
    - 命名规则：feature/自定义名称
        - 例如：feature/home-bigscreen
        - 表示首页大屏的需求开发
        - 例如：feature/g-35548
        - 表示进行35548这个故事编号的需求开发
    - 分支创建
        - 各个开发从release分支创建各自的需求分支 feature/home-bigscreen
    - 需求冲突
        - 如果多个开发人员，开发内容涉及到同样的内容
        - 则应该将这冲突的多个开发人员的分支合并为一个新分支
        - 多个开发人员同时维护这一个分支的代码
        - 在进行任意的push操作之前
        - 必须先进行update操作，并解决可能的conflict冲突
        - 在本地完成merge之后，再进行push操作
- hotfix 热修复分支/线上问题修复分支
    - 热修复分支，通常用于再上线完毕后，或临时处理线上问题时，进行代码的调整
    - 只允许从release分支创建此分支
    - 如果release分支还未完成最后一次的request分支的合并时
        - 则使用最后一次request分支代替release分支（不建议）
    - 建议删除历史分支
        - 在hotfix分支合并到release分支之后
        - 表示热修复工作已经完成
        - 不在需要此分支
        - 因此建议删除此分支
    - 命名规则：hotfix/日期
        - 例如：hotfix/240808
        - 表示24年8月8号进行的热修复内容
    - 分支创建
        - 如果，已经完成request分支合并到release分支后进行的热修复
            - 则从release分支创建热修复分支 hotfix/240808
        - 如果，还未完成request分支合并到release分支进行的热修复（不建议）
            - 则从request分支创建热修复分支 hotfix/240808
- publish: 别名 preview/pre/uat， 预发布分支
    - 预发布分支，由于request需求分支，需要填写上线申请之后或其他原因，导致没有需求号，无法创建分支
    - 则可以使用预发布分支，进行对request分支内容的预先合并，request分支的内容保持和publish分支一致
    - 此分支只允许从release分支创建
    - 只允许release/feature/hotfix分支合并到此分支
    - feature分支应该时PM/PO指定要上线的需求涉及到的内容的分支
    - 建议删除历史分支
        - 当完成合并到release之后
        - 表示已经完成上线
        - 预发布分支已经失去意义
        - 可以删除历史分支
        - 保留最后1~2个分支，用以表示上次上线时间即可
        - 用来和hotfix分支进行对照，以确定哪些hotfix分支是有意义的
    - 命名规则：publish/日期
        - 例如：publish/240808
        - 表示在24年8月8号（或者计划上线日期）创建的预发布分支，下次上线的内容就是最后一个预发布分支的内容
        - 在上线时，request分支直接从最后一个publish分支创建

### 3.3.一般流程
- release - feature - test - publish - request - release
- 各个开发者(developer)根据自己的任务(task)从release分支创建自己的特性分支(feature)
- 开发者(developer)完成任务(task)的开发工作之后，自行合并(或PO审查并合并)到test分支
- 本阶段需求完成后，PM/PO(也可以是指定开发者，比如开发组长)从release分支创建预上线分支publish
- 各个涉及到本次上线需求任务(task)的开发者(developer)将自己的feature分支合并到publish分支
- PO(或者指定的开发组长)将上阶段的所有hotfix合并到publish分支
- 合并期间，如果发生代码冲突，则由feature的开发者(developer)与其他成员确认解决冲突后合并
- PM进行上线材料申请，上线时间到达之后，PO从release分支创建request分支，并将publish分支合并到request分支
- 配置人员(Cfg)将request分支合并到release分支，完成基线(baseline)提升
- 运维人员(Ops)从release分支打包输出制品(archive)进行部署到生产环境
- 测试人员(Test)进行验证测试，如果发现验证问题(issue)
- PR/PM确认是必要紧急修复的问题的话，开发团队(DevTeam)进行热修复
- 开发者(developer)从release分支创建hotfix分支，修复问题并提交，注意同时合并到test分支
- 验证通过后完成上线发布流程，本轮流程结束

### 3.4. 案例讲解
- 上次上线热修复分支
    - hotfix/240808
- 本次计划上线日期
    - 240822
- 计划上线需求号
    - REQ26153-1
- 分配的开发任务
    - active-report 活跃报表
    - fee-report 费用报表
    - flow-upgrade 流程升级
- 则分支应该如下
    - release
    - test
    - hotfix
        - 240808
    - feature
        - active-report
        - fee-report
        - flow-upgrade
    - publish
        - 240822
    - request
        - REQ26153-1
- 则合并规则如下
    - 从release分支分别创建feature/active-report,feature/fee-report,feature/flow-upgrade分支进行开发
    - 如果指定的feature依赖hotfix的内容，则允许将hotfix分支合并到feature分支
    - feature/active-report,feature/fee-report,feature/flow-upgrade合并到test完成测试
    - 从release分支创建publish/240822预发布分支
    - 将feature/active-report,feature/fee-report,feature/flow-upgrade分支合并到publish/240822分支
    - 将hotfix/240808分支合并到publish/240822分支
    - 到这里，预发布分支已经完成合并与解决冲突
    - 从release分支创建request/REQ26153-1需求分支
    - 将publish/240822分支合并到request/REQ26153-1完成需求分支
    - 将request/REQ26153-1分支合并到release分支完成上线基线提升

### 3.5. Git使用约束
- 在进行push之前，先进行pull拉去更新，解决可能得conflict冲突
- 谨慎使用rebase
- 谨慎使用force push
- 注意使用cherry-pick
- 建议统一commit时进行代码格式化
- 建议统一使用commit message的格式
- 格式定义如下
```bash
提交类型(业务范围): 修改描述

修改详情 
```
- 提交类型定义
    - feat/feature: 新功能，功能调整
    - fix/fixed: 问题修复，调整
    - doc/docs: 文档或者注释的变更
    - style: 代码格式调整，格式化，去除无用导入类等
    - refactor: 功能代码的重构，类名、包名、方法名、变量名等重命名等
    - perf: 性能优化调整
    - test: 单元测试代码
    - revert: 撤回提交
- 举例
```bash
feat(费用报表): 添加统计费用报表逻辑

添加定时报表生成
添加报表查询接口
添加报表导出功能
```
- 在IDEA中，可以使用插件(Git Commit Template Check)
- 这样就可以统一开发团队的提交信息