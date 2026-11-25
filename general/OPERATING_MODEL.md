# Operating Model

How architects and workers organize on Joe's projects. The engineering rules, with their glossary, are in [ENGINEERING_PRINCIPLES.md](ENGINEERING_PRINCIPLES.md). A worker needs nothing from this page: its brief follows C-003. The history of each C id is in [DECISIONS.md](DECISIONS.md). A project's own mechanics (its coordination log, status words, commit keys and gate scripts) are in that project's runbook.

Four terms used on this page:
- **Lane:** one area of the work, such as processing or the GUI.
- **Wave:** a planned group of tasks.
- **Cold reader:** someone who judges work without the author's framing.
- **Seam:** a boundary in the code where the piece on each side would be reusable on its own (G-002).

## Roles

| Who | Does | Never |
|---|---|---|
| **Joe** | Decides science, product and anything touching real data; reviews what was built. | Is asked what the documents or the literature already answer. |
| **Architect** (one per lane) | Plans, surveys the code, writes briefs, rules on stops, reviews, gates, lands, talks to Joe, keeps workers busy. | Writes product code. |
| **Long-running worker** | Takes tasks from the project's task list across many sessions; builds and reviews. | Rules or lands. |
| **Scoped worker** | Builds one brief in its own working copy and hands in. | Reads beyond its budget (C-002), rules, lands, or pushes to the main line. |
| **Cold reader** | Judges work or a page it did not write. | Is given the author's conclusion. |

**Only the architect:**
- rules on a stop;
- changes a governing document;
- reviews, gates and lands;
- reads real data into its own folder;
- runs a tested command that writes real data, with the data owner's permission (G-024);
- speaks to Joe, and to the other architect where a project has two.

## Workers and briefs

- **C-001** At every wake (each time the architect starts a session or is woken), the architect first gives each unblocked task a worker.
- **C-002** A scoped worker reads only what its project's start page (`AGENTS.md`) lists, plus its brief. It reports a gap instead of searching. *Why:* full onboarding cost each worker a third or more of its session.
- **C-003** This is the one definition of a brief. A brief holds everything the worker needs, and a brief missing any part is a stop (G-036):
  - the goal;
  - the owner (its file and the names it defines), its contract tests, and its count of other copies, from the architect's survey;
  - every caller, if a path is removed or renamed (G-015);
  - the extraction, if the change adds a step to a module that already does several (G-002);
  - the exact files it may change, tests included;
  - the witness, and whether the change adds behaviour or keeps it (G-023);
  - the human surface (what a person can now do, and where), or "internal";
  - the check command;
  - a writable working copy, given one of two ways: an absolute path to a clone or worktree the architect prepared; or the main clone's path, which the worker only reads, plus a writable parent folder for the worker's own clone;
  - a scratch folder outside the working copy;
  - the names to use: task id and lane;
  - the reading list and the effort level.

  A brief names its parts by exact file and line, with no narrative, and fits the project's line cap, where its runbook declares one. A long brief is resent as context on every worker call.
- **C-005** Each worker builds in its own working copy. Nobody switches the branch of a shared checkout, or builds in the architect's copy.

## Review and gates

- **C-012** Review before every gate. The architect or a cold reader reads the change against its brief, and the witness record, before it spends a gate.
- **C-015** **The one exception to G-015:** a change to the gate's own protocol lands in two steps, a compatible reader first. It must pass under both the old gate and the new one. This applies only to the gate, because the gate must judge itself.

## Handoffs and checks

How work passes between architects and workers without a slip. Each line names the check that holds it, so nobody has to remember it.
- **C-030 Claim before anything is written.** A task reads as claimed in the project's task list before any worker commits on it. The dispatcher confirms that with a command, not from memory, because a project's tooling keys each commit to a claimed task.
- **C-031 Stacked work lands in its order.** A change built on another change that has not landed is gated after it: in the same batch with its base first, or once the base lands. Its task names the base.
- **C-032 Split work by what each worker can do.** When a worker's sandbox refuses a step (writing version-control data, using the network), the worker does what it can and says what it could not do. A cheaper worker, or the architect, does the mechanical rest. Nobody reaches a refused result another way (G-036 sub-point 2).
- **C-033 The architect owns the file list.** A task's list names exactly what may change: paths, and the entries inside shared files such as a map or a registry, never a whole shared file. A worker who needs more stops and names it; the architect widens the list and records why.
- **C-034 A pushed mistake is fixed forward.** A wrong commit on a published branch is replaced on a new branch, never by rewriting history (G-037 sub-point 2).
- **C-035 Every handoff carries its proof.** A hand-in without both halves of its witness (for example, from a builder that could not run the base) gets the missing half from the architect before the task is queued (G-023).
- **C-036 Whoever posts watches for the answer.** An entry on a channel is followed by a watcher on that channel. Silence is never read as agreement.
- **C-037 Scratch is put away or thrown out.** Each worker keeps everything it makes in the scratch folder its brief names, and cleans up before it hands in. It removes base copies, temporary files and its own working copy once its work is pushed. What must last goes somewhere durable and named, and the hand-in names it; the rest is deleted. The architect sweeps finished tasks' folders after each landing. Nothing is kept in a temporary area the system purges by itself.
- **C-038 Learned once, written once.** How to start a worker, and each fact about a worker's or a machine's environment that voids work, lives in the shared toolkit (`toolkit/README.md`, `toolkit/codex_worker.py`). An architect starts workers with it, and proposes the new fact there the day it learns one, instead of keeping it in its own notes.

## Stalls and repeats

- **C-008** Stalls.
  1. A long-running agent never ends a turn while holding work. It waits on an event with a timeout (G-032), and posts "BLOCKED" before it stops.
  2. The architect judges a worker by its last act, every couple of hours, not by the coordination log. After a two-hour stall, the worker's unstarted tasks move to another worker. Joe hears only if that fails.
- **C-019** A task that fails twice, at review or at the gate, is re-planned one level up (its brief is rewritten), never retried as it is.
- **C-010** Read the other architect's own entry, never a worker's relay. Permission to edit another's file names the file and the lines. A ruling that proves wrong is withdrawn openly, in the coordination log.

## Planning

- **C-017** Slice work at measured seams (boundaries found in the code), not by topic. A piece that lands separately is its own task, and task numbers are never reused.
- **C-018** Where a project has two architects, both agree a wave and review it before its tasks open.

## Budgets and machines

- **C-022** Spend each usage account fully by its reset, pacing per day. Route building to the account with more usage left per day before its reset, and tell Joe the split. Match each worker's model and effort to the thinking the task needs, never more:
  - **mechanical** (carrying a finished change forward, a clean merge, running named tests, a register or fence edit): the smallest model at low effort;
  - **building to a clear plan** (an owner, a fence and a witness already stated), and read-only censuses: a mid-size model at medium effort;
  - **judgment** (diagnosing a red, revising a stale plan, a red team, anything a ruling depends on): the strongest model at high effort.
  A worker that stops because the task needed more judgment than its tier is re-briefed one tier up, never retried as it is (C-019).
- **C-021** No machine wakes or runs on a permanent schedule, except the project's declared nightly test run. Keeping a machine awake is tied to a working stretch.

## Working with Joe (architects)

- **C-023** Landed means built, never done. Joe reviews real outputs and screenshots, never a command packet.
- **C-024** Before asking Joe, search his rulings, the documents and the literature, and ask only what is his. Questions go to him one at a time, in chat, most important first. Each comes with full context, a recommendation, its consequences and contingencies, and lettered options, with no recommendation when the question is science. Each answer is recorded with its reasons. A page of questions is the architect's backlog, never a list sent to him.
- **C-025** Standing permission means proceed. Compute first, into a place you own, and ask only to move results into real data. Park only the blocked piece, and finish work in flight before proposing new scope.
- **C-026** When a message is unclear, state your reading and ask. When an action Joe approved is blocked by a permission only he can grant, give him the single command to run. This is a permission step, not a review (C-023).
- **C-027** Report your own lane's work. When another lane holds you up, re-slice or do the unblocked step.
- **C-028** A page or result a person reads gets cold readers and several drafts before Joe sees it. An analysis is validated before it is scaled.

**Retired:** C-011 is now G-047, C-020 is now C-008, and C-029 is now G-036.

**Moved to the project's runbook:** C-004, C-006, C-007, C-009, C-013, C-014 and C-016.
