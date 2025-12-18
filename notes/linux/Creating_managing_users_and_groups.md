# Linux System Administration - Comprehensive Study Notes
**Date:** December 16, 2025  
**Topic:** User & Group Management, Permissions, and File Systems

---

## Table of Contents
1. [Overview & Learning Objectives](#overview--learning-objectives)
2. [User Account Management](#user-account-management)
3. [Group Management](#group-management)
4. [File & Directory Permissions](#file--directory-permissions)
5. [Advanced Topics](#advanced-topics)
6. [Command Reference Guide](#command-reference-guide)
7. [Lab Practice Summary](#lab-practice-summary)
8. [Key Concepts from Lectures](#key-concepts-from-lectures)

---

## Overview & Learning Objectives

### Main Lab Focus: Creating and Managing Users and Groups on Linux
The objective of this lab was to learn:
- Create and delete user accounts
- Create and delete groups
- Assign users to groups
- Change user and group ownership of files and directories
- Change access permissions of files and folders for different targets

### Additional Topics Covered
- Work with storage drives and filesystems
- Partition disk drives
- Create and mount partitions
- Persistent mounting of partitions

---

## User Account Management

### 1. Creating User Accounts

#### Basic User Creation
```bash
# Create a basic user account
sudo useradd foo

# Create user with home directory
sudo useradd -m username

# Create user with specific shell
sudo useradd -s /bin/bash username
```

#### User Account Types

**Standard User Accounts:**
- Meant for people
- Have home directories
- Usually have passwords
- Assigned UID ≥ 1000

**System User Accounts:**
- Used by programs/scripts
- Usually no home directory
- Usually no password
- Assigned UID between 100-999

```bash
# Create system user
sudo useradd -r bar
```

#### User Creation Options

| Option | Purpose | Example |
|--------|---------|---------|
| `-m` | Create home directory | `sudo useradd -m alice` |
| `-r` | Create system user | `sudo useradd -r serviceaccount` |
| `-s` | Specify shell | `sudo useradd -s /bin/bash bob` |
| `-d` | Specify home directory | `sudo useradd -d /custom/path user` |
| `-c` | Add comment/full name | `sudo useradd -c "John Doe" jdoe` |
| `-G` | Add to secondary groups | `sudo useradd -G developers alice` |

#### Preventing Shell Access
```bash
# Create user without shell access
sudo useradd -s /sbin/nologin baz

# This user cannot login to the terminal
# Useful for service accounts
```

### 2. Password Management

```bash
# Set password for a user
sudo passwd username

# Set password during batch creation
echo "username:password" | sudo chpasswd

# Lock a user account
sudo usermod -L username

# Unlock a user account
sudo usermod -U username
```

### 3. Modifying User Accounts

```bash
# Change user's default shell
sudo chsh -s /bin/bash username
sudo usermod -s /bin/bash username  # Alternative

# Change user's home directory
sudo usermod -d /new/home/path username

# Move user's home directory
sudo usermod -d /new/home/path -m username

# Add user to supplementary group
sudo usermod -a -G groupname username

# Change user's primary group
sudo usermod -g groupname username
```

### 4. Viewing User Information

```bash
# View user details
getent passwd username
# Output format: username:x:UID:GID:comment:home:shell

# View user IDs
id username
# Output: uid=1001(username) gid=1001(groupname) groups=...

# Check current user
whoami

# Check available shells
cat /etc/shells

# Check current shell
echo $SHELL

# View all users
cat /etc/passwd

# Search for specific user
cat /etc/passwd | grep username
```

### 5. Deleting User Accounts

```bash
# Delete user (keeps home directory)
sudo userdel username

# Delete user and home directory
sudo userdel -r username

# Force delete (even if logged in)
sudo userdel -rf username
```

**Important:** Always use `-r` flag to remove home directory unless you need to keep user files for archival purposes.

#### Cleanup After Deletion
```bash
# Find files owned by deleted user (by UID)
sudo find / -uid 1001 2>/dev/null

# Remove mail spool
sudo rm -f /var/spool/mail/username

# Remove cron jobs
sudo rm -f /var/spool/cron/crontabs/username
```

---

## Group Management

### 1. Understanding Groups

When a user account is created, a primary group with the same name is automatically created. This is called the **User Private Groups (UPG)** scheme.

**Group Types:**
- **Primary Group:** The main group a user belongs to (specified in `/etc/passwd`)
- **Secondary/Supplementary Groups:** Additional groups a user can belong to

### 2. Creating Groups

```bash
# Create a new group
sudo groupadd groupname

# Examples from lab
sudo groupadd marvel
sudo groupadd dc
sudo groupadd superhuman
```

### 3. Adding Users to Groups

```bash
# Add user to supplementary group
sudo usermod -a -G groupname username

# Add user to multiple groups
sudo usermod -a -G group1,group2,group3 username

# Alternative method using gpasswd
sudo gpasswd -a username groupname
```

**Important:** Always use `-a` (append) flag with `-G` to avoid removing user from other groups!

### 4. Removing Users from Groups

```bash
# Remove user from a group
sudo gpasswd -d username groupname
```

### 5. Viewing Group Information

```bash
# List all groups
getent group
cat /etc/group

# View specific group
getent group groupname

# See group members only
getent group groupname | cut -d: -f4

# View user's groups
groups username

# View current user's groups
groups

# Detailed group info with IDs
id username
```

### 6. Deleting Groups

```bash
# Delete a group
sudo groupdel groupname
```

**Note:** Cannot delete a group if it's the primary group of any user. Change the user's primary group first or delete the user.

---

## File & Directory Permissions

### 1. Understanding Permission Notation

#### Permission Types (rwx)
- **r (read)** = 4: Read file contents or list directory contents
- **w (write)** = 2: Modify file or create/delete files in directory
- **x (execute)** = 1: Execute file or enter directory

#### Permission Targets
1. **Owner (User)** - The file owner
2. **Group** - Users in the file's group
3. **Others** - Everyone else

#### Permission Display Format
```
-rwxr-xr--
│└┬┘└┬┘└┬┘
│ │  │  └─ Others (r--)
│ │  └──── Group (r-x)
│ └─────── Owner (rwx)
└───────── File type (- = file, d = directory)
```

### 2. Reading Permissions with ls -l

```bash
$ ls -l
-rw-r--r-- 1 alice developers 2048 Dec 16 file.txt
│││││││││  │ │     │          │    │      └── filename
│││││││││  │ │     │          │    └───────── timestamp
│││││││││  │ │     │          └────────────── size
│││││││││  │ │     └───────────────────────── group owner
│││││││││  │ └─────────────────────────────── user owner
│││││││││  └───────────────────────────────── hard links
└┬┘└┬┘└┬┘
 │  │  └─ Others: r-- (read only)
 │  └──── Group: r-- (read only)
 └─────── Owner: rw- (read & write)
```

### 3. Numeric Permission Values

| Symbolic | Binary | Numeric | Meaning |
|----------|--------|---------|---------|
| `---` | 000 | 0 | No permissions |
| `--x` | 001 | 1 | Execute only |
| `-w-` | 010 | 2 | Write only |
| `-wx` | 011 | 3 | Write + Execute |
| `r--` | 100 | 4 | Read only |
| `r-x` | 101 | 5 | Read + Execute |
| `rw-` | 110 | 6 | Read + Write |
| `rwx` | 111 | 7 | Full permissions |

### 4. Common Permission Combinations

| Permission | Numeric | Use Case |
|------------|---------|----------|
| `-rw-------` | 600 | Private files (owner only) |
| `-rw-r--r--` | 644 | Public readable files |
| `-rw-rw-r--` | 664 | Group writable files |
| `-rwx------` | 700 | Private executables |
| `-rwxr-xr-x` | 755 | Public executables |
| `drwxr-xr-x` | 755 | Public directories |
| `drwx------` | 700 | Private directories |

### 5. Changing Permissions (chmod)

```bash
# Numeric notation
sudo chmod 644 file.txt
sudo chmod 755 script.sh
sudo chmod 700 private_dir/

# Symbolic notation
chmod u+x file.sh          # Add execute for owner
chmod g-w file.txt         # Remove write from group
chmod o-r file.txt         # Remove read from others
chmod a+r file.txt         # Add read for all
chmod u=rwx,g=rx,o=r file  # Set exact permissions

# Recursive changes
sudo chmod -R 755 directory/
```

#### chmod Symbolic Notation

**Targets:**
- `u` = user/owner
- `g` = group
- `o` = others
- `a` = all

**Operators:**
- `+` = add permission
- `-` = remove permission
- `=` = set exact permission

**Examples:**
```bash
chmod u+x script.sh        # Owner can now execute
chmod g-w report.txt       # Group can no longer write
chmod o-rwx private.txt    # Others have no access
chmod a+r public.txt       # Everyone can read
```

### 6. Changing Ownership (chown)

```bash
# Change owner only
sudo chown newowner file

# Change group only (note the colon!)
sudo chown :newgroup file

# Change both owner and group
sudo chown newowner:newgroup file

# Change owner and set to owner's primary group
sudo chown newowner: file

# Recursive changes
sudo chown -R user:group directory/
```

**Memory Trick:**
- **No colon** = owner only
- **:group** = group only
- **user:group** = both

#### Alternative: chgrp Command
```bash
# Change group ownership
sudo chgrp groupname file

# These are equivalent:
sudo chown :groupname file
sudo chgrp groupname file
```

---

## Advanced Topics

### 1. sudo - Superuser Do

**What is sudo?**
- Executes commands as root (UID 0)
- Only available to administrator accounts
- Requires authentication with current user's password
- Authentication valid for a few minutes per terminal session

```bash
# Execute command as root
sudo command

# Examples
sudo useradd newuser
sudo mkdir /opt/myapp
sudo chmod 755 /etc/config
```

**Authentication Prompt:**
```
[sudo] password for student:
```
Type your current user's password, NOT the root password.

### 2. Bulk Operations

#### For Loops
```bash
# Create multiple users
for user in user1 user2 user3; do
    sudo useradd -m $user
done

# Delete multiple users
for user in user1 user2 user3; do
    sudo userdel -r $user
done

# Change shells for multiple users
for user in alice bob charlie; do
    sudo chsh -s /bin/bash $user
done

# Add multiple users to a group
for user in alice bob charlie; do
    sudo usermod -a -G developers $user
done
```

#### Range Creation
```bash
# Create user1 through user10
for i in {1..10}; do
    sudo useradd -m user$i
done
```

#### From File
```bash
# Users list in users.txt
while read user; do
    sudo useradd -m $user
    echo "$user:password123" | sudo chpasswd
done < users.txt
```

#### With Error Handling
```bash
for user in user1 user2 user3; do
    if id "$user" &>/dev/null; then
        sudo usermod -s /bin/bash $user
        echo "✓ Changed shell for $user"
    else
        echo "✗ User $user does not exist"
    fi
done
```

### 3. Important System Files

#### /etc/passwd
Contains user account information:
```
username:x:UID:GID:comment:home:shell
```

```bash
# View all users
cat /etc/passwd

# Search for specific user
getent passwd username
```

#### /etc/shadow
Contains encrypted passwords (requires root):
```bash
sudo cat /etc/shadow
```

#### /etc/group
Contains group information:
```
groupname:x:GID:member1,member2,member3
```

```bash
# View all groups
cat /etc/group

# Search for specific group
getent group groupname
```

### 4. Home Directories

**Default Location:** `/home/username`

**Creating with Home Directory:**
```bash
# Automatically creates /home/username
sudo useradd -m username

# Copy skeleton files
sudo cp -r /etc/skel/. /home/username/
```

**Manual Creation:**
```bash
# Create directory
sudo mkdir /home/username

# Copy skeleton files
sudo cp -r /etc/skel/. /home/username/

# Set ownership
sudo chown -R username:username /home/username

# Set permissions
sudo chmod 700 /home/username
```

### 5. Special Directories

#### /opt Directory
- For optional/third-party software
- Self-contained applications
- Not managed by package manager
- Examples: `/opt/google/chrome/`, `/opt/vmware/`

**Typical Structure:**
```
/opt/application/
├── bin/     # executables
├── lib/     # libraries
└── etc/     # configuration
```

---

## Command Reference Guide

### Quick Command Lookup Table

| Task | Command | Example |
|------|---------|---------|
| **USER MANAGEMENT** |
| Create user | `useradd` | `sudo useradd -m alice` |
| Create system user | `useradd -r` | `sudo useradd -r nginx` |
| Set password | `passwd` | `sudo passwd alice` |
| Modify user | `usermod` | `sudo usermod -s /bin/bash alice` |
| Change shell | `chsh` | `sudo chsh -s /bin/bash alice` |
| Delete user | `userdel` | `sudo userdel -r alice` |
| View user info | `id` / `getent passwd` | `id alice` |
| Check current user | `whoami` | `whoami` |
| Switch user | `su` | `su alice` |
| **GROUP MANAGEMENT** |
| Create group | `groupadd` | `sudo groupadd developers` |
| Add user to group | `usermod -aG` | `sudo usermod -aG devs alice` |
| Remove from group | `gpasswd -d` | `sudo gpasswd -d alice devs` |
| List groups | `getent group` | `getent group` |
| View user's groups | `groups` | `groups alice` |
| Delete group | `groupdel` | `sudo groupdel developers` |
| **PERMISSIONS** |
| Change permissions | `chmod` | `chmod 755 file` |
| Change owner | `chown` | `chown alice:devs file` |
| Change group | `chgrp` | `chgrp devs file` |
| View permissions | `ls -l` | `ls -l file` |
| **DIRECTORIES** |
| Create directory | `mkdir` | `mkdir mydir` |
| Remove empty dir | `rmdir` | `rmdir mydir` |
| Remove with contents | `rm -rf` | `rm -rf mydir` |
| List contents | `ls` | `ls -la` |
| Change directory | `cd` | `cd /home` |
| Print working dir | `pwd` | `pwd` |

### Essential Options Reference

#### useradd Options
```
-m    Create home directory
-r    Create system user
-s    Set shell
-d    Set home directory
-c    Add comment/full name
-G    Add to groups
```

#### usermod Options
```
-s    Change shell
-d    Change home directory
-m    Move home directory
-a    Append to groups (use with -G)
-G    Set supplementary groups
-g    Change primary group
-L    Lock account
-U    Unlock account
```

#### chmod Quick Reference
```
644   -rw-r--r--  Standard file
755   -rwxr-xr-x  Executable/Directory
700   -rwx------  Private directory
600   -rw-------  Private file
```

---

## Lab Practice Summary

### Users Created in Lab
From command history, these users were created:
- foo (first test user)
- bar (system user with `-r`)
- baz (no shell access with `/sbin/nologin`)
- brando
- gina, barbara, javier, peter, bruce, clark
- tony, peter, steve (Marvel group)
- bruce, clark, diana (DC group)
- teacher (for ownership exercises)

### Groups Created in Lab
- marvel
- dc
- superhuman (later deleted)
- normies
- boughtnotbuilt
- sudoers, sudo
- academics

### Permission Exercises Completed
- Created directories: homework, grades, feedback
- Changed ownership with chown
- Modified permissions with chmod (644, 711, 710, 760, 740, 741, 750)
- Practiced both user:group and :group syntax

### Key Practice Patterns
1. Created users individually and in bulk
2. Added users to multiple groups
3. Removed users from specific groups
4. Changed shells for users
5. Set up directory ownership scenarios
6. Applied various permission schemes

---

## Key Concepts from Lectures

### Storage & Filesystems (Week 3 Concept Session)

**Learning Objectives:**
- Work with storage drives and filesystems
- Partition disk drives
- Create and mount partitions
- Persistent mounting of partitions

**Important Commands:**
```bash
# List block devices
lsblk
lsblk -f

# Disk usage
df -h
df -hT /dev/sd*

# Partition management
fdisk -l
fdisk /dev/sdb

# Format filesystems
mkfs.ext4 /dev/sdb1
which mkfs.ext4
ls -l /usr/sbin/mkfs*

# Mounting
mount -t ext4 /dev/sdb1 /mnt/data
sudo mount -a

# Unmounting
umount /dev/sdb1

# Filesystem check
sudo fsck /dev/sdb

# Persistent mounting
nano /etc/fstab
```

**Key Concepts:**
- **Block Devices:** Any disk on the machine (use lsblk)
- **MBR vs GPT:** 
  - BIOS uses Master Boot Record (MBR)
  - UEFI uses GUID Partition Table (GPT)
  - GPT supports up to 128 primary partitions
- **Serial devices vs Character devices**
- **/var:** Contains logs and mail that can expand significantly

**Persistent Mounting Workflow:**
1. Create partitions (fdisk)
2. Assign filesystem (mkfs)
3. Create mount directories under /mnt
4. Mount partitions to directories
5. Add entries to /etc/fstab for auto-mount

**fstab Format:**
```
device  mount_point  filesystem  options  dump  pass
```

### Important File System Locations
- `/dev/sda3` - Primary hard drive partition
- `/mnt` - Temporary mount point
- `/var` - Variable data (logs, mail)
- `/etc/fstab` - Persistent mount configuration

---

## Questions & Additional Notes

### Questions from Week 3 Notes:

1. **How can you change the ownerships all at once?**
   - Use for loops or xargs for bulk operations
   - Example: `for dir in dir1 dir2 dir3; do chown user:group $dir; done`

2. **How can you add users and groups all at once?**
   - Use for loops with ranges: `for i in {1..10}; do useradd user$i; done`
   - Read from file: `while read user; do useradd $user; done < users.txt`

3. **Can you change ownerships outside of the folder?**
   - Yes! You can chown any file/directory you have sudo access to
   - Example: `sudo chown alice:devs /opt/app/file`

4. **How do you add a file to multiple groups?**
   - A file can only have ONE group owner at a time
   - To grant access to multiple groups, use ACLs (Access Control Lists) - advanced topic
   - Alternative: Add users to a common group and set that as the file's group

### Common Mistakes to Avoid:

1. **Using `userdel` without `-r`**
   - Always use `sudo userdel -r username` to remove home directory
   - Otherwise, orphaned files remain in /home

2. **Forgetting `-a` with `usermod -G`**
   - `usermod -G group user` replaces all groups
   - `usermod -aG group user` appends to existing groups

3. **Using `rm -rf` carelessly**
   - Double-check paths before executing
   - A space in the wrong place can be catastrophic
   - Example: `rm -rf / home/user` vs `rm -rf /home/user`

4. **Not using `sudo` for administrative tasks**
   - Most user/group management requires sudo
   - Watch for "Permission denied" errors

5. **Confusing `chown user:group` with `chown :group`**
   - No colon = owner only
   - :group = group only
   - user:group = both

### Best Practices:

1. **Always verify before deleting**
   ```bash
   id username          # Check user exists
   groups username      # Check group membership
   ls -l /home/username # Check what will be deleted
   sudo userdel -r username  # Then delete
   ```

2. **Test with echo first**
   ```bash
   # Preview what will happen
   for user in user1 user2 user3; do
       echo "Would delete: $user"
   done
   ```

3. **Use descriptive usernames and groups**
   - Avoid generic names like user1, user2
   - Use role-based names: webadmin, dbadmin, developers

4. **Document permission schemes**
   - Keep notes on why specific permissions were set
   - Use comments in scripts

5. **Regular audits**
   ```bash
   # List all users
   cat /etc/passwd
   
   # List all groups
   cat /etc/group
   
   # Find files with specific permissions
   find /home -perm 777
   ```

---

## Practice Exercises & Review

### Exercise 1: Complete User Setup
```bash
# Create user with all options
sudo useradd -m -s /bin/bash -c "John Doe" -G developers,sudo jdoe
sudo passwd jdoe
id jdoe
groups jdoe
```

### Exercise 2: Permission Scenarios
```bash
# Scenario: Shared project directory
sudo mkdir /projects/team-alpha
sudo chown :developers /projects/team-alpha
sudo chmod 770 /projects/team-alpha

# Scenario: Public readable, owner writable
sudo chmod 644 document.txt

# Scenario: Script executable by owner only
chmod 700 myscript.sh
```

### Exercise 3: Bulk Operations
```bash
# Create 5 test users
for i in {1..5}; do
    sudo useradd -m test$i
    echo "test$i:password" | sudo chpasswd
done

# Clean up
for i in {1..5}; do
    sudo userdel -r test$i
done
```

---

## Troubleshooting Guide

### Common Issues & Solutions

**Issue:** "Permission denied" when creating user
- **Solution:** Use `sudo` - only root can create users

**Issue:** "User already exists"
- **Solution:** Choose a different username or delete existing user first

**Issue:** "Directory not empty" when using rmdir
- **Solution:** Use `rm -rf directory` for non-empty directories

**Issue:** Can't login after creating user
- **Solution:** Set password with `sudo passwd username`

**Issue:** User can't execute sudo commands
- **Solution:** Add user to sudo group: `sudo usermod -aG sudo username`

**Issue:** Home directory not created
- **Solution:** Use `-m` flag: `sudo useradd -m username`

**Issue:** Changes to groups not taking effect
- **Solution:** User must log out and back in for group changes to apply

---

## Additional Resources & Commands

### System Information Commands
```bash
uname -a          # System information
lsb_release       # Distribution info
hostnamectl       # Hostname and system info
uptime           # System uptime
free -h          # Memory usage
df -h            # Disk usage
lscpu            # CPU information
```

### Useful Aliases
```bash
# Add to ~/.bashrc
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
```

### Related Topics for Future Study
- Access Control Lists (ACLs)
- SELinux / AppArmor
- PAM (Pluggable Authentication Modules)
- LDAP integration
- SSH key authentication
- File system quotas
- Advanced shell scripting

---

## Summary & Key Takeaways

### Critical Commands Learned Today
1. `useradd` / `userdel` - User creation and deletion
2. `groupadd` / `groupdel` - Group creation and deletion
3. `usermod` - Modify user properties
4. `chown` - Change file/directory ownership
5. `chmod` - Change file/directory permissions
6. `passwd` - Set/change passwords
7. `chsh` - Change default shell

### Permission Fundamentals
- **rwx** notation (read, write, execute)
- **Numeric values:** r=4, w=2, x=1
- **Three targets:** owner, group, others
- **Common patterns:** 644 (files), 755 (directories/executables)

### User Management Best Practices
- Always use `-m` to create home directories
- Always use `-r` when deleting to remove home directories
- Use `-a` with `-G` to append groups
- Set passwords immediately after user creation
- Use descriptive usernames and group names

### System Administration Mindset
- **Verify before executing** (especially with rm -rf)
- **Use sudo appropriately** (don't run as root)
- **Document your changes** (comments, logs)
- **Test in non-production** first
- **Understand implications** before making changes

---

## Final Notes

This lab provided hands-on experience with fundamental Linux system administration tasks. The skills learned here form the foundation for more advanced topics like:
- Automated provisioning
- Configuration management
- Security hardening
- Multi-user system management
- Enterprise directory services

**Remember:** Practice these commands until they become muscle memory. System administration is all about repetition and building good habits!

---

*End of Comprehensive Study Notes*
