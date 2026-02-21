说明
`/opsx:continue` 用于继续 OpenSpec 流程，生成或刷新下一阶段工件。

用法
- 基本：`/opsx:continue <proposal_id>`
- 省略参数：仅有一个 Active Change 时可直接 `/opsx:continue`

常见场景
- `/opsx:new` 或 `/opsx:ff` 之后推进到下一工件
- 手动修改了已有工件（如 `proposal.md`、`design.md`、`specs/`）后，重新生成后续工件

结果
根据当前工件状态生成或更新下一个工件（如 `design.md`、`specs/`、`tasks.md`）。
