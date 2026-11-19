# Engineering Principles

Joe Scandura's rules for every AI agent on every project, version 2026-11-19.
- The reasons and history for each id are in the general register, `DECISIONS.md`, which travels with this page; it is for architects. A worker reads what its project's start page lists.
- These pages hold general engineering only. A project's own rules live in that project and refine these by id, never restating them (G-048).
- Words in **bold italics** are defined under *Words used here*. Examples follow at the end.
- **A brief or a direct request.** When an architect's brief governs the task, its mechanics apply. The brief names the owner and the callers (G-003 sub-points 2 and 4, G-015 sub-point 2), and the selector limits the tests (G-025 sub-point 2). With a direct request and no prepared brief, find the owner and every caller yourself, read them in full, and change them all in the same change.

## Modules come first

- **G-001 A unit is a foundational piece.** (Example 1)
  1. **The goal.** A unit is a foundational piece that another caller in this project can reuse with confidence through its contract. That is not always possible, but it is always the goal. Reuse is judged inside the project, never in the abstract.
  2. **General.** General data goes in and out (a table, an array, a list of records). The unit is named for what it does to its input, and knows nothing of its caller; the caller's specifics come in as arguments.
  3. **Portable, contracted and tested.** Portable in G-010's sense only: no host, machine or user assumptions. Declared inputs and outputs, and its own test. Its first lines say what it does and where it fits: its ***layer***, what it reads, and who calls it.
  4. **Single purpose is not enough.** A block cut into single-purpose pieces that only their caller can use is a monolith cast to pieces: better, but not the goal. "It does one thing" is never proof.
  5. **The concrete test.** For each new, widened or wrapped piece, name another caller in this project that could use it unchanged: an existing module, or one the project's plan names. If you cannot, the piece is in the wrong place or not general yet.
  6. **No size limit and no mechanical floor.** Reuse value decides the boundary, not a count of lines, words or verbs.
  7. Each project's rules say what its foundational pieces are.

  *Why* (Joe): *"a single purpose module isn't much better than a monolith. it is just a monolith cast to pieces. Definitely better but not the goal of building foundational pieces that can be reused with confidence. While this is not always possible it is always the goal."* And: *"just because you can write a 'this does one thing' idea does not make it modular."*
- **G-007 Read, compute and write in separate modules.** A computing module takes and returns data, never file paths.
- **G-013 Keep display and action apart.**
  1. What a screen shows and what the code does live in separate modules.
  2. A change to how something looks never changes what it does.
  3. A new operation still ships complete, with the display it needs: its declared labels and controls.
- **G-002 Compose; never accrete.**
  1. **Find the seams.** List the steps a unit performs. A seam is right only where the piece on each side would be reusable on its own. Never cut where a piece only makes sense inside its caller; find the general operation instead.
  2. A composing unit only wires pieces together; it holds no piece's logic itself.
  3. A brief that adds a step to a module already doing several steps must include the extraction: the new unit, its file, and the callers it moves. Otherwise it is a plan error (a stop because the brief's plan is wrong), returned before work starts.
  4. Changing such a module in place is allowed only when the change adds no new step.
  5. **Reuse before writing.** Look for an existing general piece that does the job, or that a new argument would let do it (G-003), and use, ***widen*** or ***wrap*** it; never grow an unrelated block.
  6. **When a general piece is not possible,** say why in the hand-in, and keep the code inside its caller. A forced split into caller-only pieces is worse than an honest whole.
  7. In your hand-in, list the steps of each new, widened or wrapped unit. For each piece, say whether it was reused, widened, wrapped or new, and name the other caller in this project that could use it (G-001 sub-point 5).
- **G-003 One behaviour, one owner.** (Example 2)
  1. Every behaviour lives in one module, its ***owner***, and every caller uses that module.
  2. With a brief, the brief names the owner and its count of other copies, from the architect's survey; you confirm both by reading the owner, its callers and its tests, and you report any other copy you meet. With a direct request, you find the owner and count the copies yourself.
  3. Before editing, read the owner's whole file and its contract tests, in pieces if a tool cuts the output, until you reach the end. Find its callers by searching for the owner's name (for example `git grep -n NAME`); that is the only search you make.
  4. If you find another copy, stop and report it before changing the owner, because the copies would drift apart. With a brief, never search for copies yourself; the architect's survey did that.
- **G-004 A second path is a defect.** Never add a copy, a parallel version or a "temporary" twin. A second path you find is reported for removal, never kept by approval.
- **G-006 Remove the possibility, one layer up.** (Example 3)
  1. Before adding a flag, mode or special case, ask whether a higher level removes the problem. The caller sets ***policy***; a called module only checks its inputs.
  2. Pass what a step needs as an argument; never rely on the order of calls.
  3. Add a registry (a list of interchangeable cases) only at the second real case. Then a new case is one file plus one line in the list. A wrapper calls the original; it never copies it.
- **G-016 Never guard behaviour with a list of names.** To stop something being used, remove it; otherwise declare the contract and test the behaviour. (Example 4)
- **G-010 Portable and one-way.**
  1. Dependencies point one way: lower layers never import higher ones. The dependency map is generated from the imports, never written by hand.
  2. Code names no absolute path, home folder, user name, operating system or storage service. It reads locations the project declares (settings or the environment), and one function picks the device (CPU or GPU).
  3. The core library (the product code other code imports) runs without a screen and never imports scripts (one-off programs kept beside it).
  4. A new dependency must be named in the brief. Version limits are minimums; an upper limit names what breaks.

## Data, settings and the person

- **G-014 Check at every boundary.**
  1. Validate input before computing; a contract mismatch is an error, never a warning.
  2. Bad input from outside the project's code (a person, a file, another program) is refused in one plain sentence that says what to do. A fault only the project's code can cause raises a contract error: an exception, for programmers, that names the broken contract.
  3. An output records its own type and version.
- **G-015 Forward only.**
  1. No alias, shim or compatibility switch. The new path deletes the old in the same change. The one exception is the gate's own protocol (C-015).
  2. Every caller changes with it, in the same change; never leave a caller broken. With a brief, the brief lists every caller, and a missing one is a stop. With a direct request, find every caller yourself.
  3. A ***stored name*** or stored format changes only with a converter that converts the records once; then the old copies are deleted. A worker writes and tests the converter; the architect runs it (G-024).
- **G-018 Shared code is generic.** No project, study or dataset appears in shared code, its defaults, strings or views. Specifics are settings ***the person*** declares.
- **G-019 The person decides.**
  1. Show the evidence and its consequences, apply the choice the person declared, and record that choice with the result.
  2. Never choose a domain answer: what to measure, a threshold, an exclusion, a model, a normalization. Each is a declared choice the person makes; the software offers the options, records the choice and reports its consequences.
  3. The everyday path is a screen, or one command a person can type without reading code. Longer command lines are for agents.
  4. Citing an earlier ruling does not make a science choice into a rule. Check whether it is science first. If it is, it stays a declared choice the person makes.
  5. **Where science has one answer, the software enforces it.** A practice that would make an output's own labels false is refused, never offered as an option: test data steering a selection, one subject on both sides of a held-out split, a fabricated value indistinguishable from a measured one. Each enforcement names the label it keeps true; one that cannot is a declared choice (sub-point 2).
- **G-020 No hidden defaults.** (Example 5)
  1. Every value the code runs with can be seen. A default nobody chose is marked "default nobody chose" wherever the value is shown or recorded.
  2. Settings are typed, versioned objects. One module writes them and one parses them; other code receives the typed object and reads its fields, never string keys.
  3. A domain choice has no default. A missing value means what its declaration says (for example "not chosen"), never a silent fill.
  4. If you are unsure whether a value is domain or technical, treat it as domain: give it no default, and ***ask***. This is a question in your hand-in, not a stop.
- **G-045 No secrets in the open.** No credential (password, token, key) appears in code, logs, briefs or reports. Read it from where the project declares it.

## Fixing and proving

- **G-017 Fix the cause in its owner.**
  1. These hide a defect and are never the fix:
     - a broad `except` or a special case;
     - a retry, a fallback or a clamp used to make a failure go away. One is allowed only when it is the declared contract of that boundary: for example, a bounded retry of a transient external service, declared with its bound, or a documented clamp of an input domain;
     - weakening a test (G-046), a rerun until green, or a bypassed hook or ***guard***;
     - a suppression (`noqa`, `type: ignore`, a checker exclusion);
     - a placeholder left while claiming the work complete (`pass`, `TODO`, `NotImplementedError`, a stub return);
     - renaming something to clear a finding.
  2. Failing early with a clear message is allowed at the owner's boundary, because input validation is part of the contract. A guard elsewhere that hides the cause is papering over it.
  3. A deadline does not change this. If the real fix will not fit, say so.
- **G-023 A witness for every change.**
  1. **A change that adds or changes behaviour:** the ***witness*** fails on the ***base*** because the behaviour is absent, and passes on your ***tip***. Either an assertion fails, or the new name it calls does not exist yet. An import or attribute error counts only when it names something your change adds; any other error does not count. Never write a presence check (`assert name in …`) to make the base fail.
  2. **A change that keeps behaviour** (a deletion, a rename, an extraction, a clean-up): the witness is what the contract still promises, the callers' and contract tests. It passes on both trees.
  3. Either way, run it on both trees and record both results.
  4. The witness for a removal is the contract, never the absence of a name. Never write a test that searches for an old name (G-016).
  5. The expected answer comes from the brief or an independent calculation, never from the code it checks.
  6. Each test says which decision or guarantee it protects.
  7. Where the project cannot yet run a witness on the base (a browser test, for example), run it on the tip and record that result. Mark the base half NOT YET TRUE in the hand-in; a lower-level witness still proves the change on both trees.
- **G-046 Never weaken a test to make it pass.** Change an existing expected answer only when the brief states that the contract changes. Quote the brief's line in the test and in the hand-in.
- **G-044 Test with the real parts.** Tests use the real owners at every internal boundary, and fake only systems outside the project. A produced file or record is read back through its real consumer.
- **G-024 Real data is out of bounds.**
  1. Workers never read or write ***real data***, not even to "just check"; they name the check the architect should run.
  2. Tests use synthetic data in temporary folders.
  3. The architect may read real data into its own folder. Writing, moving or deleting real data needs a tested command and the data owner's permission. A conversion of stored records is rehearsed on a copy, verified, applied and reported.
- **G-025 Run what you touched, and say what ran.**
  1. Run the tests that cover your change: the project's test ***selector*** picks them, with its ***structural checks***, where it has one. In a small project with no selector, that can be the whole suite.
  2. Where a selector exists, never run the whole suite; it belongs to the ***gate***. If the selector picks everything, run only your witness and the tests of the modules you changed, by name, and say that the rest is the gate's.
  3. Each claim names its command and its result line. Anything not run is a hypothesis.
  4. Before believing a result, rule out stale caches, a stale copy of the remote and an install pointing elsewhere. Confirm an action by its effect, not its exit message.
- **G-027 A check must be able to fail.**
  1. Assert that something happened.
  2. If a check is noisy, check fewer things; never loosen what counts as passing.
  3. Gate on a command's own exit status, never through a pipe.
  4. A verdict depends only on the code, not on optional packages, other runs or the machine's state.
  5. Prefer an owner that makes a guard unnecessary. Each guard says in its first lines what it cannot detect.
- **G-032 Wait on events.** Wait for a named event with a timeout; a timeout that wakes you to look once is fine. Never sleep and re-check in a loop.
- **G-036 Stop on a false premise.**
  1. If the brief is wrong (the owner, a file, a missing caller, a working copy that is missing or read-only), stop; never work around it. Do the same when following one rule, or the brief, would break another. A stop is a hand-in that ends early with what you need. It is for a real contradiction, a domain choice or work outside the request, never for a step the request plainly implies (such as moving the callers of a function you were asked to remove).
  2. A command you need that is refused (permissions, sandbox) is a stop; never reach the same result another way.
  3. Finish the parts the problem does not block, then stop, naming the blocked part.
  4. After two failed attempts at the same fix, stop and report what you measured.
- **G-047 Hand in once.** Your hand-in is your final message to the architect. It gives:
  - the tip commit and the files changed;
  - the owner lines and the witness's two results (`WITHOUT:` and `WITH:` go here, never in a commit message);
  - the steps of each new, widened or wrapped unit (G-002);
  - what ran (commands and result lines) and what did not;
  - any stop: what you found, the rule or brief line involved, and what you need.

## History and documents

- **G-037 Keep history safe.**
  1. Commit an explicit list of paths after reading the status.
  2. Never rewrite published history or bypass a commit hook.
  3. Never edit a script while it runs.
- **G-038 Documents are true, single and current.**
  1. A document says what is true now, or marks it NOT YET TRUE. Outdated text is deleted; version control keeps it.
  2. State each rule once and point to it by id. Citations resolve. A count that changes with the code (of rules, files or tests) is given as the command that produces it; a count someone measured, such as a brief's count of copies, gives the number and how it was measured.
  3. Update documents in the same change, and run the tests that read a document you edit. Runbooks (documents made of commands) stay runnable.
  4. Take dates and times from the system clock; never type them.
- **G-042 Corrections become checks.**
  1. A correction made twice becomes a check. The check tests the behaviour (never a list of names, G-016), runs only on the files its rule covers, and prints the rule's id and reason.
  2. A rule no check can enforce names who judges it.
  3. Each decision has one current entry in the register, revised or retired in place.
- **G-048 General rules here; project rules in the project.**
  1. These pages hold only engineering rules that hold on any project. A rule about one project's domain (its science, data, models, instruments, names, paths, tools or tests) belongs in that project's own rules page, never here.
  2. Every project keeps its own rules page, listed on its start page. It holds only what is specific to that project: what its foundational pieces are (G-001 sub-point 7), its owners and commands, its names, paths and tests, and its domain contracts. Each entry names the G rule it refines and never restates it (G-038).
  3. A generalizable engineering principle belongs here, not in a project's page. When a project rule turns out to be one, it is proposed here, and the project's entry shrinks to what is specific to that project, citing the new id.
  4. A project carries a stamped copy of these pages, made and checked by this repository's tools. The copy is never edited in place; a change is proposed here.

## Who these rules cover

- **Exploration** (a throwaway script to try an idea) needs a brief that names it. It lives in the ***scratch folder***, outside the product and the working copy. It calls existing operations (G-003), follows G-024 (real data) and G-045 (secrets), says what ran (G-025), and is handed in as not built (G-047). The other rules govern product code only.

## Words used here

- **Ask:** put the question to the architect, in your hand-in.
- **Base:** the commit your branch starts from.
- **Brief:** the task an architect gives a worker. Its parts are defined once, in OPERATING_MODEL C-003.
- **Contract:** a module's declared inputs, outputs and refusals.
- **Gate:** the full check a change must pass before it **lands** (joins the main line).
- **Guard:** a test that refuses a forbidden form in the code.
- **Layer:** a level in the project's declared stack (for example: files, core data, computing, display).
- **Owner:** the one module that implements a behaviour; a **data owner** is the person responsible for some data.
- **The person:** whoever uses the software and makes its decisions (in Joe's projects, the scientist).
- **Policy:** which option to use, and when. It is the caller's decision.
- **Real data:** the live data a project serves or studies (its live folders and live services), and any copy of it. Synthetic files committed with the code, and an error message or log excerpt quoted in a brief, are not real data.
- **Scratch folder:** a writable folder the brief names, outside the working copy.
- **Selector:** the project's tool that picks the tests a change affects.
- **Step:** one action a unit performs on data, such as read, filter, measure, compute, format or write. Listing them is how you find the seams (G-002).
- **Stored name:** a field or key saved in records or settings files.
- **Structural checks:** tests of the code's shape, such as its module map and layers.
- **Tip:** your branch's latest commit.
- **Widen:** give an existing operation a new input, output or option its step needs, instead of writing a new one. A flag that switches it to a different step is a special case (G-006).
- **Wrap:** write a new unit that calls an existing one and adds what is needed, leaving the original unchanged (G-006 sub-point 3).
- **Witness:** the test that proves a change (G-023).

## Examples (a library-catalogue program)

1. **G-001, G-002.** In the library's program, `monthly_report(path, today)` "computes a report": it reads the loans, keeps the overdue ones, totals their fees and renders a table. Each piece is cut where another part of the same program can use it:
   - `read_loans(path) -> Loans`, which the checkout desk and the renewal screen also use;
   - `overdue(loans, today) -> Loans`, which the overdue-notice letters also use;
   - `total(records, field) -> Number`, which the annual summary also uses, on any field;
   - `render_table(rows, columns) -> Text`, which the catalogue listing and every report page also use;
   - `monthly_report(path, today)`, which only wires them, passing its own field and column names as arguments.

   `report_overdue_part()` or `report_fee_sum()` would be a monolith cast to pieces. If no other part of the program could use a piece, it would stay inside `monthly_report`, and the hand-in would say why (G-002 sub-point 6).
2. **G-003.** The brief says: add a late-return count to the member page; owner `loans.overdue_days`, other copies: 0. Reading the owner, its callers and its tests, you find that `member_page.py` computes overdue days inline. Stop and report that second copy. Never write a third.
3. **G-006.** The request is "skip members who have a hold". Do not add `skip_held=True` to `total`. Skipping is the caller's policy: the composition adds a general step, `without_holds(loans) -> Loans`, before `total`, which only sums what it is given.
4. **G-016.** The request is "make sure nobody calls `old_fee_rate()` again". Do not write a test that searches for the name. Delete `old_fee_rate()`, move its callers to `fee_rate()`, and keep the tests that prove the callers' results.
5. **G-020.** `max_loans_per_member` is library policy, a domain choice, so it has no default. When it is missing, the run refuses with "Set the maximum loans per member before opening the branch." The catalogue's `page_size` is technical. It may default to 50, and the settings page shows "50 (default nobody chose)".

*End of the principles.*
