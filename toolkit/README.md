# Worker toolkit

How an architect starts and keeps workers on Joe's machines, written once so nobody relearns it (C-038). Each fact here was learned the hard way. A new one is proposed here the day it is learned.

## Codex workers

- **Start one:** `python3 toolkit/codex_worker.py --workdir WT --brief BRIEF.md --out PREFIX --rules RULES.md --effort medium`. Run each one as its own background job. `--census` gives a read-only sandbox for a census or a review. `--print` shows the command without running it.
- **The command:** `codex` on the PATH. Where there is none (Joe's laptop), the tool uses the copy inside the VS Code extension, `~/.vscode/extensions/openai.chatgpt-*/bin/<platform>/codex`. Joe's word is the authorization to run it.
- **Local network:** the workspace sandbox refuses even a `127.0.0.1` bind unless `sandbox_workspace_write.network_access=true` is set. Without it every test that starts a server fails, and the failure looks like the code's. The tool sets it.
- **Version control is read-only inside the sandbox**, even with `--add-dir` on the `.git` folder: a merge fails on `ORIG_HEAD.lock`. So (C-032):
  - the architect prepares any merge (`git merge --no-commit`, conflicts left in the tree);
  - the worker edits files only and leaves them uncommitted;
  - the architect reviews, commits with the task's key, pushes and hands in.
  Say so in the rules file, or the worker spends its first turn finding out.
- **Effort:** the user's Codex config may default to the highest effort. Pass the tier C-022 names for the task.
- **One task, one session, one working copy** (C-005). The worker's last message (`PREFIX.final.md`) is its report; brief it to put the tip, the files, every test command with its counts, and anything unresolved there.
- **It cannot push, and it cannot reach the GitHub login.** The architect pushes.
- **Turn off the desktop notifier** (`notify=[]`); a headless worker otherwise calls the user's desktop hook at every turn end. The tool sets it.

## Claude workers (subagents)

- They run in the background and report once per result. Continue one with a message to it, never by starting a new one for the same task. If its report did not arrive, ask it to send it.
- A worker that ends its turn while its own background waits are still running reads as "waiting". When the wait no longer matters, tell it to stand down and stop its loops.
- Restarting the editor ends every worker and every background job of the session. Check what was committed, and start again from the brief.
- A worker never kills a process it did not start. When the architect's permissions also refuse, name the process (pid, what it runs, since when) to Joe with the one command (C-026).

## Machine facts that void work

- **A laptop on battery sleeps, and at 1% it hibernates.** `caffeinate -s` holds only on mains power. A run that spans a sleep is void: read `pmset -g log` before calling a stall, and re-run rather than diagnose its failures.
- **The GitHub login lives in the macOS keychain.** When the token expires, git erases it, and every fetch and push on that machine, including background followers, fails with `could not read Username for 'https://github.com': Device not configured`. Restarting the editor does not restore it. One `git fetch` in the Terminal app, with a personal access token as the password, does. Check with `printf 'protocol=https\nhost=github.com\n\n' | git credential-osxkeychain get` (it prints nothing when the login is gone).
- **A stuck run that holds a shared slot blocks every other run on the machine** (for example browser-test slots). Find the holder by its open lock files (`lsof`) and name it.
- **An editable install imports one checkout's code wherever a command runs.** To run a repository command as a given commit, run it from a working copy of that commit, never from a checkout on another branch.
