# agent-guidance

Joe Scandura's rules for AI agents, in layers (G-048):
- **general/**: engineering rules for every project. Every project carries them.
- **domains/science/**: rules shared by the projects that do science or data analysis (S ids). A science project opts in.
- A project's own rules (its stains, organisms, instruments, models, names, paths, tools and tests) live in that project and refine these by id.

| Path | What it is |
|---|---|
| `general/ENGINEERING_PRINCIPLES.md` | The rules (G ids), with examples. Every agent reads this. |
| `general/DECISIONS.md` | The register: Joe's words, the incidents and the reason behind each G and C id. For architects. |
| `general/OPERATING_MODEL.md` | How architects and workers organize (C ids). For architects. |
| `general/AGENTS_TEMPLATE.md` | A short start page (`AGENTS.md`) for a project, with its slots. |
| `domains/science/SCIENCE_PRINCIPLES.md` | The science rules (S ids): science choices are the scientist's; where science has one answer, the software enforces it. |
| `domains/science/SCIENCE_DECISIONS.md` | The science register: the words, incidents and reasons behind each S id. |
| `settings/` | Reference copies of each agent tool's settings, and `check_settings.sh`, which shows how this machine differs. It changes nothing; Joe approves every change. |
| `tools/stamp.py` | Puts a stamped copy of the general pages (and any opt-in set) into a project, and checks such a copy. |
| `tools/copy_check.py` | Copied, stamped, into each project folder with the pages: checks the copies using only the copies, so a project's own test can run it. |
| `tests/` | The tools' tests: `python3 -m unittest discover -s tests`. |

## Using it in a project

A project carries a stamped copy of the general pages, plus the science pages if it does science (for example in `docs/principles/`), so every agent on every machine, sandboxes included, finds them in the repository it works in. Its start page points to that copy and to the project's own rules page.

```sh
cd ~/dev/agent-guidance && git pull --ff-only && python3 tools/stamp.py into /path/to/project/docs/principles --with science
cd ~/dev/agent-guidance && python3 tools/stamp.py check /path/to/project/docs/principles --with science
```

`check` prints `CURRENT`, `BEHIND` (refresh with `into`) or `EDITED IN PLACE` for each page. A copy is never edited in place; propose the change here.

Each stamp line carries the sha256 of the text below it, and `into` also writes a stamped `copy_check.py` into the folder. The project's own test runs `python3 docs/principles/copy_check.py docs/principles`, which exits 0 only when every file in that folder is `INTACT`, with no clone of this repository. The folder holds the copies and nothing else.

## Changing a rule

A change is a commit here, with Joe's approval: the rule's text in the principles or the operating model, and its entry in the register (his words, the incident, the reason, the check). Then refresh each project's copy. Nothing is loaded into agent sessions globally; each project opts in through its copy.

## Talking between architects

Several projects' architects read and change these rules. A git repository carries commits, not messages, so:
- **Proposals** are `proposal/WHO-DATE` branches, one commit per proposal, each message naming who proposed it and Joe's words behind it.
- **Replies, questions and decisions' reasons** go on the channel: one append-only file, `CHANNEL.md`, on its own branch (`channel`), so main holds only rules.
  - `python3 tools/channel.py read --as "YOUR PARTY NAME"` prints new entries to you or to `all`. Run it at every lane check.
  - `python3 tools/channel.py post --from "YOUR PARTY NAME" --to "THEIR PARTY NAME" --subject "..." < body.txt` posts one.
- **Decisions** are merges to main. The architect who reviews a proposal merges it, or replies on the channel saying why not; a disagreement between architects goes to Joe.
- **Wake-ups:** where architects' sessions can message each other directly, a one-line "new on the channel" is enough; the channel stays the record.
