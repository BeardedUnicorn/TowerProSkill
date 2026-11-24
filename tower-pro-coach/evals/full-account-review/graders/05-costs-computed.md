---
type: regex
target: trace
pattern: '"type":"tool_use","id":"[^"]+","name":"mcp__[^"]+__(calc_run|form_calc|plan_effective_path)"'
weight: 1
---

At least one cost or duration was obtained from an SDK pricing call (calc_run, form_calc or plan_effective_path) rather than stated from memory. Checked over the whole run.
