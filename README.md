# 深度学习 Idea 模板

此仓库提供一套面向深度学习基线项目的 `.codex` 模板，目标是持续产出能够支撑 `oral` 级论文的方法与实验内容。

核心入口只有三个 skill：

- `idea-discovery`
- `idea-execution`
- `idea-review`

## 快速开始

1. 将 `.codex`、`AGENTS.md`、`experience.md` 复制到目标基线仓库。
2. 记录一次基线锚点：

   ```bash
   git rev-parse HEAD > .codex/baseline_commit.txt
   ```

3. 如有需要，创建 `direction.md`，写入任务目标、数据集、硬约束、已有判断。
4. 按顺序启动第一轮：
   - `$idea-discovery`
   - `$idea-execution`
   - `$idea-review`

## 规则文件位置

根 `AGENTS.md` 只负责介绍仓库用途、运行时文件和入口 skill。

完整规则统一放在：

- `.codex/idea-workflow/workflows/idea-discovery.md`
- `.codex/idea-workflow/workflows/idea-execution.md`
- `.codex/idea-workflow/workflows/idea-review.md`

三份 `SKILL.md` 只负责把入口 skill 连接到这些规则文件。

## 实际使用顺序

### 1. 新 idea

每一轮新 idea 都从 `$idea-discovery` 开始。

这一阶段会写出：
- 一条主线
- 三个协同创新点
- 最多两个主要超参数
- 完整实验方案
- 第一批正式实验

`$idea-discovery` 会先读取本地材料，再按固定顺序调用三个 discovery 子代理：

- `paper-architect`
- `experiment-designer`
- `idea-critic`

其中：
- 主代理先负责仓库勘查、失败经验比对、基线契约恢复、必要时 Exa 补证、以及一次澄清
- `paper-architect` 专门负责生成 `Method`
- `experiment-designer` 专门负责生成 `Experiment Plan` 与 `Current Batch`
- `idea-critic` 从审稿视角检查完整 idea，并微调 `Method`、`Experiment Plan`、`Current Batch`，同时写出 `Outcome Bar` 与 `Review Notes`

如果仓库证据不足、基线字段仍无法确定、任一关键子代理失败、或者 `idea-critic` 未通过，`$idea-discovery` 会停止并指出缺失项，不会写出薄弱 idea。

### 2. 当前批次实现与运行

`$idea-execution` 只负责当前批次。

这一阶段会：
- 按 `Current Batch` 实现代码
- 创建一个新的实验脚本
- 用 `request_user_input` 披露实验数量、实验内容、分析项
- 用 `screen` 发起正式实验

只要正式实验已经发起，下一步就进入 `$idea-review`。

### 3. 结果评审

`$idea-review` 面向已经跑完的正式批次。

如果实验仍在运行，或者结果文件还没有写全，`$idea-review` 只会提示“当前批次还不能评审”，随后等待再次运行，不会写出正式评审结果。

当批次已经完整时，评审结果只有三类：

#### `improve`

含义：
- 当前 idea 还有继续深挖的空间
- 当前批次已经暴露出下一步可研究的问题
- 论文故事还没有完整收口

处理顺序：
1. `$idea-review` 先总结当前最好指标、与基线的差值、以及最重要的实验现象。
2. `$idea-review` 使用 `request_user_input` 发起多轮沟通，确认下一步改进方向，以及采用该方向的原因。
3. 沟通内容至少覆盖：
   - 当前主要缺口或异常现象
   - 改进假设
   - 采用该假设的理由
   - 下一批正式实验
   - 下一批分析项
4. 沟通完成后，`$idea-review` 会把“当前批次结果摘要 + 选择该改进方向的原因 + 新一批实验设计”写回 `.codex/active_idea.md`。
5. 然后回到 `$idea-execution`，实现并运行下一批正式实验。

`improve` 不会产生 git 提交。

#### `abandon`

含义：
- 当前 idea 已经没有可信的继续空间
- 或者现有证据已经说明目标提升难以成立

处理顺序：
1. `$idea-review` 将失败记录追加到 `experience.md`
2. 清理当前 idea 的日志、实验产物、实验脚本、代码修改
3. 将 `.codex/active_idea.md` 重置为空模板
4. 回到 `$idea-discovery`，开始下一个 idea

`abandon` 不会产生 git 提交。

#### `finish`

含义：
- 当前方法效果已经足够强
- 已经观察到不平凡且可解释的实验现象
- idea 本身已经足够支撑 `oral` 级论文的方法部分与实验部分

处理顺序：
1. `$idea-review` 将最好结果、关键实验现象、以及“为何已经足够停止”写入 `.codex/active_idea.md`
2. 生成一次正式 git 提交
3. 停止当前 idea

只有 `finish` 允许 git 提交。

## 最常见的循环

1. `$idea-discovery`
2. `$idea-execution`
3. `$idea-review`
4. 如果批次未完成，稍后再次运行 `$idea-review`
5. 如果结果是 `improve`，由 `$idea-review` 完成多轮沟通与写回，再运行 `$idea-execution`
6. 如果结果是 `abandon`，回到 `$idea-discovery`
7. 如果结果是 `finish`，停止当前 idea

## `oral` 级 idea 约束

每个 idea 都应满足下面的结构要求：

- 一条主线
- 三个相互配合的创新点
- 最多两个主要方法超参数
- 足以支撑论文方法部分的方法细节
- 足以支撑论文实验部分的实验与分析内容

## 运行时文件

- `.codex/baseline_commit.txt`：基线锚点
- `.codex/active_idea.md`：当前 idea 的唯一状态文件
- `.codex/logs/`：当前正式实验日志
- `experience.md`：被放弃 idea 的长期记录

`.codex/active_idea.md` 现在采用两层结构：

- 精简 frontmatter，只保存运行状态与评审结果
- 正文保存 `Baseline Contract`、`Method`、`Experiment Plan`、`Current Batch`、`Outcome Bar`、`Review Notes`

## discovery 子代理顺序

- 主代理：补基线契约、仓库现象、thesis seed、失败经验比对、必要时 Exa 补证
- `paper-architect`：生成 `Method`
- `experiment-designer`：生成 `Experiment Plan`、`Current Batch`、运行命令与产物字段
- `idea-critic`：给出通过或驳回，微调前三段内容，并写出 `Outcome Bar` 与 `Review Notes`
- `result-judge`：根据完整结果判断 `improve`、`abandon`、`finish`
- `improvement-planner`：基于当前结果提出下一轮改进方向、理由和沟通重点
