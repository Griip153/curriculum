# Day 1 — Teaching Lesson: Setup, Git & GitHub, and How the Web Works

> Companion to `README.md`. This lesson assumes **zero** prior programming experience.
> Every step is written out in full — don't skip ahead, and don't worry if something
> takes you longer than you expect. Everyone's computer fights back a little on Day 1.

## Objective
Set up a professional workspace and understand the machine you will spend two months
programming inside: the request/response cycle.

## 0. What is "backend" development, actually?

Every app you use — Instagram, a banking app, a food delivery app — is really two
programs talking to each other:

- The **frontend** is what you see and tap: buttons, screens, colours. It runs on
  *your* phone or in *your* browser.
- The **backend** is a program running on someone else's computer (a **server**),
  which the frontend talks to over the internet to get or save data — your posts,
  your bank balance, your order history.

This track is entirely about the second one: writing the program that lives on the
server, stores data, and answers requests correctly and securely. **FastAPI**, which
you'll meet in Week 2, is the tool we'll use to write that program in Python.

## 1. Installing Python

**Definition:** Python is a programming language — a way of writing instructions that
a computer can follow exactly. We use it because it reads close to plain English and
because it is one of the two or three most common languages for backend work today.

1. Go to **python.org/downloads** and download the latest Python 3 release (3.11 or
   newer).
2. Run the installer.
   - **Windows:** on the very first installer screen, tick the box **"Add python.exe
     to PATH"** before clicking Install. This one checkbox is the single most common
     Day 1 mistake — if you skip it, your terminal won't be able to find Python at all.
   - **Mac:** the default installer options are fine.
3. Confirm it worked. Open a terminal (Windows: search "Command Prompt" or
   "PowerShell"; Mac: search "Terminal") and type:
   ```bash
   python3 --version
   ```
   On Windows it might be `python --version` instead — try both if one doesn't work.
   You should see something like `Python 3.12.1`. If you see an error like "command
   not found," Python isn't on your PATH yet — reinstall and make sure to tick that box.

**Checkpoint:** `python3 --version` (or `python --version`) prints a version number,
no errors.

## 2. Installing VS Code

**Definition:** VS Code (Visual Studio Code) is a code editor — a text editor built
specifically for writing and running programs, with built-in terminal access, syntax
highlighting, and error-checking.

1. Go to **code.visualstudio.com**, download it, and install it — default options are
   fine.
2. Open VS Code and install two extensions (click the four-squares icon on the left
   sidebar, search, click Install):
   - **Python** (by Microsoft)
   - **Pylance** (by Microsoft, usually installs alongside Python)
3. Open VS Code's built-in terminal: **View → Terminal**, or `` Ctrl+` `` (backtick).
   You'll use this terminal, not a separate one, for the entire track.

**Checkpoint:** you can open VS Code, open its terminal panel, and run
`python3 --version` inside it with the same result as Step 1.

## 3. Virtual environments — why they exist (a first look)

**Definition:** A virtual environment is an isolated, self-contained copy of Python
and its installed packages, kept inside one project folder, so that different
projects on your machine can use different (even conflicting) versions of the same
tool without interfering with each other.

You don't need to create one today — that happens properly in Week 2 once you have a
real project to isolate. But understand *why* it matters now, so it isn't a mystery
later: imagine Project A needs version 1 of a tool and Project B needs version 2 of
the *same* tool. Without virtual environments, installing one breaks the other. A
virtual environment gives each project its own private toolbox.

## 4. Git — saving versions of your work

**Definition:** Git is a program that tracks changes to your files over time, so you
can save a "snapshot" (called a **commit**) whenever your code reaches a working
point, see exactly what changed between snapshots, and undo mistakes safely.

1. Download Git from **git-scm.com** and install it (default options are fine).
2. Confirm it worked:
   ```bash
   git --version
   ```
3. Tell Git who you are — it stamps every commit with this, and it should match your
   GitHub account:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

**The four commands you'll use constantly, in order:**
```bash
git add .              # stage every changed file — "I want to include this in the next snapshot"
git commit -m "message" # take the snapshot, with a short description of what changed
git push                # send your snapshots to GitHub
git pull                # download snapshots someone else pushed, before you start working
```

**Definition of each word, precisely:**
- **Repository ("repo")** — a project folder that Git is tracking.
- **Stage** — mark a file as "included in the next commit." `git add .` stages
  everything that changed.
- **Commit** — a saved snapshot of the staged files, with a message describing it.
- **Push / pull** — upload your commits to GitHub / download commits from GitHub.

## 5. GitHub — where your repos live online

**Definition:** GitHub is a website that hosts Git repositories online, so your code
is backed up, shareable, and reviewable by other people (or your instructor).

1. Create a free account at **github.com** if you don't have one.
2. You'll be added to the training organisation — accept the invite email.
3. Create your first repo:
   - On GitHub, click **New repository**.
   - Name it `seed-backend-python`.
   - Tick **"Add a README file."**
   - Click **Create repository**.
4. Clone it to your computer — this downloads a working copy you can edit:
   ```bash
   git clone https://github.com/YOUR-ORG/seed-backend-python.git
   cd seed-backend-python
   ```

**Checkpoint:** you have a local folder `seed-backend-python` that is a working copy
of a repo that also exists on GitHub.

## 6. Your first Python file

Open the `seed-backend-python` folder in VS Code (**File → Open Folder**). Create a
new file called `hello.py` with this single line:
```python
print("Hello, backend track!")
```
**Definition:** `print(...)` is a built-in Python function that displays text in the
terminal. It's the very first tool you'll use to see what your code is doing.

Run it from the VS Code terminal:
```bash
python3 hello.py
```
You should see `Hello, backend track!` printed. That's it — you just ran your first
program.

Now save your work with Git:
```bash
git add .
git commit -m "Add hello.py"
git push
```

## 7. How the web works — clients, servers, and HTTP

**Definition:** A client is any program that *makes* a request — your browser, a
mobile app, Postman. A server is a program that *listens* for requests and sends back
a response. The whole conversation between them follows a shared set of rules called
**HTTP** (HyperText Transfer Protocol).

Think of it like ordering at a restaurant counter:
- You (the **client**) walk up and place an order (the **request**).
- The kitchen (the **server**) prepares it and hands it back (the **response**).
- Both sides follow a shared menu format so the order makes sense to both of you —
  that shared format is HTTP.

**The pieces of a request, in plain terms:**
- **Method** — what kind of action you want: `GET` (fetch something), `POST` (create
  something), `PUT`/`PATCH` (update something), `DELETE` (remove something).
- **URL** — the address of the specific thing you want, e.g.
  `https://api.example.com/students/7`.
- **Headers** — small pieces of metadata about the request (e.g. "I'm sending JSON,"
  "here's my login token").
- **Body** — the actual data you're sending, for methods like `POST` and `PUT` (a new
  student's name and score, for example).

**The pieces of a response:**
- **Status code** — a 3-digit number that summarises what happened: `200` means "OK,
  here's your data," `404` means "not found," `500` means "the server broke." You'll
  learn the full set over the next few weeks.
- **Body** — the data being sent back, almost always as **JSON** in this track (a
  text format for structured data you'll meet properly in Week 1, Day 4).

This entire track is about writing the **server** side of this conversation — a
Python program that listens for requests like these and answers them correctly.

## 8. Submitting your first daily report

Every day, you'll open a Pull Request in the `daily-reports` repo describing what you
built. Your instructor will give you the exact repo link and template on Day 1 — for
today, your report should mention: Python and VS Code installed successfully, your
first Git commit pushed, and one sentence, in your own words, describing what a
"request" and a "response" are.

---

## Common mistakes to watch for
- **Forgetting to add Python to PATH on Windows** — if `python3 --version` fails,
  this is almost always why. Reinstall and tick the box.
- **Running `git push` before `git add` and `git commit`** — push only sends
  snapshots that already exist; if you haven't committed anything, there's nothing to
  push.
- **Editing files on GitHub's website *and* locally at the same time** — this causes
  conflicting versions. Always `git pull` before you start working, and always work
  in one place at a time.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*