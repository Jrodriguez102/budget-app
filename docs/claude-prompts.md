# Prompts for Jacob's Claude

Copy/paste these into Claude (web, or the VS Code extension) at each stage of
frontend work. Run them in order — each one assumes the previous step is done.

Pull this file (`git pull`) before starting a new session in case a prompt has
been updated or a new one added.

---

## 1. Getting started (run this first)

```
I'm a beginner coder helping build a personal budgeting app's frontend. I know very
little about coding, Git, GitHub, or VS Code, so please walk me through things
step-by-step and explain what each command does before I run it.

Context on the project:
- It's a personal budgeting app with a Next.js + Tailwind frontend and a
  Python/FastAPI backend.
- My friend owns the backend and the budget allocation logic. I own the frontend.
- The repo is on GitHub and I've been added as a collaborator.
- I do NOT need the backend running to start — there are example JSON files
  (called "fixtures") that show exactly what the data will look like, and I
  should build against those first.

What I need help with, in order:
1. Confirm I have Git, Node.js, and VS Code installed (help me check/install if not).
2. Help me clone the repo to my computer using the terminal.
3. Help me open the repo in VS Code and understand the folder structure.
4. Walk me through reading these files in this order and explain what each means
   for what I'll be building:
   - README.md (root)
   - docs/API_CONTRACT.md
   - the four files in the fixtures/ folder
   - frontend/README.md
5. Once I understand the data shapes, help me run `npx create-next-app@latest .`
   inside the frontend folder to scaffold the app, and get a basic dev server running.
6. Then help me build a simple dashboard page that loads plan_normal.json (one of
   the fixtures) and displays: income/expense summary, goal progress bars, and
   category suggestions — just static layout, no interactivity yet.

Please pause after each major step and make sure I understand what happened before
moving to the next one. Also explain basic Git concepts (branch, commit, push,
pull request) as they come up, since I'll need to know them to submit my work.
```

---

## 2. Once the static dashboard shell is working

```
[Placeholder — next prompt goes here once the static dashboard from step 1 is done.
This will cover handling the other three fixture states (plan_tight,
plan_no_variable_budget, plan_negative_income) and building the status/message
banner UI for each.]
```

---

## Notes for Jacob
- You don't need to wait on the backend. Everything you build in early steps uses
  the fixture JSON files as stand-ins for real API responses.
- If Claude suggests something that touches files outside `frontend/`, pause and
  check with your collaborator first.
- Commit often, in small chunks, and open a pull request instead of pushing
  straight to `main` — your collaborator will review before merging.
