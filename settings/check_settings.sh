#!/bin/zsh
# Compare this machine's agent settings with the reference copies in this folder.
# It only reports differences. It changes nothing; Joe approves every change.
D=${0:A:h}
show() { # label reference live
  if [ ! -f "$3" ]; then echo "== $1: MISSING on this machine ($3)"; return; fi
  if diff -q "$2" "$3" >/dev/null; then echo "== $1: same as the reference"; else echo "== $1: DIFFERS (reference first, this machine second)"; diff -u "$2" "$3" | sed -n '3,200p'; fi
}
echo "Machine: $(scutil --get ComputerName 2>/dev/null || hostname)"
show "Codex settings (~/.codex/config.toml)" "$D/codex_config.toml" ~/.codex/config.toml
show "Codex global instructions (~/.codex/AGENTS.md)" "$D/codex_global_AGENTS.md" ~/.codex/AGENTS.md
show "Claude settings (~/.claude/settings.json)" "$D/claude_settings.json" ~/.claude/settings.json
