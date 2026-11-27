---
type: regex
target: trace
pattern: '"type":"tool_use","id":"[^"]+","name":"mcp__[^"]+__(calc_run|form_calc|plan_effective_path|plan_spending|survival_rank)"'
weight: 1
---

At least one cost or duration was obtained from an SDK pricing call (calc_run, form_calc, plan_effective_path, plan_spending or survival_rank) rather than stated from memory. Checked over the whole run.
