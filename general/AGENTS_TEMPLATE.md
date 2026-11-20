# AGENTS.md template

Copy this into a repository's root and fill in each `CAPITALIZED` slot. Keep it to about 40 lines.

- Every line is a command or a pointer. When agents keep breaking a rule, make it a check (G-042), not another line. If this file has more "never" lines than commands, move them into checks.
- Add a `CLAUDE.md` that holds `@AGENTS.md`, so that every kind of agent reaches the same entry point.
- Every command must work in a fresh agent shell:
  - it starts with `cd ABSOLUTE_WORKTREE &&`, because the working folder does not persist between calls;
  - it uses absolute tool paths;
  - it contains no angle-bracket placeholders (such as `<path>`), which a shell reads as redirection;
  - it never takes a shared lock, and never runs the whole suite where the project has a test selector (G-025);
  - a command that runs code sets DATA_ROOT_OFF, the project's real-data location pointed at a folder that does not exist, so a worker's run cannot reach real data (G-024);
  - it chains with `&&`, or ends by printing and returning the real exit status, so a failure is never reported as a pass.
- Run each command once before publishing.

```markdown
# Agent instructions (PROJECT)

STATUS LINE, if the repository's document guard requires one.

The goal: read GOAL_FILE first. It is the one statement of what this project is for; this page never restates it (G-048 sub-point 5).

**A scoped worker reads this page, PRINCIPLES_COPY (with its examples), PROJECT_RULES and its brief, and nothing else** (C-002). The code it changes, the owner's file, callers and contract tests are part of the work. The architect reads the rest when needed.

The CAPITALS below (WORKTREE, SCRATCH, TASK, LANE, WORKER) come from your brief. A brief that lacks one, or a working copy that is missing or read-only, is a stop.

## Set up (new machine only)
ENVIRONMENT COMMANDS. Never change the shared environment from a working copy.

## Your working copy
The architect prepares WORKTREE. Check it: `cd WORKTREE && WRITABLE_CHECK`. Never create a worktree inside the main clone's `.git`, and never write to the main checkout.

## Check your work
`cd WORKTREE && DATA_ROOT_OFF CHECK_COMMAND WORKER`. It runs the selected tests (the whole suite only where the project has no selector, G-025), never under a shared lock.

## Prove the witness
`cd WORKTREE && WITNESS_COMMAND TEST_NODE`. It records the base and tip runs G-023 asks for.

## Find the owner
`OWNER_LOOKUP "WORD"`.

## Hand in
PUSH and HAND_IN_CHECK, then your hand-in: your final message to the architect (G-047).

## Where things are
Owners: MODULE_MAP. Plan: PLAN_FILE. Tasks: REGISTERS.

## Long-running workers and architects
CATCH_UP_COMMAND, then COORDINATION_PROTOCOL.

*End of AGENTS.md.*
```
