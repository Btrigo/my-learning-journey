# Linux File System - Comprehensive Notes

## Table of Contents
1. [File System Overview](#file-system-overview)
2. [Directory Structure](#directory-structure)
3. [Important Directories Explained](#important-directories-explained)
4. [File Types](#file-types)
5. [Paths: Absolute vs Relative](#paths-absolute-vs-relative)
6. [File System Concepts](#file-system-concepts)
7. [Practical Examples](#practical-examples)
8. [Quick Reference](#quick-reference)

---

## File System Overview

### What is a File System?

A file system is how your operating system organizes, stores, and retrieves data on storage devices. Think of it like a filing cabinet system for your computer.

**Key Concepts:**
- Everything in Linux is a file (even directories and devices!)
- Single hierarchical tree structure starting from root (`/`)
- Case-sensitive: `File.txt` and `file.txt` are different files
- No drive letters (C:, D:) like Windows - everything under one root

---

## Directory Structure

### The Linux File System Hierarchy

```
/                           Root - Top of everything
├── bin/                    Essential command binaries
├── boot/                   Boot loader files
├── dev/                    Device files
├── etc/                    System configuration files
├── home/                   User home directories
│   ├── alice/
│   ├── bob/
│   └── charlie/
├── lib/                    System libraries
├── media/                  Removable media mount points
├── mnt/                    Temporary mount points
├── opt/                    Optional/third-party software
├── proc/                   Process and kernel info
├── root/                   Root user's home directory
├── run/                    Runtime data
├── sbin/                   System binaries
├── srv/                    Service data
├── sys/                    Kernel and system info
├── tmp/                    Temporary files
├── usr/                    User programs and data
│   ├── bin/                User command binaries
│   ├── lib/                User libraries
│   ├── local/              Locally installed software
│   └── share/              Shared data
└── var/                    Variable data (logs, mail)
    ├── log/                Log files
    ├── mail/               User mailboxes
    └── tmp/                Temporary files
```

---

## Important Directories Explained

### `/` (Root)
- **The top of everything**
- All other directories branch from here
- Not to be confused with `/root` (root user's home)

```bash
cd /        # Go to root directory
ls /        # List everything at root level
```

---

### `/home` - User Home Directories
- **Where user files live**
- Each user gets their own directory: `/home/username`
- Personal documents, downloads, desktop, etc.

```bash
/home/alice/Documents
/home/alice/Downloads
/home/alice/.bashrc        # Hidden config files start with .
```

**Current user's home:**
```bash
cd ~        # Shortcut to your home directory
cd          # Also goes to home
pwd         # Should show /home/yourusername
```

---

### `/root` - Root User's Home
- **Home directory for the root (admin) user**
- NOT the same as `/` (root directory)
- Regular users can't access this

```bash
# Only root can access
sudo ls /root
```

---

### `/bin` - Essential Binaries
- **Critical system commands**
- Available to all users
- Commands needed to boot and run the system

```bash
ls /bin
# Contains: ls, cp, mv, rm, cat, bash, etc.
```

---

### `/sbin` - System Binaries
- **System administration commands**
- Usually require root/sudo
- System maintenance tools

```bash
ls /sbin
# Contains: fdisk, fsck, reboot, shutdown, etc.
```

---

### `/usr` - User Programs
- **Most user applications and utilities**
- Secondary hierarchy (mirror of /)
- READ-ONLY for regular users

**Important subdirectories:**
```
/usr/bin/       User commands (not essential for boot)
/usr/sbin/      System admin commands (not essential)
/usr/lib/       Libraries for /usr/bin and /usr/sbin
/usr/local/     Locally compiled/installed software
/usr/share/     Architecture-independent data
```

---

### `/usr/local` - Locally Installed Software
- **Programs you compile yourself**
- Not managed by package manager
- Keeps custom software separate from system software

```bash
/usr/local/bin/         Custom executables
/usr/local/lib/         Custom libraries
/usr/local/share/       Custom shared data
```

---

### `/etc` - Configuration Files
- **System-wide configuration**
- Text-based config files
- Most important configs live here

**Key files:**
```bash
/etc/passwd             User accounts
/etc/shadow             Encrypted passwords
/etc/group              Group information
/etc/fstab              File system mount config
/etc/hosts              Hostname to IP mappings
/etc/hostname           System hostname
/etc/ssh/               SSH configuration
/etc/apt/               Package manager config (Ubuntu/Debian)
```

---

### `/var` - Variable Data
- **Data that changes frequently**
- Logs, databases, mail, caches
- Can grow large over time

**Important subdirectories:**
```bash
/var/log/               System and application logs
/var/mail/              User mailboxes
/var/tmp/               Temp files preserved between reboots
/var/cache/             Application cache
/var/lib/               State information for programs
```

**Common use:**
```bash
# View system logs
sudo tail -f /var/log/syslog

# Check mail
ls /var/mail/
```

---

### `/tmp` - Temporary Files
- **Temporary file storage**
- Cleared on reboot (usually)
- World-writable (any user can write)

```bash
# Create temp file
echo "test" > /tmp/mytemp.txt

# Anyone can create files here
```

---

### `/opt` - Optional Software
- **Third-party applications**
- Self-contained packages
- Not managed by system package manager

```bash
/opt/google/chrome/
/opt/vmware/
/opt/teamviewer/
```

**From your lab notes:** You learned about this today!

---

### `/boot` - Boot Loader Files
- **Files needed to boot the system**
- Kernel, initrd, bootloader config
- DON'T delete anything here!

```bash
ls /boot
# Contains: vmlinuz (kernel), initrd.img, grub config
```

---

### `/dev` - Device Files
- **Hardware device representations**
- Disks, terminals, USB devices
- Special files that represent hardware

**Common devices:**
```bash
/dev/sda            First hard drive
/dev/sda1           First partition on first drive
/dev/sdb            Second hard drive
/dev/null           Black hole (discards all input)
/dev/zero           Produces infinite zeros
/dev/random         Random data generator
/dev/tty            Current terminal
```

**Examples:**
```bash
# List all block devices (disks)
lsblk

# Discard output (send to black hole)
command > /dev/null

# Generate random data
head -c 100 /dev/random
```

---

### `/proc` - Process Information
- **Virtual file system**
- Kernel and process information
- Not real files - generated on-the-fly

```bash
# CPU information
cat /proc/cpuinfo

# Memory information
cat /proc/meminfo

# Process info (PID 1234)
ls /proc/1234/
```

---

### `/sys` - System Information
- **Virtual file system**
- Kernel and hardware information
- Used by system tools

```bash
# View system info
ls /sys/class/net/      # Network interfaces
ls /sys/block/          # Block devices
```

---

### `/media` - Removable Media
- **Auto-mount point for removable media**
- USB drives, CDs, external drives
- System manages this automatically

```bash
/media/username/USB_DRIVE/
/media/username/DVD/
```

---

### `/mnt` - Mount Points
- **Temporary manual mount points**
- Admins mount file systems here
- You control this (not automatic)

```bash
# Mount a drive manually
sudo mount /dev/sdb1 /mnt/mydrive

# Unmount
sudo umount /mnt/mydrive
```

**From your lab:** You'll use this for partition mounting!

---

### `/lib` and `/lib64` - System Libraries
- **Shared libraries**
- Like DLL files in Windows
- Required by binaries in /bin and /sbin

```bash
ls /lib
# Contains: libc.so.6, libm.so.6, etc.
```

---

### `/srv` - Service Data
- **Data for services**
- Web servers, FTP servers
- Not commonly used

```bash
/srv/www/               Web server data
/srv/ftp/               FTP server data
```

---

## File Types

### Everything is a File in Linux!

Linux treats almost everything as a file, including:
- Regular files
- Directories
- Devices
- Sockets
- Links

### File Type Indicators (from `ls -l`)

```bash
$ ls -l
-rw-r--r--  Regular file
drwxr-xr-x  Directory
lrwxrwxrwx  Symbolic link
brw-rw----  Block device (disk)
crw-rw----  Character device (terminal)
prw-r--r--  Named pipe (FIFO)
srwxrwxrwx  Socket
```

**First character tells you the type:**
- `-` = Regular file
- `d` = Directory
- `l` = Symbolic link (shortcut)
- `b` = Block device (disk)
- `c` = Character device (terminal, printer)
- `p` = Pipe
- `s` = Socket

---

## Paths: Absolute vs Relative

### Absolute Paths
**Start from root (`/`)**
- Always begins with `/`
- Unambiguous - works from anywhere
- Full path from top of file system

```bash
/home/alice/Documents/report.txt
/etc/passwd
/var/log/syslog
/usr/bin/python3

# Works from any directory
cd /home/alice/Documents
cat /etc/passwd
```

---

### Relative Paths
**Start from current directory**
- No leading `/`
- Depends on where you are
- Shorter, but location-dependent

```bash
# If you're in /home/alice
cd Documents            # Goes to /home/alice/Documents
cat file.txt            # Opens /home/alice/file.txt

# If you're in /home/bob
cd Documents            # Goes to /home/bob/Documents
cat file.txt            # Opens /home/bob/file.txt (different file!)
```

---

### Special Path Symbols

| Symbol | Meaning | Example |
|--------|---------|---------|
| `.` | Current directory | `./script.sh` |
| `..` | Parent directory | `cd ..` |
| `~` | Home directory | `cd ~` or `~/Documents` |
| `/` | Root directory | `/etc` |
| `-` | Previous directory | `cd -` |

**Examples:**
```bash
pwd                     # /home/alice/Documents/Work

cd ..                   # Go up: /home/alice/Documents
cd ../..                # Go up twice: /home/alice
cd ../../bob            # Go up twice, then into bob: /home/bob

cd ~                    # Go home: /home/alice
cd ~/Documents          # Go to your Documents: /home/alice/Documents

cd /tmp                 # Absolute path
cd -                    # Go back to previous directory
```

---

### Path Examples in Action

```bash
# Starting point
$ pwd
/home/alice

# Absolute path - always works
$ cat /etc/passwd
# ✓ Works!

# Relative path - depends on location
$ cat Documents/report.txt
# ✓ Works (from /home/alice)

$ cd /tmp
$ cat Documents/report.txt
# ✗ ERROR - no Documents here!

# Using .. to go up
$ pwd
/home/alice/Documents/Projects/WebApp
$ cd ../..
$ pwd
/home/alice/Documents

# Using ~ for home
$ cd /var/log
$ cd ~/Documents
$ pwd
/home/alice/Documents
```

---

## File System Concepts

### 1. Hidden Files
Files/directories starting with `.` are hidden

```bash
ls             # Doesn't show hidden files
ls -a          # Shows ALL files including hidden

.bashrc        # Hidden config file
.ssh/          # Hidden directory
```

---

### 2. Inodes
- Every file has an inode (index node)
- Contains metadata: permissions, owner, timestamps, location
- The actual "pointer" to file data

```bash
# View inode numbers
ls -li

# Output:
# 1234567 -rw-r--r-- 1 alice alice 1024 Dec 16 file.txt
#   ↑ inode number
```

---

### 3. Hard Links vs Symbolic Links

**Hard Link:**
- Multiple names for the same inode
- Deleting one doesn't affect others
- Can't cross file systems

```bash
ln file.txt hardlink.txt
# Both point to same data
```

**Symbolic Link (Symlink):**
- Like a Windows shortcut
- Points to another file's path
- Can cross file systems
- Breaks if original is deleted

```bash
ln -s file.txt symlink.txt
# symlink.txt -> file.txt
```

---

### 4. File System Types

**Common Linux file systems:**
- **ext4** - Most common, default for many distros
- **ext3** - Older, still widely used
- **xfs** - High performance, large files
- **btrfs** - Modern, copy-on-write
- **vfat/fat32** - USB drives, Windows compatibility
- **ntfs** - Windows file system

**View file system types:**
```bash
df -T          # Show mounted file systems with types
lsblk -f       # Show block devices with file systems
```

---

### 5. Mount Points

**Mounting** = Attaching a file system to a directory

```bash
# View all mounted file systems
mount
df -h

# Mount a USB drive
sudo mount /dev/sdb1 /media/usb

# Unmount
sudo umount /media/usb
```

**From your lab notes:** You'll learn more about mounting and `/etc/fstab`!

---

## Practical Examples

### Example 1: Exploring the File System

```bash
# Start at root
cd /

# List top-level directories
ls -l

# Check home directory
cd /home
ls

# View your home
cd ~
pwd

# Check system configs
ls /etc

# View logs (requires sudo)
sudo ls /var/log
```

---

### Example 2: Understanding Paths

```bash
# Where am I?
pwd
# Output: /home/alice

# Absolute path - go to /etc
cd /etc
pwd
# Output: /etc

# Relative path - go to ssh subdirectory
cd ssh
pwd
# Output: /etc/ssh

# Go up one level
cd ..
pwd
# Output: /etc

# Go home
cd ~
pwd
# Output: /home/alice
```

---

### Example 3: Finding Files

```bash
# Find all .txt files in your home
find ~ -name "*.txt"

# Find files by user
find /home -user alice

# Locate command (faster, uses database)
locate filename

# Which command (find executables)
which python3
# Output: /usr/bin/python3
```

---

### Example 4: Disk Usage

```bash
# How much space is used?
df -h

# Size of directory
du -sh /home/alice

# Largest directories in current dir
du -h --max-depth=1 | sort -hr
```

---

## Quick Reference

### Essential Navigation Commands

| Command | What It Does |
|---------|--------------|
| `pwd` | Print working directory (where am I?) |
| `cd /path` | Change directory |
| `cd` or `cd ~` | Go home |
| `cd ..` | Go up one level |
| `cd -` | Go to previous directory |
| `ls` | List files |
| `ls -la` | List all files with details |

---

### Path Shortcuts

| Symbol | Meaning |
|--------|---------|
| `/` | Root directory |
| `~` | Your home directory |
| `.` | Current directory |
| `..` | Parent directory |
| `-` | Previous directory |

---

### Important Directories Summary

| Directory | Purpose | Example |
|-----------|---------|---------|
| `/` | Root - top of everything | - |
| `/home` | User home directories | `/home/alice` |
| `/root` | Root user's home | - |
| `/etc` | System configuration | `/etc/passwd` |
| `/var` | Variable data (logs) | `/var/log/syslog` |
| `/tmp` | Temporary files | `/tmp/test.txt` |
| `/usr` | User programs | `/usr/bin/python3` |
| `/opt` | Optional software | `/opt/google/chrome` |
| `/bin` | Essential commands | `/bin/ls` |
| `/sbin` | System commands | `/sbin/fdisk` |
| `/dev` | Device files | `/dev/sda1` |
| `/mnt` | Temp mount points | `/mnt/usb` |
| `/media` | Removable media | `/media/alice/USB` |
| `/boot` | Boot files | `/boot/vmlinuz` |
| `/lib` | System libraries | `/lib/x86_64-linux-gnu` |
| `/proc` | Process info (virtual) | `/proc/cpuinfo` |
| `/sys` | System info (virtual) | `/sys/class/net` |

---

## Key Takeaways

1. **Everything starts at `/` (root)**
2. **Your files live in `/home/username`**
3. **System configs are in `/etc`**
4. **Logs are in `/var/log`**
5. **Commands are in `/bin`, `/sbin`, `/usr/bin`**
6. **Absolute paths start with `/`, relative paths don't**
7. **`.` = here, `..` = up one level, `~` = home**
8. **Everything in Linux is a file (even devices!)**

---

## Connection to Your Lab

From your Linux System Administration lab, you learned:
- Users have home directories in `/home/username`
- Configuration files in `/etc/passwd`, `/etc/shadow`, `/etc/group`
- Temporary mounts go in `/mnt`
- Optional software in `/opt`
- Mail stored in `/var/mail`

Now you understand **where** these fit in the overall file system structure!

---

## Practice Exercises

### Exercise 1: Explore Your System
```bash
# Start at root
cd /

# List top-level directories
ls -l

# Go to your home
cd ~

# Where are you?
pwd

# List hidden files
ls -a
```

### Exercise 2: Practice Paths
```bash
# Go to /etc using absolute path
cd /etc

# Go to ssh using relative path
cd ssh

# Go up two levels using ..
cd ../..

# Go home
cd ~
```

### Exercise 3: Find Things
```bash
# Find your shell config
ls ~/.bashrc

# View system info
cat /etc/os-release

# Check disk usage
df -h

# View running processes (virtual file system!)
ls /proc
```

---

## Additional Resources

**Man pages (built-in help):**
```bash
man ls          # Learn about ls
man find        # Learn about find
man hier        # File system hierarchy description!
```

**Useful commands to explore:**
```bash
tree /          # Visual tree of file system (may need to install)
ncdu ~          # Interactive disk usage (may need to install)
whereis command # Find command location
file filename   # Identify file type
stat filename   # Detailed file info
```

---

*End of Linux File System Notes*