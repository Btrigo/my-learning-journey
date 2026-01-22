# Git Quick Reference & Troubleshooting Guide

## Table of Contents
1. [Undoing Commits](#undoing-commits)
2. [Fixing Commit Messages](#fixing-commit-messages)
3. [Managing Files](#managing-files)
4. [Branch Mistakes](#branch-mistakes)
5. [Working with Remote (GitHub)](#working-with-remote-github)
6. [Emergency Fixes](#emergency-fixes)
7. [Daily Workflow](#daily-workflow)

---

## Undoing Commits

### Scenario 1: "I Just Committed, Haven't Pushed Yet"

**Undo commit, keep changes (most common):**
```bash
git reset HEAD~1

# Your changes go back to uncommitted
# Files are still modified/staged
# You can fix and re-commit
```

**Undo commit, discard all changes (DANGEROUS):**
```bash
git reset --hard HEAD~1

# ⚠️ WARNING: Deletes everything
# Cannot be undone
# Only use if you want to lose the work
```

**Undo multiple commits:**
```bash
git reset HEAD~3        # Undo last 3 commits, keep changes
git reset --hard HEAD~3 # Undo last 3 commits, delete changes
```

**Undo to specific commit:**
```bash
# Find commit hash
git log --oneline

# Reset to that commit
git reset abc1234       # Keep changes
git reset --hard abc1234 # Delete changes
```

### Scenario 2: "Already Pushed to GitHub"

**Use revert instead of reset:**
```bash
# Creates new commit that undoes the last one
git revert HEAD

# Git opens editor for revert message
# Save and close

# Push the revert
git push origin main
```

**Why revert instead of reset?**
- Other people might have pulled your commit
- Reset rewrites history (causes problems)
- Revert adds new commit (safe for collaboration)

**Revert multiple commits:**
```bash
git revert HEAD~2..HEAD  # Revert last 2 commits
git push origin main
```

### Scenario 3: "I Committed to Wrong Branch"

```bash
# You're on main, but meant to commit to feature branch

# 1. Undo the commit (keep changes)
git reset HEAD~1

# 2. Save your changes
git stash

# 3. Switch to correct branch
git checkout feature-branch
# Or create new branch:
git checkout -b feature-branch

# 4. Restore your changes
git stash pop

# 5. Commit on correct branch
git add .
git commit -m "Your message"
git push origin feature-branch
```

### Quick Reference: Reset vs Revert

| Command | Changes History? | When to Use |
|---------|-----------------|-------------|
| `git reset` | Yes (rewrites) | Before pushing |
| `git revert` | No (adds commit) | After pushing |

---

## Fixing Commit Messages

### Scenario 1: "Wrong Message on Last Commit (Not Pushed)"

```bash
git commit --amend -m "Correct message"

# Replaces the last commit message
# Commit hash changes
# Only do before pushing
```

### Scenario 2: "Want to Add More to Last Commit"

```bash
# Make your additional changes
nano file.txt

# Stage the changes
git add file.txt

# Add to previous commit
git commit --amend --no-edit

# Or with new message:
git commit --amend -m "Updated message with new changes"
```

### Scenario 3: "Already Pushed, Need Different Message"

```bash
# DON'T amend after pushing (causes problems)
# Instead, just make new commit explaining:
git commit --allow-empty -m "Correction: previous commit actually did X not Y"
git push origin main
```

---

## Managing Files

### Scenario 1: "Accidentally Added Wrong Files"

**Before committing:**
```bash
# Unstage specific file
git reset file.txt

# Unstage all files
git reset

# Files still modified, just not staged
```

**After committing but before pushing:**
```bash
# Remove file from last commit
git reset HEAD~1              # Undo commit
git reset file.txt            # Unstage the wrong file
git commit -m "Your message"  # Re-commit without it
```

### Scenario 2: "Want to Ignore Files I Already Committed"

```bash
# Add to .gitignore
echo "secret.txt" >> .gitignore

# Remove from Git (keeps local file)
git rm --cached secret.txt

# Commit the removal
git add .gitignore
git commit -m "Remove secret.txt from tracking"
git push origin main
```

### Scenario 3: "Deleted File by Accident"

**If not committed yet:**
```bash
# Restore single file
git checkout -- file.txt

# Restore all deleted files
git checkout -- .
```

**If committed and pushed:**
```bash
# Find the commit before deletion
git log -- file.txt

# Restore from specific commit
git checkout abc1234 -- file.txt

# Commit the restoration
git add file.txt
git commit -m "Restore accidentally deleted file"
git push origin main
```

---

## Branch Mistakes

### Scenario 1: "Working on Wrong Branch"

```bash
# Save your work
git stash

# Switch to correct branch
git checkout correct-branch

# Restore your work
git stash pop

# Continue working
```

### Scenario 2: "Want to Delete a Branch"

**Delete local branch:**
```bash
# Must switch to different branch first
git checkout main

# Delete merged branch
git branch -d feature-branch

# Force delete unmerged branch (CAREFUL!)
git branch -D feature-branch
```

**Delete remote branch:**
```bash
git push origin --delete feature-branch
```

### Scenario 3: "Merged Wrong Branch"

**If haven't pushed:**
```bash
# Undo the merge
git reset --hard HEAD~1

# Or if merge created merge commit:
git reset --hard ORIG_HEAD
```

**If already pushed:**
```bash
# Revert the merge
git revert -m 1 HEAD
git push origin main
```

---

## Working with Remote (GitHub)

### Scenario 1: "Pushed Something I Shouldn't Have"

**Option 1: Revert (safest):**
```bash
git revert HEAD
git push origin main
```

**Option 2: Force push (DANGEROUS, use only on personal repos):**
```bash
# Undo locally
git reset --hard HEAD~1

# Force push (overwrites GitHub)
git push --force origin main

# ⚠️ WARNING: Only do this if:
# - Personal project
# - Nobody else has pulled
# - You understand the risks
```

### Scenario 2: "Can't Push - Conflicts with Remote"

```bash
# Pull changes first
git pull origin main

# If conflicts, resolve them:
# 1. Open conflicting files
# 2. Edit to fix conflicts
# 3. Remove conflict markers
git add .
git commit -m "Resolved merge conflicts"

# Now push
git push origin main
```

### Scenario 3: "Want to Undo Push (Personal Repo Only)"

```bash
# Local: undo commit
git reset --hard HEAD~1

# Force push to GitHub
git push --force origin main

# ⚠️ Only on personal projects!
```

---

## Emergency Fixes

### "I Have No Idea What I Did - Start Over"

**If changes not committed:**
```bash
# Discard all local changes
git reset --hard HEAD

# Remove untracked files
git clean -fd

# Pull fresh from GitHub
git pull origin main
```

**If committed locally but not pushed:**
```bash
# Throw away all local commits
git reset --hard origin/main

# Now you match GitHub exactly
```

**Nuclear option (⚠️ DELETES EVERYTHING):**
```bash
# Completely start over
cd ..
rm -rf project-name
git clone https://github.com/username/project-name.git
cd project-name
```

### "I Committed Sensitive Data (Passwords, Keys)"

**Immediate action:**
```bash
# Remove file from last commit
git reset HEAD~1
git rm --cached secrets.txt
echo "secrets.txt" >> .gitignore
git add .gitignore
git commit -m "Remove sensitive data"

# If already pushed:
git push --force origin main
```

**Then immediately:**
1. Change the password/key
2. Consider the old one compromised
3. For thorough cleanup, use `git filter-branch` or BFG Repo-Cleaner

### "Branch is Completely Broken"

```bash
# Delete and recreate from main
git checkout main
git branch -D broken-branch
git checkout -b new-feature-branch

# Start fresh
```

---

## Daily Workflow

### Starting Work

```bash
# Always start with latest code
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/my-work

# Work on your changes
```

### During Work

```bash
# Check what you've changed
git status
git diff

# Stage changes
git add .
# Or specific files:
git add file1.txt file2.txt

# Commit often
git commit -m "Descriptive message"

# Backup to GitHub
git push origin feature/my-work
```

### Finishing Work

```bash
# Switch to main
git checkout main

# Merge your feature
git merge feature/my-work

# Push to GitHub
git push origin main

# Delete feature branch
git branch -d feature/my-work
git push origin --delete feature/my-work
```

### Quick Backup

```bash
# Save work in progress (even if not ready to commit)
git add .
git commit -m "WIP: work in progress"
git push origin feature-branch

# Continue later from different machine
git pull origin feature-branch
```

---

## Common Commands Cheat Sheet

### Viewing Status
```bash
git status                  # What's changed
git log                     # Commit history
git log --oneline           # Compact history
git log --oneline --graph   # Visual branch history
git diff                    # See changes not staged
git diff --staged           # See staged changes
```

### Undoing Things
```bash
git reset HEAD~1            # Undo last commit, keep changes
git reset --hard HEAD~1     # Undo last commit, delete changes
git revert HEAD             # Create new commit undoing last one
git checkout -- file.txt    # Discard changes to file
git clean -fd               # Remove untracked files
```

### Branch Management
```bash
git branch                  # List branches
git branch feature-name     # Create branch
git checkout feature-name   # Switch to branch
git checkout -b feature     # Create and switch
git branch -d feature       # Delete branch
git merge feature           # Merge branch into current
```

### Remote Operations
```bash
git remote -v               # Show remote URLs
git pull origin main        # Get latest from GitHub
git push origin main        # Send commits to GitHub
git push -u origin branch   # Push new branch
git fetch                   # Download without merging
```

### Saving Work
```bash
git stash                   # Save uncommitted changes
git stash list              # See stashed changes
git stash pop               # Restore and remove from stash
git stash apply             # Restore but keep in stash
git stash drop              # Delete stashed changes
```

---

## Troubleshooting Decision Tree

**"I messed up, what do I do?"**

```
Did you commit? 
├─ No → git reset HEAD (unstage)
│       git checkout -- file (discard changes)
│
└─ Yes → Did you push?
          ├─ No → git reset HEAD~1 (safe to rewrite history)
          │
          └─ Yes → git revert HEAD (don't rewrite history)
                   OR
                   git push --force (personal repo only!)
```

---

## Safety Tips

### Before Doing Anything Drastic

1. **Check status:**
   ```bash
   git status
   git log --oneline -5
   ```

2. **Create backup branch:**
   ```bash
   git branch backup-$(date +%Y%m%d)
   # Now you have a safety copy
   ```

3. **Test on copy first:**
   ```bash
   # Clone to test folder
   git clone /path/to/repo /tmp/test-repo
   cd /tmp/test-repo
   # Try your fix here first
   ```

### Rules of Thumb

✓ **DO:**
- Commit often
- Push to backup branches
- Use descriptive commit messages
- Pull before pushing
- Test before merging to main

✗ **DON'T:**
- Use `--force` on shared branches
- Commit sensitive data
- Work directly on main for features
- Make huge commits
- Panic - everything is recoverable

---

## When Things Go Really Wrong

**"I need help!"**

```bash
# See what Git suggests
git status

# See recent actions
git reflog

# Get help for a command
git help reset
git reset --help
```

**Remember:**
- Git stores everything
- Almost nothing is truly lost
- `git reflog` shows ALL actions
- You can recover from most mistakes
- When in doubt, ask before force-pushing

---

## Practice Exercise: Safe Experimentation

```bash
# Create practice repo
mkdir git-practice
cd git-practice
git init

# Make some commits
echo "File 1" > file1.txt
git add file1.txt
git commit -m "First commit"

echo "File 2" > file2.txt
git add file2.txt
git commit -m "Second commit"

echo "File 3" > file3.txt
git add file3.txt
git commit -m "Third commit"

# Now practice undoing:
git log --oneline              # See commits
git reset HEAD~1               # Undo last commit
git status                     # file3.txt is back to uncommitted
git add file3.txt             
git commit -m "Third commit (again)"

# Practice stashing:
echo "More changes" >> file1.txt
git stash
git stash pop

# Practice branching:
git checkout -b experiment
echo "Experiment" > experiment.txt
git add experiment.txt
git commit -m "Experimental feature"
git checkout main
git merge experiment

# Delete practice repo when done
cd ..
rm -rf git-practice
```

---

*This guide covers 90% of Git mistakes you'll encounter. Bookmark it!*