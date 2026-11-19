# Decisions: the general register

The record behind [ENGINEERING_PRINCIPLES.md](ENGINEERING_PRINCIPLES.md) (the G rules) and the general coordination rules in [OPERATING_MODEL.md](OPERATING_MODEL.md) (the C rules). The rule text lives on those pages; this register holds the history. Ids are never reused.

Each entry gives:
- **Absorbs:** retired ids folded into this one.
- **Words:** Joe's words, verbatim.
- **Incidents:** the corrections on record. Their count is a minimum.
- **Why:** the reason for the rule.
- **Enforce:** a check pattern any project can adopt, or `judgment: <who>`.

All dates are 2026, and "n.r." means not recorded. Every entry is **live**. A project records its own checks for these ids in its own register.

## Engineering rules (G)

### G-001 · A unit is a foundational piece
**first** 07-22; law 10-07; step test, general steps and foundational pieces ruled by Joe 11-19 · **applies to** all product code
- **Words:**
  - *"size law is arbitrary … what we need is a logic of modularity rule that ensures modules are contracted by input/output so that they can be built/tested/verified and then relied upon by contract (mostly)."*
  - *"it is very hard to understand how we could have a 3000 line function that is modularized appropriately."* (10-07)
  - His standing instruction to every agent: *"the code logic should also be human understandable and comprised of conceptually-defined, testable code blocks/functions/modules."*
  - **Ruling, 11-19** (on the size question): *"WRT the size limit, I think this is artificial and brittle and I challenge the idea that a monolithic function can be 'one nominal behavior' b/c that is likely an abstraction hiding many submodules. This may be too much for an AI agent to adjudicate: I have found abstract reasoning a real weakness in public ai models but just because you can write a 'this does one thing' idea does not make it modular. Because that 'one thing' may require several steps so it is not one thing but many."*
  - **Ruling, 11-19** (on generality): *"we should always favor generalizable functions that can be reused predictably in our repo. If we write a bunch of 'steps' that are specific to a larger unit, they can't be reused and the modularity is somewhat artificial. It is just writing the code in blocks but the brittleness problem is not fixed and modularity is technical rather than useful."*
  - **Ruling, 11-19** (on the goal): *"your 2nd issue is important and I think that's where conceptual modularization comes in. One verb is also brittle. Modularity also has to favor portability, generalization and re-usability. a single purpose module isn't much better than a monolith. it is just a monolith cast to pieces. Definitely better but not the goal of building foundational pieces that can be reused with confidence. While this is not always possible it is always the goal"*
  - **On reuse, 11-19:** *"use, widen or wrap that"*. This matches his 10-07 law on reuse by wrapping: *"we use a module, wrapped as needed to ensure against drift and to help limit the amount of redundant testing"*. Wrapping means a new unit that calls the existing one and adds what is needed, leaving the original unchanged.
  - **On scope, 11-19:** *"I think the foundational piece is specific to the repo. otherwise things become too abstract. No?"* The architect agreed. Reuse is judged inside the project: another caller means an existing module, or one the project's plan names. "Portable" keeps only its G-010 sense (no host, machine or user assumptions), and each project's rules say what its foundational pieces are.
- **Incidents (4):**
  - 07-22: four overlapping front doors, and a ~20,000-line subsystem inside one layer.
  - 10-07: 62 modules over 1,000 lines; a one-word label change cost a 30-minute gate.
  - 11-19: agents were still building brittle blocks.
  - 11-19, round 4: a reviewer showed that a broad owner can grow into a massive block while still claiming "one job".
- **Why:**
  - "One thing" is an abstraction an agent can always claim. Listing the steps is a concrete test that does not rest on abstract judgement.
  - A size limit was rejected as artificial and brittle.
  - Pieces that serve only one caller are "a monolith cast to pieces". The goal is a foundational piece: general, portable, contracted, tested, and reusable with confidence. The concrete test is to name another caller in this project that could use the piece unchanged. If none exists, the code stays inside its caller and the hand-in says why.
  - The round-5 floor ("one glossary verb applied once") was removed. Joe: *"One verb is also brittle."* Reuse value decides the boundary.
- **Enforce:**
  - Mechanical aids for review:
    - flag a function that both holds its own data logic and calls two or more other steps;
    - flag a docstring or comment that lists sequential steps inside one function;
    - the architect reviews the step list in the hand-in.
    - flag a new function named for, or holding constants of, its single caller, or with exactly one caller, for the architect's review of its generality, never for automatic refusal.
  - A module map (purpose, one behaviour or several, inputs, outputs) checked against the code.
  - Never a size limit.

### G-007 · Read, compute and write in separate modules
**first** 10-09 · **applies to** computing code
- **Incidents (1):** 10-09: writing was added at each call site, so a format change touched 98 files.
- **Enforce:** report any function that both does file I/O and computes.

### G-013 · Keep display and action apart
**first** 10-10 · **applies to** user-interface code
- **Words:** *"you're either adding or adjusting one module, not the whole damn thing"* (10-10).
- **Incidents (3):**
  - Twice, a page's main total vanished after a layout edit.
  - 11-19: reviewers read the rule as forbidding a new operation from shipping with its own display.
- **Enforce:** refuse imports from display modules into action modules; a layout contract test per page.

### G-002 · Compose; never accrete
**Absorbs** G-005 · **first** 08-21; extraction in the brief 11-19 · **applies to** all product code
- **Words:**
  - *"monolithic functions are forbidden, bespoke 'fixes' are forbidden"* (08-21).
  - *"don't make a whole bunch of bespoke stuff"* (11-11).
- **Incidents (6):**
  - 08-20/21: a web request handler held a core algorithm.
  - 08-28: *"giant monolithic blobs"*.
  - 10-12: the large modules had not shrunk in two months.
  - 11-14 to 11-16: eight scratch versions of one method.
  - 11-19, two reviewers:
    - "carve what you touch" told a worker to do the opposite of "stay inside the brief";
    - "finish inside the brief" let the work grow a module that already did several jobs.
- **Why:** big blocks shrink only if each change that touches one takes something out. So the brief, written by the architect, must carry the extraction. Since Joe's 11-19 ruling, a composing unit only wires steps together, and a worker lists the steps of any new, widened or wrapped unit in its hand-in.
- **Enforce:**
  - A list of several-job modules that may only shrink.
  - A change that adds a job to an existing module fails unless it moves that job out.
  - The architect refuses a brief without the extraction.
- **Incident, sub-point 2:** 11-19, MPN repository: the dataset compile driver was split into four stage modules, each called only by the driver and each still holding its logic; by G-001 sub-point 4 that is a monolith cast to pieces.

### G-003 · One behaviour, one owner
**first** 10-05; verification by reading 11-19 · **applies to** all code, exploration included
- **Words:**
  - *"If we had a parquet writer module, this change would be to change that module and we'd be done b/c everyone used it."* (10-09).
  - *"you have pretended to learn that lesson many times"* (10-10).
- **Incidents (9):**
  - 10-05: a second reader found none of its records.
  - 10-09: one file reader was built at 20 sites.
  - 10-10, three times: an existing design was rebuilt.
  - 11-16: four builds duplicated existing operations.
  - 11-19: reviewers found the worker told both to "count copies" and "never search", and found that partial reads of long files miss callers.
  - 11-19: "the file or the function" let a worker read only the function; the rule now says the whole file, read to its end.
  - 11-19, behaviour test (draft 3): given a plain request to rename a parameter across a small package, an agent changed nothing. It read the brief-only mechanics (a caller list, no whole-codebase search, a selector) as binding without a brief. The rule now states when they apply.
- **Why:** with one owner, a change is one edit. The architect surveys the code, and the worker verifies by reading the owner in full, so neither does the other's job.
- **Incident, sub-point 3 (1):** 11-19, cross-repository review: "the only search you make" contradicted sub-point 2 for a direct request, where you count the copies yourself; Example 2's inline copy would not be found by the owner's name.
- **Enforce:**
  - A map with one owner per behaviour; a duplicate owner fails.
  - Each brief names the owner and its count of copies, and the hand-in confirms both.
- **Words, sub-point 5:** *"One reader, one writer, one structured object"* (10-05); *"Each step has a settings object that cannot drift and one reader and one writer."* (10-16).
- **Incidents, sub-point 5:** 10-05, a second reader of a stored fact found none of its records; 10-09, a loose metadata dictionary was read by key at 26 sites (microscopy).

### G-049 · Keep one map of the library
**first** 10-09 · **applies to** every module
- **Words:**
  - *"If we had a parquet writer module, this change would be to change that module and we'd be done b/c everyone used it."* (10-09).
  - *"the ask for modularity tied to testing and a function library to allow more streamlined testing of "what was touched" and maintenance of that library/tree to make sure new functions or updated functions are correct"* (11-19, naming this as general engineering).
- **Incidents (3):**
  - 10-09: one write format was spread over 12 files, so a one-module change became a 98-file cutover.
  - 11-19, microscopy census: 299 of 780 mapped modules declared no inputs or outputs.
  - 11-19, MPN repository: with no module map, the selector chose 592 of 631 test files for a change to one compile module.
- **Enforce:**
  - The gate regenerates the import edges, and they must match the map.
  - A touched module that declares no inputs or outputs fails.

### G-004 · A second path is a defect
**first** 10-07 · **applies to** all code
- **Words:**
  - *"parallel paths should not be possible without approval at the highest levels … this MUST BE a conscious and reasoned decision"* (10-07).
  - *"No legacy structures or second paths"* (10-31).
  - *"Please be sure you are not inventing parallel paths for things we already have steps for"* (11-16).
  - On the 10-07 words, which allow approval: *"the key is to have the agent need to justify a parallel path to actually convince itself that a parallel path is necessary and then to seek approval. Not just seek approval but do the work beforehand (cold reader or red-team or higher reasoning etc)"* (11-19).
- **Incidents (7):**
  - 10-07: one calculation had three implementations.
  - 10-07: "parallel paths with a sunset" were offered for approval.
  - Further second paths on 10-05, 10-09, 10-31, 11-11 and 11-16.
  - 11-19, cross-repository review: the rule said "never kept by approval" while the 10-07 words allow approval at the highest level; Joe ruled that approval is possible, after the agent has justified the path and had the case reviewed.
- **Enforce:**
  - Each known second path is a debt with an open removal task, and fails when the task closes.
  - A scan for identical function bodies.
- **Incident, sub-point 5:** 11-19, MPN repository: a build read from its cache recorded different source-read counts from a rebuild of the same code, so the cached record was not the one a rebuild writes.

### G-006 · Remove the possibility, one layer up
**Absorbs** G-008, G-009, G-011 · **first** 08-21 · **applies to** all design
- **Words:**
  - *"nothing should be run by order alone. we have signatures for a reason."* (08-21).
  - *"why do we need the history at all to start training? … a true primitive"* (10-21).
  - *"it should be possible to wrap our objects. What we don't want is parallel paths"* (10-16).
  - *"a single reader function that then employs different raw file readers"* (10-09).
- **Incidents (7):**
  - 14 callers each handled data-chunk overlap.
  - Reordering two lines switched off a validation.
  - 10-21: a primitive carried history it did not need.
  - 10-31: four builds were spent chasing a "universal" guard.
  - A backend was named in general code.
  - Platform checks were scattered outside one function.
  - Helper layers were built before any reuse.
- **Enforce:**
  - Refuse direct construction of a format reader outside its dispatcher.
  - Refuse backend names in general code.
  - Otherwise `judgment: architect`.

### G-016 · Never guard behaviour with a list of names
**first** 09-09; ruling 11-01; restored as its own rule 11-19 · **applies to** guards, validators, tests
- **Words:**
  - *"I don't like your approach of excluding function names to change behavior. This should be contracted."* and *"This is just lazy wallpapering over a defect"* (11-01).
  - *"not refused by name but refused by contract"* (10-23).
  - *"rejecting by name keeps the path alive (by name)"* (09-09).
- **Incidents (4):**
  - 09-09, 10-23 and 11-01: guards refused retired names.
  - 11-19, behaviour test: the "nobody calls the old function again" trap fell in 2 of 3 draft-2 runs. Both failed runs wrote a name search *as their witness*, because G-023 then demanded a witness that fails on the base. The cause was G-023, not this rule's place on the page; draft 4 fixes G-023 (sub-points 2 and 4).
- **Why:** a name list guards one spelling of a defect. A check whose subject is the words themselves (shared code names no study) tests a vocabulary contract, not behaviour, and is allowed.
- **Enforce:** list every guard whose subject is a list of retired names, as a debt that may only shrink.
- **Incident, debts:** 11-19, census: four live name-list guards in the microscopy repository; in MPN, an outcome-name scan with an acknowledgement list, and a function-length test with a name allowlist.

### G-010 · Portable and one-way
**Absorbs** G-034, G-035 · **first** 08-04 · **applies to** product code and tools
- **Words:** *"the repo shouldn't know anything about Mac. It's just locations"* (10-31).
- **Incidents (6):**
  - 08-04: 16 scripts with one hard-coded storage path broke when the storage moved.
  - 10-07: dependencies pointed the wrong way.
  - A cache folder defaulted to a home directory.
  - A dependency ceiling blocked an install.
  - The core imported display code.
  - A product module imported a script.
- **Enforce:**
  - Derive the import graph from the code.
  - Scan for absolute paths and host names.
  - Import the core with no display.
  - Refuse product imports from scripts, and refuse upper bounds that name no breakage.

### G-014 · Check at every boundary
**Absorbs** G-021 · **first** n.r. · **applies to** every path that reads, stores or replaces data
- **Incidents (5):**
  - Six hand-drawn annotations were destroyed while every test passed.
  - An all-default contract validated anything.
  - Schema bytes changed with a library version.
  - Refusals were reworded on the way to the person.
  - A bad file from another program fitted neither kind of refusal.
- **Enforce:**
  - An all-default contract raises.
  - Each storing path has a wrong-contract test.
  - Committed schemas are compared on every run.
  - A known refusal is one sentence.
- **Incidents, sub-points 4 and 5:** pass-only tests left boundaries unproved (microscopy, R-012); the MPN contract requires warning, stale and degraded states to be preserved as themselves, because normalising one to success hid failures.

### G-015 · Forward only
**first** n.r.; callers in the brief 11-19 · **applies to** code and stored records
- **Words:**
  - *"of course no"* (10-21, asked whether to keep compatibility).
  - *"not requiring backwards compatibility shims"* (10-23).
  - *"we don't need to accrete outdated detritus"* (11-05).
- **Incidents (6):**
  - 09-09, 10-21 and 10-23: compatibility kept.
  - 10-31: an old record kept beside its replacement hid frozen settings.
  - 11-05: superseded files kept.
  - 11-19: reviewers found that "list callers outside the brief" left callers broken.
- **Enforce:**
  - One converter per stored format, with a test.
  - Unknown fields are refused.
  - The gate's protocol is the one exception (C-015).

### G-018 · Shared code is generic
**first** n.r. (founding) · **applies to** shared code, its defaults, strings and views
- **Words:**
  - *"how would a generalizable repo understand these groupings"* (10-09).
  - *"We've gone over this 1,000 times"* (11-11).
- **Incidents (6):** 10-09, 11-02, 11-06, 11-11 (twice), 11-18.
- **Enforce:** one list of every project's own words, refused in shared code and its strings. This is a vocabulary check (G-016's *Why*).

### G-019 · The person decides
**Absorbs** G-022 · **first** 09-10 · **applies to** design, settings, reports, surfaces
- **Words:**
  - *"you are trying to do science again"* (09-13).
  - *"There is no absolute refusal"* (11-08).
  - *"you've vomited command line to me"* (11-05).
- **Incidents (15):**
  - 09-10, 09-13, 10-07 (twice), 10-08 (four times), 10-15, 10-23, 11-02 and 11-11: an agent chose a domain answer.
  - 11-05: all seven reviewed items were command packets.
  - 11-19: a draft repository rule made normalization law ("never per tile … drives both the display … a tile is never its own normalization authority"), carried in from earlier GUI rulings. Joe: *"you are making science decisions again with #2. Normalization is a science decision. when, how, it is done is up to the scientist. the repo just makes options available."* Sub-point 4 was added: citing a ruling does not make a science choice a rule.
- **Enforce:**
  - Domain settings have no default.
  - A task states its human surface.
  - Design talk: `judgment: architect, then Joe`.

### G-020 · No hidden defaults
**Absorbs** G-012 · **first** 08-27 · **applies to** every value code runs with
- **Words:**
  - *"it is ok to have defaults. it is not ok to hardwire things and worse to have invisible defaults"* (08-27).
  - *"No hidden defaults"* (11-05).
  - *"Each step has a settings object that cannot drift and one reader and one writer."* (10-16).
- **Incidents (11):**
  - 08-27, 09-24 and 10-10.
  - 09-17: a field added later had no declared meaning for its absence.
  - 10-15: a setting was chosen silently.
  - 10-19: a day of training was lost.
  - 10-21: module constants ran unseen.
  - 11-05.
  - A dictionary was read by key at 26 sites.
  - 11-19: two readers asked what to do when unsure whether a value is domain or technical.
- **Why:** "one writer, one reader" means one module builds the object from storage and one stores it; every other module receives the typed object.
- **Enforce:**
  - Every value a registered operation runs with is declared or read from the data.
  - Refuse module constants on an execution path.
  - Refuse by-key reads outside the owner.

### G-045 · No secrets in the open
**first** 11-19 (architect's ruling, on a red-team finding) · **applies to** code, logs, briefs, reports
- **Incidents (0):** none recorded. The rule is preventive; a repository holds storage credentials.
- **Enforce:** a secret scanner over committed files and logs.
- **Why, tools that run document text:** a document is untrusted input to such a tool; the MPN contract requires an allowlist, a read-only tool and stopping its whole process group on timeout, because killing the shell left its children running.

### G-017 · Fix the cause in its owner
**first** 08-21; escapes listed 11-19 · **applies to** all code and tests
- **Words:** *"bespoke 'fixes' are forbidden"* (08-21). *"The rounds concept has to be removed, not just papered over and renamed"* (11-01).
- **Incidents (6):**
  - 10-23 and 11-01: a concept was renamed to clear a finding.
  - 11-19: reviewers found five escapes that nothing catches:
    - a broad except;
    - skip, or a raised ceiling;
    - a bypassed hook;
    - suppressions;
    - placeholders.
  - 11-19: two readers could not tell an early failure from a guard.
  - 11-19, round 4: a reviewer found the list too categorical. A bounded retry of a transient external service, or a documented clamp of an input domain, can be the boundary's declared contract. It is banned only as a way to make a failure go away.
- **Why:** the owner's boundary check is part of its contract. Anywhere else, a check hides the cause.
- **Enforce:** `judgment: architect` until a diff report flags each escape for review.

### G-023 · A witness for every change
**Absorbs** G-031 · **first** n.r. · **applies to** every change
- **Words:** *"don't waste time doing tests that are pointless"* (09-17).
- **Incidents (7):**
  - Tests that could only pass.
  - A check compared against code it shared.
  - A fix's test was never run without the fix.
  - 11-19: a "failure" on the base was only an import error.
  - 11-19: readers asked what witnesses a rename.
  - 11-19, behaviour test and all four round-3 reviewers: "must fail on the base" pushed agents to write a name search as the witness for a removal (G-016). A change that keeps behaviour is witnessed by its contract, which passes on both trees.
  - 11-19, round 4: a witness for a new entry point can fail on the base only by naming the missing name. Excluding that error left a presence check as the only route, so such an error now counts when it names what the change adds.
- **Enforce:**
  - One command, with `--kind adds` or `--kind preserves`, runs the witness on the base and the tip. It records `WITHOUT:` and `WITH:`, or `BASE:` and `TIP:`. For `--kind adds`, an import or attribute error counts only for a name the tip adds.
  - A hand-in check refuses a hand-in without that record.

### G-046 · Never weaken a test to make it pass
**first** n.r.; own rule 11-19 · **applies to** tests
- **Incidents (2):**
  - Tests were loosened to go green.
  - 11-19: readers could not tell an updated expected answer from a weakened one.
- **Enforce:** a diff report flags loosened tolerances, skips and changed expected values, for review against the brief.

### G-044 · Test with the real parts
**Absorbs** G-029 · **first** 11-19 · **applies to** tests
- **Incidents (3):**
  - Two tested units disagreed at their join.
  - A journey was never run end to end before the hand-in.
  - A mocked owner proved only the call order.
- **Enforce:** report test doubles that replace a registered owner module.

### G-024 · Real data is out of bounds
**first** n.r.; one definition 11-19 · **applies to** tests, workers, architects
- **Words:** *"we don't need to accrete outdated detritus"* (11-05, on deleting superseded records after conversion).
- **Incidents (6):**
  - 10-31: a rehearsal pointed at live data was saved only by a crash.
  - A test server could reach the live store.
  - A tool runner silently set the live data location.
  - 10-08: a computation waited on a write approval.
  - 11-19, two rounds: the reviewers found the right to read, the right to write, and what counts as real data each stated several ways.
- **Why:** real data is the one thing that cannot be regenerated, and a copy carries the same risk.
- **Enforce:**
  - A test fixture fails when the data-location variable names a real folder.
  - Sub-point 4: a commit hook refuses staged data files; reports and logs give counts, not rows (`judgment: architect` for text).
- **Why, sub-point 4:** in a project with patient data, a quoted log line can carry an identifier or a date, so the glossary's log-excerpt exception cannot hold there; and an ignored file is still synced and pushed by tools that do not read the ignore list.

### G-025 · Run what you touched, and say what ran
**Absorbs** G-026, G-030 · **first** 08-04; focused runs 11-01 · **applies to** every result reported
- **Words:**
  - *"do not re-test it for every change … run the full suite once a logical refactor group is complete. that is just good engineering."* (10-07).
  - *"you are very drift prone and call done things that are unusable for a human"* (11-02).
- **Incidents (12):**
  - 10-07: a one-word change cost a 30-minute full run.
  - 11-02: builders' runs held the gate for hours.
  - 11-15: five gates turned red from runs beside them.
  - A misread measurement produced a false hypothesis.
  - A rejected push printed success.
  - A remote copy was 453 commits behind.
  - Shell surprises:
    - a failed filename pattern aborted a command;
    - a process search matched itself;
    - a tool runner overrode variables.
- **Enforce:**
  - The selector is shared with the gate.
  - The worker's check refuses a whole-suite plan.
  - Cited lines and commits resolve.

### G-027 · A check must be able to fail
**Absorbs** G-028, G-033 · **first** 09-09 · **applies to** tests, gates, scripts
- **Incidents (12):**
  - Six gates shipped with no browser coverage.
  - Red code was pushed through a pipe.
  - A forgiving parser hid defects.
  - 10-31: a guard meant to catch everything.
  - The main line was red for ten days for anyone with one optional package.
  - Gates failed on a sleeping machine, during training, and on a full disk.
- **Enforce:**
  - Shell scripts set `pipefail`.
  - A gate prints every leg and counts skips.
  - Each guard declares its blind spots.

### G-032 · Wait on events
**first** n.r.; own rule again 11-19 · **applies to** tests and agents
- **Incidents (3):**
  - Fixed waits failed under load.
  - 10-30: an agent waited five hours with nothing watching.
  - 11-19: readers read "a heartbeat timeout" as jargon.
- **Enforce:** refuse fixed sleeps in tests.

### G-036 · Stop on a false premise
**first** 09-04; partial hand-ins 11-19 · **applies to** every worker
- **Incidents (10):**
  - Dozens of hand-ins changed files outside their brief (16 on 11-02).
  - 11-19: readers could not tell what "pull apart" means, whether a refused command is a stop, or whether to finish the unblocked parts first.
  - 11-19, behaviour test (draft 4): an agent asked to stop a function being called stopped and asked, although moving its two callers was plainly part of the request. A stop is now limited to a real contradiction, a domain choice or work outside the request.
- **Enforce:**
  - The hand-in check compares the changed files with the brief.
  - Otherwise `judgment: architect`.

### G-047 · Hand in once
**first** n.r.; moved from the operating model 11-19 · **applies to** every worker
- **Incidents (5):**
  - Five hand-ins lacked their key.
  - 11-19: the stop procedure sat outside the worker's reading list.
  - 11-18, MPN repository: long returns resent as context fed a 60%-in-12-hours worker usage burn; the project then capped briefs and hand-ins at 20 lines (see C-003).
- **Enforce:** a hand-in template check.

### G-037 · Keep history safe
**first** n.r. · **applies to** version control, running scripts
- **Incidents (9):**
  - Bulk adds committed unrelated files.
  - Rebased merges lost records.
  - Scripts were edited while running (10-03, 10-09, 11-08).
  - 09-18, MPN repository: a commit that failed on a ref-lock race still landed, carrying another agent's staged files under the wrong message.
  - 07-27, MPN repository: agents in separate worktrees shared one stash stack, so one agent's stash could be popped by another.
- **Enforce:** a push hook refuses rewritten history. Sub-point 4: `judgment: architect` at review of the commit list.

### G-038 · Documents are true, single and current
**Absorbs** G-039, G-040, G-041 · **first** 08-16 · **applies to** documents
- **Words:**
  - *"your memory is frail"* (08-22).
  - *"drifty, multiple wordy descriptions"* (09-13).
- **Incidents (12):**
  - Superseded text was read as current.
  - The plan was renumbered three times in a day.
  - Restated laws drifted apart.
  - Docs-only edits turned the main line red (10-01, 10-02, 10-03, 10-08, 11-05).
  - 11-13: typed times ran ahead of the clock.
  - 11-19: the principles stated their own rule count as a number.
- **Enforce:**
  - Citations resolve.
  - A document change runs the tests that read it.
  - An entry's time may not be later than its commit.
- **Incident, governing document:** 11-19: the operating model let only the architect change a governing document while G-038 sub-point 3 told the worker to update documents in the same change; the term had no definition.

### G-042 · Corrections become checks
**Absorbs** G-043 · **first** 11-19 · **applies to** registers, checks, agent memory
- **Words:** a principle Joe adopted on 11-19 (not his wording): *"Agents repeat mistakes because nothing enforces a line in a text file. If you correct something twice, add a check. Run each check only on the files it's about, and put the reason in the error."*
- **Incidents (4):**
  - 43 of 139 rules had no check.
  - The two most-corrected rules had none.
  - A note held nine appended "again" paragraphs.
  - 16 of 23 rulings had no date.
- **Enforce:**
  - A register guard requires unique ids.
  - Each check exists and prints its id.
  - A retired entry names its replacement.
- **Incident, sub-point 4:** 11-19: the microscopy repository defined these four words for its own register while MPN used none; one vocabulary lets a reader compare registers.

### G-048 · General rules here; project rules in the project
**first** 11-19 · **applies to** these pages and every project's rules page
- **Words:**
  - *"What you proposed is a mixture of general design philosophy (avoidance of parallel paths and papering over defects instead of fixing them etc) and repo specific (targets not channels, physical units not px, generic not study biology etc...). I think we want to develop those separately. One to be used and refined over time for all of our work across projects and one for the individual repos"* (11-19).
  - *"I think such a repo should be only for general engineering. not the imaging or ML specific rules. those belong to the repo BUT we should have general rules about the need for such guidance and what goes in such repo-specific guidance. if it is generalizable engineering principle then it belongs in agent-guidance not the repo-specific guidance"* (11-19).
- **Incidents (2):**
  - 11-19: the first draft mixed the general rules with one repository's rules.
  - 11-19: the general register cited one repository's task number as its check (G-023), and was corrected when the pages became their own repository.
- **Why:** one general set can be refined across every project only if it holds nothing project-specific; a project's page stays short only if it never restates a general rule.
- **Enforce:**
  - The stamped copy carries the source commit, and a check flags a copy that differs from that commit or is behind the source.
  - A vocabulary check of these pages against each project's own words (G-016's *Why* allows a vocabulary check).
  - Otherwise `judgment: architect`.

## Retired G ids (never reused)

| Retired | Now in |
|---|---|
| G-005 | G-002 |
| G-008, G-009, G-011 | G-006 |
| G-012 | G-020 |
| G-021 | G-014 |
| G-022 | G-019 |
| G-026, G-030 | G-025 |
| G-028, G-033 | G-027 |
| G-029 | G-044 |
| G-031 | G-023 |
| G-034, G-035 | G-010 |
| G-039, G-040, G-041 | G-038 |
| G-043 | G-042 |

Draft 2 retired six more ids, which this draft restores with their original meaning: G-004, G-007, G-013, G-016, G-032 and G-036.

## Coordination rules (C, general)

The rule text is in [OPERATING_MODEL.md](OPERATING_MODEL.md).

| Id | First | Joe's words · incidents (count) | Enforce |
|---|---|---|---|
| C-001 | 11-02 | *"you are working and have no subagents working. this is not architect behavior. this is subcontractor behavior"*. Five unblocked tasks waited (1). | judgment: Joe |
| C-002 | 11-19 | Codex use was *"largely being wasted on large memory reading for the workers"*. Onboarding took a third or more of a session; the budget then left out the owner's code (3). | a brief template check |
| C-003 | 09-04 | Five umbrella tasks fell before any code. Briefs lacked owners, human surfaces, task ids or folders (7). Line cap: *"We need to remove the message bloat. that is unsustainable."* (11-18, MPN repository, relayed by its GUI architect); the same day, long orders resent as context drove a worker account through 60% of its usage in 12 hours (1). | brief template check |
| C-005 | 09-12 | A commit landed on the wrong branch. A helper building in the architect's copy reset its branch (5). | a checkout hook |
| C-008 | 09-24 | *"your comlink sucks"* (11-06); *"every couple hours is plenty"* (10-15); *"codex was waiting on you ... you must fix this"* (11-07). Idle turns of 5–10 h (9). | judgment: architect |
| C-010 | 10-07 | A relayed decision acted on, twice; a void grant; a task opened on a relay (4). | judgment: architect |
| C-012 | 11-19 | 16 candidates reached the gate outside their brief (2). | judgment: architect or cold reader |
| C-015 | 10-03 | A gate change gated itself. One turned every gate red (2). | a gate-touching change runs under both harnesses |
| C-017 | 09-04 | Umbrella tasks fell. A later slice was stranded under a closed task (5). | task ids never reused |
| C-018 | n.r. | Tasks opened without review fell to reviewers (n.r.). | judgment: architects |
| C-019 | n.r. | Tasks retried as they were (n.r.). | judgment: architect |
| C-021 | 10-21 | A repeating night wake; gates ran on a sleeping machine (2). | judgment: architect |
| C-022 | 11-10 | *"The goal is to use both to their max but to not run out of usage before refresh (or only for a few hours or so). we "can't take it with us" so we need to spend while we can"*. Accounts compared by totals; routing reversed four times. Routing decided 11-19 from his rulings (6). | judgment: architect |
| C-023 | 11-02 | *"you are very drift prone and call done things that are unusable for a human"*. Seven items not right (3). | a verdict file Joe writes |
| C-024 | 09-13 | *"we've reviewed this many times"*; *"I already answered"*; *"full context, recommendation … contingencies"*; *"I always need questions prioritized, one at a time, with full context, a possible recommendation with consequences and contingencies."* (11-19) (6). | judgment: architect |
| C-025 | 07-29 | *"that non-action cost me a day"* (4). | judgment: architect |
| C-026 | 09-14 | An approved action was asked again; a dictated message was misread (2). | judgment: architect |
| C-027 | 09-28 | Another lane's traffic was relayed to Joe (1). | judgment: architect |
| C-028 | 11-05 | *"a workable draft is probably draft 5-10"*; *"stop talking about more donors"* (11-13). Pictures sent without independent readers; scaling offered before validation (3). | judgment: architect |

**Retired C ids:** C-011 is now G-047, C-020 is now C-008, and C-029 is now G-036.

**Moved to the repository's runbook:** C-004, C-006, C-007, C-009, C-013, C-014 and C-016.
