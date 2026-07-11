# Collaborating on This Repo

A reference for how we work together on this project — branches, PRs, and the
day-to-day Git rhythm. Read this once up front, then use it as a lookup whenever
you forget a command or a step.

## The core idea

The repo is split into `backend/` (Julian) and `frontend/` (Jacob), so most of
the time we're not touching the same files. The one place our work overlaps is
`docs/API_CONTRACT.md` — the shared definition of what data looks like. As long
as we both build against that contract, we can work independently without
knowing the details of each other's code.

## Branch model

Nobody pushes straight to `main`. `main` is always the "known good" version of
the app.

1. Before starting work, create a feature branch off `main`:
   ```bash
   git checkout main
   git pull
   git checkout -b your-branch-name
   ```
   Example branch names: `backend-allocation-engine`, `frontend-dashboard-shell`.

2. Commit freely to your own branch — small, frequent commits are easier to
   review and easier to undo if something breaks.

3. When a chunk of work is ready, push your branch:
   ```bash
   git push -u origin your-branch-name
   ```

4. Open a **pull request (PR)** on GitHub from your branch into `main`.

5. The other person reviews it and merges it. Reviewing doesn't need to be
   deep — even a quick read-through catches most misunderstandings early.

## Daily rhythm

- **Start of a session:** `git checkout main && git pull` — get the latest
  merged work before branching off again.
- **While working:** commit often on your branch.
- **End of a session / feature done:** push your branch, open a PR, let the
  other person know.
- **After a PR merges:** both people run `git checkout main && git pull` before
  starting the next branch, so nobody builds on stale code for long.

## Where conflicts can happen

Even with separate folders, a few things can cause friction:

- **`docs/API_CONTRACT.md` changes** — a breaking change for whoever's building
  against it. Flag contract changes to the other person *before* changing them,
  not after.
- **Root-level files** (`README.md`, config files) — rare, but both people could
  touch these.
- **Fixture files** (`plan_normal.json`, etc.) — shared reference data. If these
  change, frontend work built against old assumptions might look wrong.

If a real conflict happens, Git will show exactly which file and lines when
merging — it's not silent, it just needs a human to pick the right version.

## Branch protection

`main` is protected — pushing directly to it is blocked for everyone, PRs are
required. This isn't about trust, it's a safety net so nobody accidentally
overwrites good work.

## Communication touchpoints

Git handles the mechanics, but these matter more than any tooling:

- **Before changing the API contract** — tell the other person first.
- **When a fixture changes** — same, quick heads-up.
- **When a PR is ready** — the other person reviews before merging, even
  briefly.

## Quick command reference

```bash
# Start new work
git checkout main
git pull
git checkout -b my-branch-name

# Save progress
git add .
git commit -m "short description of what changed"

# Share work
git push -u origin my-branch-name
# (first push only needs -u origin my-branch-name; after that just `git push`)

# After your PR merges
git checkout main
git pull
```
