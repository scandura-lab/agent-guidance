# Science Principles

Joe Scandura's rules for AI agents on projects that do science or data analysis, version 2026-11-19.
- They add to the general engineering rules (`ENGINEERING_PRINCIPLES.md`), which every project carries. A project that does science carries this page too (G-048).
- The reasons and history for each id are in `SCIENCE_DECISIONS.md`, which travels with this page; it is for architects.
- A project's own rules refine these by id and never restate them. A rule about one project's science (its stains, organisms, instruments or models) stays in that project.

## The scientist decides

- **S-001 Science choices are the scientist's.**
  1. Never choose a science answer: what to measure, a threshold, an exclusion, a model, a normalization, a training or held-out split, the unit of analysis. Each is a choice the scientist declares. The software offers the options, records the choice with the result and reports its consequences (G-019 sub-point 1).
  2. A science choice has no hidden default (G-020 sub-point 3). The software may recommend a value, and may apply it when the scientist states none, only if every output and record marks it "default nobody chose" (G-020 sub-point 1). It shows what helps the choice, for example an elbow plot beside a PCA setting. Requiring a statement is allowed, never required. If you are unsure whether a value is science or technical, treat it as science (G-020 sub-point 4).
  3. Citing an earlier ruling does not make a science choice into a rule. Check whether it is science first. If it is, it stays a declared choice.
- **S-002 Where science has one answer, the software enforces it.**
  1. A practice that would make an output's own ***labels*** false is refused, never offered as an option: test data steering a selection, one subject on both sides of a held-out split, a fabricated value indistinguishable from a measured one.
  2. Each enforcement names, in its refusal, the label it keeps true. A practice for which no such label can be named is not enforced; it is a declared choice (S-001).

## Words used here

- **Label:** what an output says about itself, for example "held-out", "measured" or "test score". S-002 keeps such words true.
- **Science choice:** a choice whose answer changes what a result means, as opposed to how fast or where it is computed.

*End of the science principles.*
