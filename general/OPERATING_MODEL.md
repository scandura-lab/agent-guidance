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
- **C-005** Each worker builds in its own working copy. Nobody switches the branch of a shared checkout, or builds in the architect's copy.

## Review and gates

- **C-012** Review before every gate. The architect or a cold reader reads the change against its brief, and the witness record, before it spends a gate.
- **C-015** **The one exception to G-015:** a change to the gate's own protocol lands in two steps, a compatible reader first. It must pass under both the old gate and the new one. This applies only to the gate, because the gate must judge itself.

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

- **C-022** Spend each usage account fully by its reset, pacing per day. Route building to the account with more usage left per day before its reset, and tell Joe the split. Set the effort by task:
  - low for carrying a finished change forward;
  - medium for building;
  - high for reviews.
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
