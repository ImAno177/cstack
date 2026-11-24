---
name: sharpen
description: Make a task deeper, not bigger, then rewrite the prompt. Use for /sharpen.
disable-model-invocation: true
---

I want a deeper version of this task, not a bigger one. Before rewriting it, do four things:

1. Say what a top professional in this field would do here that I'm not asking for.
2. Name the rawest material they would start from instead of what has already been digested for me.
3. Name the specific methods and tools they would use.
4. Say what, other than you or me, would show the result is right.

Then rewrite my prompt to ask for exactly that.

Leave choices that are mine to make open instead of deciding them.

Reply with the four answers, then the rewritten prompt in one block the user can paste. Run no part of the task.

Example (task: "summarize our churn data"):

> 1. An analyst would segment churn by cohort and cause, not report one rate.
> 2. They would start from the raw event table, not the dashboard export.
> 3. Survival curves (Kaplan-Meier) in SQL plus a notebook.
> 4. A holdout cohort the summary must predict.
>
> Rewritten prompt: "From the raw `events` table, build Kaplan-Meier retention curves per signup cohort and test the summary against the holdout cohort. Leave the choice of segments to me."
