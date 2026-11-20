# Decisions: the science register

The record behind [SCIENCE_PRINCIPLES.md](SCIENCE_PRINCIPLES.md) (the S rules), in the same form as the general register (`DECISIONS.md`): Joe's words, the incidents, the reason and the check. Ids are never reused. All dates are 2026.

**Why this set exists (11-19).** Joe ruled that *"rules like 'don't make scientific decisions' belong to the data-science / analysis domain, not to general engineering"* (recorded by a project's architect when it withdrew a proposed general rule, commit 8631adc), and chose a shared, opt-in science set over keeping science rules in each repository, so the science projects do not drift apart. S-001 holds what was G-019 sub-points 2 and 4.

### S-001 · Science choices are the scientist's
**first** 09-10 (as part of G-019); its own set 11-19 · **applies to** design, settings, reports, briefs
- **Words:**
  - *"you are trying to do science again"* (09-13).
  - *"Normalization is a science decision. when, how, it is done is up to the scientist. the repo just makes options available."* (11-19).
  - *"normalization of a tile vs training a model using a per tile normalized signal are not the same things. But in both settings I do think they are science decisions and should be explicitly chosen without hidden defaults"* (11-19).
- **Incidents (14):**
  - 09-10, 09-13, 10-07 (twice), 10-08 (four times), 10-15, 10-23, 11-02 and 11-11: an agent chose a domain answer.
  - 11-19: a draft repository rule made normalization law ("never per tile … a tile is never its own normalization authority"), carried in from earlier interface rulings. Sub-point 3 was added: citing a ruling does not make a science choice a rule.
  - 11-19: a question to Joe merged two different science choices (how a tile is shown, and how a model's input is normalized) into one.
- **Why:** an agent that picks a threshold or a normalization changes what a result means, and nobody can see that it did.
- **Enforce:**
  - Science settings have no default.
  - Design talk: `judgment: architect, then Joe`.

### S-002 · Where science has one answer, the software enforces it
**first** 08-10 (one project); shared 11-19 · **applies to** selection, splits, evaluation, recorded values
- **Words:** *"this is not a user option. it is bad science. the repo must enforce doing good science."* (08-10, ruling in one project that selecting on test-set metrics stays banned).
- **Incidents (1):** 11-19, cross-repository review: S-001 alone read as letting a person declare a leaky split, and a project rule ("never forbids one") contradicted that project's own held-out-split checks.
- **Why:** an output labelled "held-out" or "measured" that is not is false, whatever anyone declared. Naming the label keeps the rule from growing into a general refusal of choices (S-001).
- **Enforce:** each enforcement names the label it keeps true, in its refusal.
