# 深度学习 Idea 流程模板

此仓库提供一套紧凑的 `.codex` 流程，用于深度学习基线项目中的 `oral` 级 idea 探索。

核心循环只包含三个 skill：

- `idea-discovery`
- `idea-execution`
- `idea-review`

## 快速开始

1. 将 `.codex` 目录、`AGENTS.md`、`experience.md` 复制到目标基线仓库中。
2. 记录一次基线锚点：
   ```bash
   git rev-parse HEAD > .codex/baseline_commit.txt
   ```
3. 如有需要，创建 `direction.md`，写入目标任务、数据集、硬约束、当前判断。
4. 用下面的顺序启动第一轮：
   - `$idea-discovery`
   - `$idea-execution`
   - `$idea-review`

整个循环始终围绕一个当前 idea 展开：
- discovery 负责写出一个 `oral` 级 idea，包括论文级方法提纲、完整实验计划、第一批正式实验
- execution 负责为当前批次创建新的实验脚本，完成启动前确认，并用 `screen` 发起正式实验
- review 负责判断当前证据是否已经证明价值，是否可以进入 git，或者是否应当放弃当前 idea

## 实际使用顺序

真实使用顺序由状态决定，不是只执行一次固定三步。

### 1. discovery 阶段

每轮新 idea 的起点都是 `$idea-discovery`。

可能出现两种结果：
- 如果基线字段不完整，或者当前仓库信息不足以支撑 `oral` 级论文内容，discovery 会停止，不会写入弱 idea。补齐缺失信息后，再次运行 `$idea-discovery`。
- 如果 discovery 成功，`.codex/active_idea.md` 会写入一个明确的 `Current Batch`。下一步进入 `$idea-execution`。

### 2. execution 阶段

只有当 `.codex/active_idea.md` 中已经存在清晰的 `Current Batch` 时，才进入 `$idea-execution`。

execution 的职责是：
- 实现当前批次需要的代码改动
- 为当前批次创建一个新的实验脚本
- 用 `request_user_input` 做启动前确认
- 用 `screen` 发起正式实验

只要实验已经启动，或者实验已经结束，下一步都进入 `$idea-review`。

### 3. review 阶段

`$idea-review` 用于正式实验启动后或结束后。

review 会同时给出两个结果：
- `decision`
- `value_status`

#### 情况 A：`decision=wait`

含义：
- 实验仍在运行，或者
- 证据还不完整，或者
- 证据互相冲突

下一步：
- 先不要运行 `$idea-execution`
- 等待实验结束，或者等待更多结果文件出现
- 然后再次运行 `$idea-review`

#### 情况 B：`decision=continue` 且 `value_status=unclear`

含义：
- 当前 idea 仍有继续价值
- 当前证据还不足以支持代码提交

下一步：
1. 先由 `$idea-review` 更新 `Current Batch`、`Value Bar`、`Next Batch`
2. 再运行 `$idea-execution`，执行这一批后续改进
3. 新一轮正式实验结束后，再运行 `$idea-review`

这是最常见的“继续完善、继续探索、继续分析”循环。

#### 情况 C：`decision=continue` 且 `value_status=supported`

含义：
- 当前批次已经达到价值门槛
- 当前代码和实验脚本值得保留到 git 历史中

下一步：
1. 先由 `$idea-review` 为当前有效批次创建批准提交，并记录到 `approved_commits`
2. 检查完整论文实验计划是否已经足够
3. 如果仍然缺少实验或分析，继续由 `$idea-review` 更新 `Current Batch` 和 `Next Batch`，然后运行 `$idea-execution`
4. 如果完整论文实验计划已经足够，就停在当前 idea，并保留已批准状态

`supported` 的含义是“当前批次已经值得保留”，不是“整个 idea 自动结束”。

#### 情况 D：`decision=terminate`

含义：
- 当前 idea 已经没有可信的继续空间，或者
- 现有证据已经表明目标提升无法达到

下一步：
1. 由 `$idea-review` 将失败记录追加到 `experience.md`
2. 由 `$idea-review` 创建只包含经验记录和状态重置的说明提交
3. 由 `$idea-review` 回退所有 `approved_commits`
4. 由 `$idea-review` 清理当前日志、实验产物、实验脚本、未提交代码修改
5. 回到 `$idea-discovery`，开始下一个 idea

## 常见顺序

单个 idea 最常见的顺序如下：

1. `$idea-discovery`
2. `$idea-execution`
3. `$idea-review`
4. 如果结果是 `wait`，稍后再次运行 `$idea-review`
5. 如果结果是 `continue + unclear`，运行 `$idea-execution`，然后再运行 `$idea-review`
6. 如果结果是 `continue + supported`，且完整论文实验计划仍未完成，运行 `$idea-execution`，然后再运行 `$idea-review`
7. 如果结果是 `terminate`，回到 `$idea-discovery`，开始下一个 idea

## `oral` 级 idea 约束

每个生成的 idea 都应满足下面的结构约束：
- 一条主线
- 三个相互配合的创新点
- 最多两个主要方法超参数
- 足以支撑论文方法部分的方法细节
- 足以支撑论文实验部分的实验与分析内容

## 运行时文件

- `.codex/baseline_commit.txt`：基线回退锚点
- `.codex/active_idea.md`：当前 idea 状态与下一步
- `.codex/logs/`：当前 `screen` 日志
- `experience.md`：终止 idea 的长期记录

`.codex/active_idea.md` 当前采用两层结构：
- 精简 frontmatter，只保存运行态与清理态字段
- 正文保存 `Baseline Contract`、`Paper Thesis`、`Innovation Points`、`Method Sketch`、`Full Experiment Program`、`Current Batch`、`Value Bar`

## 辅助 agents

- `repo-exa-scout`：从仓库与外部资料中寻找 thesis seed、基线契约、可测现象
- `paper-architect`：将 thesis seed 组织成 `oral` 级方法骨架、创新点、理论切入点、超参数约束
- `analysis-planner`：设计完整实验计划和第一批分析内容
- `experiment-designer`：设计当前批次脚本、实验列表、产物位置
- `idea-critic`：检查重合、混杂因素、价值门槛、停止条件
- `result-judge`：解释结果证据，并协助判断继续、等待、终止
