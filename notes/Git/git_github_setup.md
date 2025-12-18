# Git & GitHub Setup - Comprehensive Notes
**Date:** December 18, 2025  
**Topic:** Version Control Setup, Portfolio Management, and Multi-Machine Workflow

---

## Table of Contents
1. [Portfolio Assessment & Strategy](#portfolio-assessment--strategy)
2. [Git Fundamentals](#git-fundamentals)
3. [Initial Repository Setup](#initial-repository-setup)
4. [Understanding .gitignore](#understanding-gitignore)
5. [Authentication Methods](#authentication-methods)
6. [Two-Machine Workflow](#two-machine-workflow)
7. [Common Git Commands](#common-git-commands)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Best Practices](#best-practices)
10. [Next Steps](#next-steps)

---

## Portfolio Assessment & Strategy

### Current State Analysis

**Strengths:**
- Excellent technical documentation (especially Linux system administration notes)
- Consistent daily logging showing discipline
- Strong foundational knowledge
- Well-organized folder structure
- Good use of templates and automation

**Critical Gap:**
- Empty `/projects` folder - employers need to see what you can BUILD, not just what you've studied
- Empty `/tryhackme` folder
- Study notes alone won't differentiate you from other candidates

### Recommendation: Build Before You Showcase

**Timeline:**
- Wait 2-3 weeks before making portfolio public
- Use private repo for personal learning and version control NOW
- Build 3-5 projects before showcasing to employers
- Projects demonstrate applied skills, problem-solving, and completion ability

**Why Version Control Now, Showcase Later:**
- ✅ Access files from anywhere (laptop + desktop)
- ✅ Track changes and history
- ✅ Practice Git workflow
- ✅ Build projects incrementally
- ✅ When ready, make public with complete portfolio

### Project Ideas to Build
1. **Linux User Management Suite** - Automated user/group provisioning
2. **System Health Monitor** - CPU/RAM/disk monitoring with reports
3. **Network Diagnostic Toolkit** - Port scanning, DNS tools, connectivity tests
4. **Homelab Infrastructure Documentation** - Network diagrams, setup guides
5. **AWS Infrastructure Deployment** - Terraform/CloudFormation examples

---

## Git Fundamentals

### What is Git?

Git is a **distributed version control system** that tracks changes to files over time. Think of it as a sophisticated "save points" system for your code and documents.

**Key Concepts:**

**Repository (Repo):**
- Your project folder that Git tracks
- Contains your files + a hidden `.git` folder with all history
- Can exist locally (your computer) and remotely (GitHub)

**Commit:**
- A snapshot of your files at a specific moment
- Like a save point in a video game
- Includes a message describing what changed
- Immutable - once created, it's permanent in history

**Branch:**
- A parallel version of your code
- Default branch is `main` (used to be `master`)
- Allows experimentation without affecting main code
- Can be merged back when ready

**Remote:**
- A version of your repo hosted elsewhere (e.g., GitHub)
- Named `origin` by convention
- Allows backup and collaboration

**Staging Area:**
- Files you've marked to be included in next commit
- Like a "loading dock" before committing
- Use `git add` to stage files

### The Git Workflow Visualization

```
Working Directory → Staging Area → Local Repository → Remote Repository
    (edit files)    (git add)      (git commit)       (git push)
```

**Reverse flow (getting updates):**
```
Remote Repository → Local Repository → Working Directory
                   (git fetch)        (git merge/pull)
```

---

## Initial Repository Setup

### Step-by-Step First-Time Setup

#### 1. Configure Git Identity (Required)
```bash
# Set your name (appears in commits)
git config --global user.name "Brandon"

# Set your email (should match GitHub account)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

**Why this matters:** Every commit records who made it. This identifies you as the author.

#### 2. Navigate to Your Project
```bash
cd ~/Desktop/Brandos-learning-journey
# Or on Windows: cd /c/Users/becon/Desktop/Brandos-learning-journey
```

#### 3. Initialize Git Repository
```bash
git init
```

**What this does:**
- Creates a hidden `.git` folder
- This folder contains all Git's tracking data
- Your folder is now a Git repository

**You'll see:**
```
Initialized empty Git repository in /path/to/Brandos-learning-journey/.git/
```

#### 4. Check Repository Status
```bash
git status
```

**What this shows:**
- Current branch name
- Untracked files (files Git doesn't know about yet)
- Staged files (ready to commit)
- Modified files (tracked but changed)

#### 5. Stage All Files
```bash
# Stage everything
git add .

# Or be selective
git add README.md notes/ daily-logs/
```

**The `.` means:** "Add everything in current directory and subdirectories"

#### 6. Verify What's Staged
```bash
git status
```

**Critical check:** Make sure you DON'T see:
- `scratchpad-*.md` (should be ignored)
- `to-do-list.md` (should be ignored if you want it private)
- Any files with passwords, keys, or credentials

#### 7. Create First Commit
```bash
git commit -m "Initial commit: Learning journey and study notes"
```

**Good commit message format:**
```bash
# ✅ Good messages
git commit -m "Initial commit: Learning journey and study notes"
git commit -m "Add daily log for Dec 18 with Linux partitioning notes"
git commit -m "Fix script path to use relative directories"
git commit -m "Update README with skills matrix"

# ❌ Bad messages
git commit -m "update"
git commit -m "changes"
git commit -m "fixed stuff"
git commit -m "asdf"
```

**Why good messages matter:**
- Future you will need to understand what changed
- Employers look at commit history
- Shows professionalism and organization

#### 8. Rename Branch to Main
```bash
git branch -M main
```

**Why:** GitHub's default is now `main` instead of `master`. This ensures compatibility.

#### 9. Connect to GitHub
```bash
git remote add origin https://github.com/Btrigo/my-learning-journey.git
```

**Breaking this down:**
- `remote add` = add a remote location
- `origin` = nickname for the remote (standard convention)
- The URL = your GitHub repository

**Verify it worked:**
```bash
git remote -v
```

**Should show:**
```
origin  https://github.com/Btrigo/my-learning-journey.git (fetch)
origin  https://github.com/Btrigo/my-learning-journey.git (push)
```

#### 10. Push to GitHub
```bash
git push -u origin main
```

**Breaking this down:**
- `push` = send commits to remote
- `-u` = set upstream (makes future pushes easier)
- `origin` = the remote we just added
- `main` = the branch we're pushing

**The `-u` flag means:** Next time you can just type `git push` without specifying origin/main.

---

## Understanding .gitignore

### What is .gitignore?

A `.gitignore` file tells Git which files to **never track**. This is critical for:
- **Security** - Don't commit passwords, API keys, SSH keys
- **Privacy** - Keep personal notes private
- **Cleanliness** - Don't track OS junk files
- **Efficiency** - Don't track temporary/generated files

### How .gitignore Works

**Pattern Matching:**
```gitignore
# Exact filename in root directory only
secrets.txt

# Any file with this name anywhere
*.log

# Any file ending in .tmp
*.tmp

# Entire directory
temp/

# Directory anywhere in repo
**/cache/

# Exceptions (don't ignore this)
!important.log
```

### Your .gitignore File Explained

```gitignore
# =============================================================================
# SECURITY - NEVER COMMIT THESE (most important section)
# =============================================================================
*.pem          # SSH private keys
*.key          # Any key files
*.ppk          # PuTTY private keys
id_rsa*        # SSH keys (common name)

.env           # Environment variables with secrets
.env.local
credentials.json
secrets.yaml
config.json
**/secrets/    # Any "secrets" folder anywhere

.aws/credentials  # AWS credentials
.aws/config

*password*     # Any file with "password" in name
*secret*
*credential*

# =============================================================================
# PERSONAL FILES - Your private notes and scratchpad
# =============================================================================
scratchpad*.md       # scratchpad-12-2-2025.md, etc.
**/personal/         # Any folder named "personal"
**/private-notes/

to-do-list.md        # Your private to-do list

*draft*.md           # Any draft files
*WIP*.md             # Work in progress files

# =============================================================================
# OPERATING SYSTEM FILES - Junk your OS creates
# =============================================================================
# macOS
.DS_Store            # Mac folder settings
.AppleDouble
.LSOverride
._*

# Windows
Thumbs.db            # Image thumbnails
desktop.ini          # Folder settings
$RECYCLE.BIN/

# Linux
*~                   # Backup files
.directory

# =============================================================================
# EDITOR/IDE FILES - Config files for your code editor
# =============================================================================
.vscode/             # VS Code settings
*.code-workspace

*.sublime-project    # Sublime Text
*.sublime-workspace

*.swp                # Vim swap files
*.swo
*~

.idea/               # JetBrains IDEs
*.iml

# =============================================================================
# PYTHON - If you're writing Python scripts
# =============================================================================
__pycache__/         # Compiled Python files
*.py[cod]
*$py.class
*.so

venv/                # Virtual environments
env/
ENV/
.venv

build/               # Distribution files
dist/
*.egg-info/

# =============================================================================
# TEMPORARY FILES - Stuff that shouldn't be tracked
# =============================================================================
*.tmp
*.temp
*.log
*.bak
*.swp

tmp/                 # Temporary directories
temp/
cache/

logs/                # Log directories
*.log

# =============================================================================
# EXAMPLE/TEST FILES - Files you're just testing with
# =============================================================================
test_data/
sample_data/
**/tests/tmp/

example_output/
**/examples/*.log
**/examples/*.tmp
```

### Testing Your .gitignore

**Before committing:**
```bash
# See what will be tracked
git status

# See what's being ignored
git status --ignored

# Check if specific file is ignored
git check-ignore -v scratchpad.md
```

**Output explanation:**
```bash
$ git check-ignore -v scratchpad.md
.gitignore:27:scratchpad*.md	scratchpad.md
```
This means: Line 27 of .gitignore is ignoring this file.

### Common .gitignore Mistakes

**Mistake 1: Adding .gitignore after committing secrets**
```bash
# WRONG - too late!
git add password.txt
git commit -m "add config"
echo "password.txt" >> .gitignore  # File already in Git history!

# RIGHT - .gitignore first
echo "password.txt" >> .gitignore
git add .
git commit -m "initial commit"
```

**Mistake 2: Trying to ignore already-tracked files**
```bash
# If file is already tracked, .gitignore won't work
# You need to untrack it first:
git rm --cached secrets.txt
echo "secrets.txt" >> .gitignore
git commit -m "Remove secrets from tracking"
```

**Mistake 3: Forgetting wildcards**
```bash
# This only ignores logs/ in root
logs/

# This ignores logs/ anywhere
**/logs/
```

---

## Authentication Methods

### Why Authentication Changed in 2021

**Before August 13, 2021:**
```bash
git push
Username: Btrigo
Password: your-github-password  # ✅ This worked
```

**After August 13, 2021:**
```bash
git push
Username: Btrigo
Password: your-github-password  # ❌ REJECTED!
Password: your-token            # ✅ Must use token now
```

**Why the change?**
- Passwords can be reused across sites (security risk)
- Tokens can be scoped (limited permissions)
- Tokens can expire
- Tokens can be revoked without changing your password

### Three Authentication Methods

#### Method 1: HTTPS with Personal Access Token

**When you use it:**
- Remote URL: `https://github.com/username/repo.git`
- Most common for beginners
- Works on any system

**Setup:**
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select `repo` scope (full control of repositories)
4. Set expiration (90 days recommended)
5. Copy token (starts with `ghp_`)
6. Save it somewhere safe!

**Usage:**
```bash
git push
Username: Btrigo
Password: [paste your token - you won't see it]
```

**Save token so you don't re-enter:**
```bash
# Windows
git config --global credential.helper wincred

# Mac
git config --global credential.helper osxkeychain

# Linux
git config --global credential.helper store
```

**Pros:**
- Works everywhere
- Easy to understand

**Cons:**
- Token expires (need to regenerate)
- Need to save it somewhere
- Need to enter it at least once per machine

#### Method 2: SSH Keys (Recommended)

**When you use it:**
- Remote URL: `git@github.com:username/repo.git`
- Preferred by professionals
- Set up once, works forever

**How SSH Works:**
1. Generate a key pair (public + private key)
2. Give GitHub your public key
3. Keep private key on your computer
4. Git uses private key to prove identity

**Setup:**
```bash
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
# Press Enter 3 times (accept defaults, no passphrase)

# 2. Display public key
cat ~/.ssh/id_ed25519.pub
# Copy this entire output

# 3. Add to GitHub
# Go to: https://github.com/settings/keys
# Click "New SSH key"
# Title: "Laptop SSH Key"
# Key: Paste what you copied
# Click "Add SSH key"

# 4. Test connection
ssh -T git@github.com
# Should say: "Hi Btrigo! You've successfully authenticated..."

# 5. Change remote to use SSH
git remote set-url origin git@github.com:Btrigo/my-learning-journey.git

# 6. Push (no password needed!)
git push
```

**Pros:**
- No password ever needed
- More secure
- Never expires
- Industry standard

**Cons:**
- Slightly more complex initial setup
- Need to set up on each machine

#### Method 3: GitHub CLI or Desktop App

**GitHub Desktop, VS Code, GitKraken, etc.**
- Handle authentication for you
- OAuth login (logs you in through browser)
- Stores credentials automatically

**You probably used this before** without realizing it!

### Why You Weren't Prompted for Credentials

**Windows Credential Manager saved your credentials from previous GitHub usage:**

```bash
# Check if you have credential helper
git config --global credential.helper
```

**If it shows:**
- `manager` or `wincred` or `manager-core` ✅ Windows stores credentials
- `osxkeychain` ✅ Mac stores credentials
- `store` ✅ Linux stores credentials (less secure)

**Where Windows stores them:**
- Control Panel → Credential Manager → Windows Credentials
- Look for `git:https://github.com`

**This is why your push "just worked"!**

---

## Two-Machine Workflow

### The Golden Rule

**ALWAYS pull before you start working, ALWAYS push when you're done.**

```bash
# Starting work
git pull

# Make changes

# Finishing work
git add .
git commit -m "message"
git push
```

**This simple habit prevents 99% of problems.**

### Initial Setup on Desktop

After pushing from laptop, set up your desktop:

```bash
# 1. Navigate to where you want the project
cd ~/Desktop

# 2. Clone the repository
git clone https://github.com/Btrigo/my-learning-journey.git

# Output:
# Cloning into 'my-learning-journey'...
# remote: Enumerating objects: 50, done.
# Receiving objects: 100% (50/50), done.

# 3. Navigate into the cloned folder
cd my-learning-journey

# 4. Verify everything is there
ls -la

# 5. Check Git status
git status
# Should show: "On branch main, Your branch is up to date"

# 6. Verify remote
git remote -v
# Should show your GitHub URL
```

**That's it!** Both machines now have the same code.

### Daily Workflow Examples

#### Scenario 1: Work on Laptop, Switch to Desktop

**On Laptop (end of work session):**
```bash
cd ~/Desktop/Brandos-learning-journey

# Check what changed
git status

# Stage changes
git add .

# Commit with good message
git commit -m "Add daily log for Dec 19 and complete AWS lab exercises"

# Push to GitHub
git push
```

**On Desktop (start of work session):**
```bash
cd ~/Desktop/my-learning-journey

# Get latest changes from laptop
git pull

# You'll see:
# remote: Counting objects: 5, done.
# Updating abc1234..def5678
# Fast-forward
#  daily-logs/2025-12-19.md | 45 ++++++++++++++
#  notes/aws/new-topic.md   | 23 +++++++
#  2 files changed, 68 insertions(+)

# Verify you have the new files
ls daily-logs/
# You should see 2025-12-19.md

# Now work on desktop
# Make changes...

# When done:
git add .
git commit -m "Add network troubleshooting notes"
git push
```

**Back on Laptop (next session):**
```bash
cd ~/Desktop/Brandos-learning-journey

# Get desktop's changes
git pull

# Continue working...
```

#### Scenario 2: Edited Same File on Both Machines

**What happens:**
- Laptop: Edit `notes/linux.md`, push to GitHub
- Desktop: Edit `notes/linux.md` (without pulling first), try to push
- Git says: "Updates were rejected"

**Solution:**
```bash
# On desktop
git pull

# Git will try to auto-merge the changes
# If successful:
#   "Merge made by the 'recursive' strategy"

# Then push
git push

# If merge conflict (rare):
# 1. Git will mark conflicts in the file:
#    <<<<<<< HEAD
#    Your desktop changes
#    =======
#    Laptop changes
#    >>>>>>> commit-hash
#
# 2. Open the file and decide what to keep
# 3. Remove the <<<<<<, =======, >>>>>>> markers
# 4. Save the file
# 5. git add the-file.md
# 6. git commit -m "Resolve merge conflict in linux.md"
# 7. git push
```

#### Scenario 3: Forgot to Push from One Machine

**Example:** Worked on laptop, closed it without pushing, then worked on desktop.

**On Desktop (after making changes):**
```bash
# Always pull first!
git pull

# If laptop didn't push, nothing new to pull
# Make your changes
git add .
git commit -m "Add new notes"
git push
```

**On Laptop (when you remember):**
```bash
# Pull desktop's changes first
git pull

# If you have uncommitted local changes and desktop changes conflict:
# Git will try to merge or warn you

# Best practice: commit your laptop changes first
git add .
git commit -m "Laptop work from yesterday"

# Then pull
git pull

# Resolve any conflicts if needed
# Then push
git push
```

### Visualizing the Two-Machine Flow

```
LAPTOP                    GITHUB                    DESKTOP
------                    ------                    -------
Make changes
git add/commit/push ----> Updated with new code
                          
                          Code now on GitHub  <---- git pull (gets changes)
                                                    Make changes
                          Updated again       <---- git add/commit/push

git pull (gets changes)
Make changes
git push ---------------> Updated
```

### Checking Which Machine Has Latest Code

**On any machine:**
```bash
# See recent commits
git log --oneline -5

# Shows last 5 commits with messages
# Most recent is at top
```

**Check if you have uncommitted changes:**
```bash
git status
```

**Possible outputs:**
```bash
# Everything synced, nothing new
"nothing to commit, working tree clean"

# You have uncommitted changes locally
"Changes not staged for commit:"

# You have commits not pushed to GitHub
"Your branch is ahead of 'origin/main' by 1 commit"

# GitHub has commits you don't have
"Your branch is behind 'origin/main' by 1 commit"

# Both have different commits
"Your branch and 'origin/main' have diverged"
```

---

## Common Git Commands

### Everyday Commands

```bash
# Check status (use constantly!)
git status

# Stage files
git add .                    # Stage everything
git add file.md             # Stage specific file
git add notes/              # Stage entire directory

# Commit staged files
git commit -m "message"

# Push to GitHub
git push

# Pull from GitHub
git pull

# View commit history
git log
git log --oneline           # Condensed view
git log --oneline -5        # Last 5 commits
git log --graph --oneline   # Visual branch graph

# See what changed
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff HEAD~1             # Compare to last commit

# View remote info
git remote -v               # Show remote URLs
git remote show origin      # Detailed remote info
```

### Branch Commands

```bash
# List branches
git branch                  # Local branches
git branch -a               # All branches (local + remote)

# Create new branch
git branch feature-name

# Switch branches
git checkout feature-name
git switch feature-name     # Newer syntax

# Create and switch in one command
git checkout -b feature-name
git switch -c feature-name  # Newer syntax

# Merge branch into current branch
git merge feature-name

# Delete branch
git branch -d feature-name  # Safe delete (won't delete unmerged)
git branch -D feature-name  # Force delete
```

### Undoing Changes

```bash
# Unstage a file (keep changes)
git reset HEAD file.md

# Discard changes to file (CAREFUL!)
git checkout file.md
git restore file.md         # Newer syntax

# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged)
git reset HEAD~1

# Undo last commit (DISCARD changes - DANGEROUS!)
git reset --hard HEAD~1

# Create new commit that undoes a previous commit
git revert HEAD             # Undo last commit
git revert abc1234          # Undo specific commit
```

### Stashing (Temporarily Save Changes)

```bash
# Save current changes without committing
git stash

# List stashed changes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{0}

# Delete a stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

### Fixing Mistakes

```bash
# Forgot to add files to last commit
git add forgotten-file.md
git commit --amend --no-edit

# Change last commit message
git commit --amend -m "Better message"

# Untrack file but keep it locally
git rm --cached file.txt
# Then add to .gitignore

# Recover deleted file
git checkout HEAD -- file.md

# See who changed what
git blame file.md           # Line-by-line author info
```

### Remote Commands

```bash
# Add remote
git remote add origin URL

# Change remote URL
git remote set-url origin NEW_URL

# Remove remote
git remote remove origin

# Fetch updates without merging
git fetch origin

# Fetch and merge (same as git pull)
git fetch origin
git merge origin/main

# Push new branch to remote
git push -u origin branch-name

# Delete remote branch
git push origin --delete branch-name
```

---

## Troubleshooting Guide

### Issue: "Please tell me who you are"

**Problem:** Git doesn't know your identity.

**Solution:**
```bash
git config --global user.name "Brandon"
git config --global user.email "your.email@example.com"

# Then retry your commit
git commit -m "your message"
```

---

### Issue: "Updates were rejected" when pushing

**Error message:**
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do not have locally
```

**Meaning:** GitHub has commits you don't have (probably from your other machine or someone else).

**Solution:**
```bash
# Pull first, then push
git pull origin main

# If you get merge conflicts, resolve them
# Then push
git push
```

**If this is your first push and GitHub created a README:**
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

### Issue: Merge Conflicts

**When it happens:** Two people (or two machines) edited the same part of the same file.

**What you'll see:**
```
Auto-merging notes/file.md
CONFLICT (content): Merge conflict in notes/file.md
Automatic merge failed; fix conflicts and then commit the result.
```

**In the file:**
```markdown
Some content that's fine

<<<<<<< HEAD
Your local changes
=======
Remote changes from GitHub
>>>>>>> abc1234

More content that's fine
```

**How to fix:**
1. Open the conflicted file
2. Decide what to keep (remove one section or combine both)
3. Delete the `<<<<<<<`, `=======`, `>>>>>>>` markers
4. Save the file
5. Stage it: `git add notes/file.md`
6. Commit: `git commit -m "Resolve merge conflict in file.md"`
7. Push: `git push`

**Example resolution:**
```markdown
Some content that's fine

Combined version with both changes merged together

More content that's fine
```

---

### Issue: "fatal: not a git repository"

**Meaning:** You're not in a Git-tracked directory.

**Solution:**
```bash
# Make sure you're in the right folder
cd path/to/Brandos-learning-journey

# Or initialize Git if you haven't
git init
```

---

### Issue: Accidentally Committed a Secret

**What you did:**
```bash
git add password.txt
git commit -m "add config"
git push  # OH NO!
```

**Immediate action:**
```bash
# Remove from tracking but keep file locally
git rm --cached password.txt

# Add to .gitignore
echo "password.txt" >> .gitignore

# Commit the removal
git commit -m "Remove password file from tracking"
git push
```

**BUT BEWARE:** The file is still in Git history! Anyone can see old commits.

**For complete removal (advanced):**
```bash
# Use git filter-branch or BFG Repo-Cleaner
# This rewrites history - research before using!

# Better: Rotate the compromised credentials immediately
# Change passwords, regenerate API keys, etc.
```

---

### Issue: Forgot to Add .gitignore Before First Commit

**Problem:** You already committed files that should be ignored.

**Solution:**
```bash
# 1. Create .gitignore
nano .gitignore
# Add patterns for files to ignore

# 2. Remove tracked files that should be ignored
git rm --cached scratchpad.md
git rm --cached -r logs/

# 3. Commit the changes
git commit -m "Add .gitignore and remove files that should be ignored"

# 4. Future changes to these files won't be tracked
```

---

### Issue: Wrong Commit Message

**If you haven't pushed yet:**
```bash
# Change the last commit message
git commit --amend -m "Better message"
```

**If you already pushed:**
```bash
# Change message
git commit --amend -m "Better message"

# Force push (use carefully!)
git push --force
```

**Warning:** Force push can cause problems if others have pulled your code!

---

### Issue: Need to Undo Last Commit

**Keep changes, undo commit:**
```bash
git reset --soft HEAD~1
# Your changes are still staged
```

**Keep changes, unstage them:**
```bash
git reset HEAD~1
# Your changes are still there, just unstaged
```

**Discard everything (DANGEROUS!):**
```bash
git reset --hard HEAD~1
# All changes are GONE!
```

---

### Issue: Line Ending Warnings (Windows)

**Warning:**
```
warning: LF will be replaced by CRLF the next time Git touches it
```

**Meaning:** Git is converting Unix-style line endings (LF) to Windows-style (CRLF).

**This is harmless!** Your files will work fine.

**To silence warnings:**
```bash
git config --global core.autocrlf false
```

**Or let Git handle it automatically:**
```bash
git config --global core.autocrlf true  # Recommended for Windows
```

---

### Issue: Can't Push - Permission Denied

**HTTPS error:**
```
remote: Permission denied
fatal: Authentication failed
```

**Solutions:**
1. Check your token hasn't expired
2. Regenerate token with correct scopes
3. Clear cached credentials:
   ```bash
   # Windows
   git credential-manager erase https://github.com
   
   # Mac
   git credential-osxkeychain erase
   host=github.com
   protocol=https
   # Press Enter twice
   ```

**SSH error:**
```
Permission denied (publickey)
```

**Solutions:**
1. Check SSH key is added to GitHub
2. Test SSH connection: `ssh -T git@github.com`
3. Generate new key if needed (see SSH setup section)

---

### Issue: Merge Message Editor Won't Close

**What happened:** Git opened a text editor for a merge message.

**In VS Code:**
- Just close the file tab (click X or Ctrl+W)
- Git will continue automatically

**In Vim (terminal editor):**
```
Press ESC
Type :wq
Press Enter
```

**In Nano (terminal editor):**
```
Press Ctrl+O (save)
Press Enter (confirm)
Press Ctrl+X (exit)
```

---

### Issue: "detached HEAD state"

**What it means:** You checked out a specific commit instead of a branch.

**How to get back:**
```bash
git checkout main
# or
git switch main
```

**If you made changes in detached HEAD:**
```bash
# Create a new branch from here
git checkout -b new-branch-name
# or
git switch -c new-branch-name
```

---

## Best Practices

### Commit Best Practices

**Commit Often:**
```bash
# Don't wait until end of day to commit everything
# Commit logical chunks as you work

# Bad: 1 commit with 50 changed files
git add .
git commit -m "today's work"

# Good: Multiple commits with related changes
git add daily-logs/2025-12-19.md
git commit -m "Add daily log for Dec 19"

git add notes/linux/systemd.md
git commit -m "Add notes on systemd service management"

git add scripts/backup.sh
git commit -m "Create automated backup script"
```

**Write Meaningful Commit Messages:**

**Format:**
```
Short summary (50 chars or less)

Optional longer description if needed.
Explain WHY the change was made, not just WHAT changed.
```

**Good examples:**
```bash
git commit -m "Add user authentication to login page"
git commit -m "Fix null pointer exception in data parser"
git commit -m "Update README with installation instructions"
git commit -m "Refactor database connection code for better performance"
```

**Bad examples:**
```bash
git commit -m "changes"
git commit -m "fix"
git commit -m "update"
git commit -m "asdf"
git commit -m "final version"
git commit -m "final version 2"
git commit -m "final version actually final"
```

**Conventions:**
```bash
# Start with a verb in present tense
"Add feature"    not "Added feature"
"Fix bug"        not "Fixed bug"
"Update docs"    not "Updated docs"

# Common prefixes
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Formatting, no code change
refactor: Code restructuring
test: Adding tests
chore: Maintenance tasks
```

### Branch Best Practices

**Main branch:**
- Should always be stable
- Don't commit broken code directly
- Deploy from here

**Feature branches:**
```bash
# Create branch for each feature/task
git checkout -b add-user-authentication
git checkout -b fix-login-bug
git checkout -b update-readme

# Work on branch
# Make commits
# When done, merge back to main

git checkout main
git merge add-user-authentication
```

**Branch naming:**
```bash
# Good names
feature/user-authentication
fix/login-bug
docs/update-readme
refactor/database-connection

# Bad names
temp
test
new-branch
asdf
```

### .gitignore Best Practices

**Add .gitignore FIRST:**
```bash
# Before any commits
# 1. Create .gitignore
# 2. Add patterns
# 3. Then git init and git add
```

**Be specific but comprehensive:**
```gitignore
# Too broad (bad)
*

# Too narrow (bad)
secret-key-file-2025-12-18.txt

# Just right (good)
*secret*
*.key
.env
```

**Common categories to ignore:**
1. Credentials and secrets
2. Personal files
3. OS-generated files
4. Editor/IDE files
5. Compiled/generated files
6. Temporary files
7. Dependencies (node_modules, etc.)

### Security Best Practices

**Never commit:**
- Passwords, API keys, tokens
- SSH private keys
- Database credentials
- .env files with secrets
- Customer data
- Personal information

**If you accidentally commit a secret:**
1. Immediately rotate/change the compromised credential
2. Remove file from Git tracking
3. Add to .gitignore
4. Consider rewriting Git history (advanced)

**Use environment variables:**
```python
# Bad
password = "my-secret-password"

# Good
import os
password = os.getenv("DATABASE_PASSWORD")
```

### Collaboration Best Practices

**Pull before you push:**
```bash
# Always get latest changes first
git pull
# Make your changes
git add .
git commit -m "message"
git push
```

**Communicate with team:**
- Let others know if you're working on a file
- Use branches for experimental work
- Write clear commit messages
- Review others' code

**Code review workflow:**
```bash
# 1. Create feature branch
git checkout -b new-feature

# 2. Make changes and commit
git add .
git commit -m "Add new feature"

# 3. Push branch
git push -u origin new-feature

# 4. Create pull request on GitHub
# 5. Team reviews code
# 6. Make requested changes
# 7. Merge when approved
```

### Performance Best Practices

**Don't track large files:**
- Binary files > 100MB
- Videos, images (unless necessary)
- Compiled executables
- Archives (.zip, .tar.gz)

**For large files, use Git LFS:**
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.mp4"

# Commit .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS"
```

**Keep commits focused:**
```bash
# Bad: Mixing unrelated changes
git add .
git commit -m "Update README, fix bug, add feature, refactor code"

# Good: Separate commits
git add README.md
git commit -m "Update README with new instructions"

git add src/bugfix.py
git commit -m "Fix null pointer in data parser"

git add src/feature.py
git commit -m "Add user authentication"
```

---

## Next Steps

### Immediate Actions (This Week)

1. **Clone to Desktop**
   ```bash
   cd ~/Desktop
   git clone https://github.com/Btrigo/my-learning-journey.git
   cd my-learning-journey
   git status
   ```

2. **Test the Two-Machine Workflow**
   - Make a change on laptop, push
   - Pull on desktop, verify change
   - Make a change on desktop, push
   - Pull on laptop, verify change

3. **Practice Daily Git Workflow**
   ```bash
   # Start of work session
   git pull
   
   # During work
   git add .
   git commit -m "message"
   
   # End of work session
   git push
   ```

### Short-Term (Next 2 Weeks)

1. **Build Your First Project**
   - User Management Automation Suite
   - Document in /projects folder
   - Write clear README
   - Commit incrementally as you build

2. **Establish Daily Habits**
   - Pull before starting work
   - Commit at logical stopping points
   - Push when done
   - Never go more than 1 day without syncing

3. **Learn Advanced Git**
   - Practice branching
   - Try resolving a merge conflict (intentionally create one)
   - Experiment with `git stash`
   - Learn `git log` and `git diff` in depth

### Medium-Term (Next Month)

1. **Build 3-5 Projects**
   - Populate your /projects folder
   - Each with working code and documentation
   - Commit history showing development process

2. **Consider SSH Setup**
   - More convenient than tokens
   - Follow SSH setup guide above
   - Set up on both machines

3. **Prepare Public Portfolio**
   - Clean up commit history
   - Write comprehensive README
   - Add architecture diagrams
   - Consider separate repos for major projects

### Long-Term

1. **Contribute to Open Source**
   - Fork repositories
   - Submit pull requests
   - Learn collaboration workflows

2. **Learn Advanced Git**
   - Interactive rebase
   - Cherry-picking commits
   - Submodules
   - Git hooks

3. **Explore Git Services**
   - GitHub Actions (CI/CD)
   - GitHub Pages (portfolio website)
   - GitHub Issues and Projects

---

## Quick Reference Card

Save this section for daily use:

### Essential Commands
```bash
# Daily workflow
git pull              # Start: get latest
git status            # Check what changed
git add .             # Stage changes
git commit -m "msg"   # Save snapshot
git push              # End: send to GitHub

# Info commands
git status            # Current state
git log --oneline     # Recent commits
git diff              # See changes
git remote -v         # Show remotes

# Undo commands
git reset HEAD file   # Unstage file
git checkout file     # Discard changes
git commit --amend    # Fix last commit

# Branch commands
git branch            # List branches
git checkout -b name  # Create and switch
git merge name        # Merge branch
```

### Common Workflows

**Normal work session:**
```bash
git pull
# make changes
git add .
git commit -m "description"
git push
```

**Fix a mistake:**
```bash
# Forgot to add file
git add forgotten.md
git commit --amend --no-edit

# Wrong commit message
git commit --amend -m "better message"

# Want to undo commit
git reset --soft HEAD~1
```

**Merge conflict:**
```bash
git pull  # Conflict happens
# Edit files, remove <<< === >>> markers
git add conflicted-file.md
git commit -m "Resolve merge conflict"
git push
```

---

## Additional Resources

### Official Documentation
- Git: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com/
- GitHub Skills: https://skills.github.com/

### Learning Resources
- Interactive Git Tutorial: https://learngitbranching.js.org/
- Pro Git Book (free): https://git-scm.com/book/en/v2
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf

### Tools
- GitHub Desktop: https://desktop.github.com/
- GitKraken: https://www.gitkraken.com/
- VS Code Git Integration: Built-in

### Your Specific Setup

**Repositories:**
- Laptop: `/c/Users/becon/Desktop/Brandos-learning-journey`
- Desktop: `~/Desktop/my-learning-journey` (after cloning)
- GitHub: https://github.com/Btrigo/my-learning-journey

**Branch:** `main`

**Remote:** `origin` (https://github.com/Btrigo/my-learning-journey.git)

**Authentication:** Windows Credential Manager (automatic)

---

## Glossary

**Repository (Repo):** A project folder tracked by Git

**Commit:** A snapshot of your files at a point in time

**Branch:** A parallel version of your code

**Remote:** A version of your repo hosted elsewhere (e.g., GitHub)

**Origin:** Default name for your main remote

**Clone:** Copy a remote repository to your local machine

**Fork:** Copy someone else's repository to your GitHub account

**Pull:** Download changes from remote to local

**Push:** Upload changes from local to remote

**Fetch:** Download changes without merging

**Merge:** Combine changes from different branches

**Staging Area:** Files marked to be included in next commit

**HEAD:** Pointer to current commit/branch

**Upstream:** The original repository you forked from

**.git folder:** Hidden folder containing all Git data

**.gitignore:** File specifying which files to ignore

**Working Directory:** Your actual files (what you see and edit)

**Tracked Files:** Files Git is monitoring for changes

**Untracked Files:** Files Git doesn't know about yet

**Conflict:** When Git can't automatically merge changes

**Fast-forward:** Merge where no new commits are created

**Detached HEAD:** Viewing a specific commit instead of a branch

---

## Summary

**What You Accomplished Today:**
1. ✅ Set up Git on your laptop
2. ✅ Created comprehensive .gitignore
3. ✅ Fixed script to use relative paths
4. ✅ Made your first commit
5. ✅ Connected to GitHub
6. ✅ Resolved merge conflict
7. ✅ Successfully pushed to GitHub
8. ✅ Learned Git fundamentals
9. ✅ Understood authentication methods
10. ✅ Prepared for two-machine workflow

**Your Portfolio is Now:**
- ✅ Version controlled
- ✅ Accessible from anywhere
- ✅ Backed up on GitHub
- ✅ Ready for collaborative development
- ✅ Tracking your learning journey

**Next Time You Work:**
```bash
# Pull first
git pull

# Make changes
# ...

# Commit and push
git add .
git commit -m "what you did"
git push
```

**Remember:** Git is a skill that improves with practice. The more you use it, the more natural it becomes. You've got the foundation - now build on it!

---

*End of Comprehensive Git & GitHub Setup Notes*