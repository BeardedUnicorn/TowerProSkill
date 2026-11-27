---
type: llm
focus: last_message
weight: 1
---

PASS if the answer gives an explicit cash figure for the 100 Health levels, counted from the player's own Workshop level (the level the run starts at), and calls it cash.
FAIL if it gives no figure, gives only a coin price, prices the levels from level 0 instead of the player's level, or adds or compares cash and coins as if they were one currency.
