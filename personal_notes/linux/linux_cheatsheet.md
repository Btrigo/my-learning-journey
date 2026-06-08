# Linux Notes

Comprehensive reference for commands, filesystem, permissions, networking, and troubleshooting.

---

## 1. The Linux Philosophy

**Everything is a file.** Hardware devices, running processes, network sockets, kernel state — all of it is exposed as files you can read, write, and interact with using the same commands. This is not a metaphor. `/dev/sda` is your disk. `/proc/meminfo` is live RAM data from the kernel. `/dev/null` is a black hole you can pipe output into.

**The terminal is the primary interface.** GUIs exist but most Linux administration — especially on servers — happens at the command line. Get comfortable here.

**Commands are composable.** Small tools that do one thing well, chained together with pipes (`|`). `ps aux | grep nginx | awk '{print $1}'` is three tools doing one job. This is the Unix way.

**Case sensitive.** `/etc/Hosts` and `/etc/hosts` are different files. `Brandon` and `brandon` are different users. Always.

---

## 2. The Filesystem Hierarchy (FHS)

Linux has one unified filesystem tree starting at `/` (root). There are no drive letters. Everything — including external drives, USB sticks, and network shares — is mounted somewhere under `/`.

```
/
├── bin/        Essential user binaries (ls, cp, cat, ping)
├── boot/       Kernel, bootloader (GRUB), initramfs
├── dev/        Device files (disks, terminals, /dev/null)
├── etc/        System-wide configuration files (plain text)
├── home/       User home directories (/home/brandon)
├── lib/        Shared libraries needed by /bin and /sbin
├── media/      Auto-mount point for removable media (USB, CD)
├── mnt/        Manual mount point for temporary mounts
├── opt/        Third-party/vendor software (self-contained)
├── proc/       Virtual filesystem — live kernel/process data
├── root/       Root user's home directory
├── run/        Runtime data (PIDs, sockets) — cleared on reboot
├── sbin/       System admin binaries (fdisk, reboot, ifconfig)
├── srv/        Data served by services (web, FTP)
├── sys/        Virtual filesystem — kernel hardware info
├── tmp/        Temporary files — cleared on reboot
├── usr/        User programs, libraries, documentation
│   ├── bin/    Most installed user commands live here
│   ├── sbin/   Most installed admin commands live here
│   ├── local/  Manually installed software (not via package manager)
│   └── share/  Shared data, man pages, icons
└── var/        Variable data that changes at runtime
    ├── log/    System and application logs
    ├── lib/    Application state/databases
    ├── spool/  Print and mail queues
    ├── cache/  Package manager cache, app caches
    └── www/    Web server root (nginx/apache default)
```

### Key Directories for Day-to-Day Work

| Directory | Why You Care |
|---|---|
| `/etc` | Every service config lives here as plain text. Misconfigured service? Start here. |
| `/var/log` | All logs. When something breaks, come here. |
| `/home/username` | User files, dotfiles, SSH keys |
| `/root` | Root user's home — separate from /home intentionally |
| `/tmp` | Safe scratch space. Gone on reboot. |
| `/opt` | Where vendor agents (CloudWatch, Splunk, etc.) often install |
| `/usr/local/bin` | Where you put custom scripts so they're on PATH |
| `/proc` | Live kernel data. Not real files on disk. |
| `/dev` | Hardware as files. `/dev/null` discards output silently. |

---

## 3. Navigation & Basic File Operations

### Moving Around

```bash
pwd                    # Print working directory — where am I?
ls                     # List files in current directory
ls -la                 # Long format + hidden files (dotfiles)
ls -lh                 # Human-readable file sizes
cd /var/log            # Change to absolute path
cd ~                   # Go to home directory
cd ..                  # Go up one level
cd -                   # Return to previous directory (underrated)
```

### Files & Directories

```bash
mkdir dirname          # Create a directory
mkdir -p a/b/c         # Create nested directories in one shot
touch file.txt         # Create empty file or update timestamp
cp file.txt /dest/     # Copy file
cp -r dir/ /dest/      # Copy directory recursively
mv file.txt newname    # Move or rename
rm file.txt            # Delete file (no recycle bin — gone is gone)
rm -rf dirname/        # Delete directory recursively (careful)
```

> **rm -rf has no undo.** Double-check your path before running it, especially as root.

### Viewing Files

```bash
cat file.txt           # Dump entire file to stdout
less file.txt          # Scrollable view (q=quit, /=search, G=end, g=top)
head -n 20 file.txt    # First 20 lines
tail -n 50 file.txt    # Last 50 lines
tail -f /var/log/syslog  # Follow file live — watch logs in real time
```

> **tail -f** is one of the most used commands in live troubleshooting. Keep a terminal open with this running while you reproduce an issue.

### Finding Files

```bash
find / -name "nginx.conf"          # Find a file by name anywhere
find /var/log -name "*.log"        # Find all .log files under /var/log
find /home -name "*.sh" -type f    # Find only files (not dirs) with .sh extension
find /tmp -mtime +7                # Files not modified in 7+ days
find / -size +100M                 # Files larger than 100MB
which nginx                        # Find where a command binary lives
whereis nginx                      # Find binary, source, and man page locations
```

---

## 4. Symbolic Links & Hard Links

Links let you create references to files or directories without duplicating them. Two types exist and they behave very differently.

### Symbolic Links (Symlinks)

A symlink is a pointer to another file or directory — like a shortcut. If the original is deleted, the symlink breaks.

```bash
ln -s /etc/nginx/nginx.conf ~/nginx.conf     # Create a symlink in home dir
ln -s /usr/bin/python3 /usr/local/bin/python # Make python point to python3
ls -la                                        # Symlinks show as: link -> target
```

Output example:
```
lrwxrwxrwx 1 root root  20 Jun 1 nginx.conf -> /etc/nginx/nginx.conf
```

The `l` at the start of permissions means symlink. The `->` shows what it points to.

### Hard Links

A hard link is a second directory entry pointing to the same underlying data on disk. Deleting the original does not destroy the data — it still exists via the hard link.

```bash
ln file.txt hardlink.txt     # Create a hard link (same inode, same data)
```

Hard links cannot span filesystems and cannot link to directories.

### Common Symlink Uses in Linux

```bash
# Web server config — enable a site by symlinking to sites-enabled
ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite

# Make a versioned binary accessible without the version number
ln -s /usr/bin/python3.11 /usr/local/bin/python3

# Point a custom log location to /var/log
ln -s /var/log/myapp /opt/myapp/logs

# Remove a symlink (do NOT use rm -rf on a symlink to a directory)
rm symlink.txt               # Correct way to remove a symlink
unlink symlink.txt           # Also correct
```

> When you see a path that seems odd or circular, run `ls -la` — there's probably a symlink involved.

---

## 5. Archives & Compression

### tar — Tape Archive (most common)

`tar` bundles files together. Combined with gzip or bzip2 it also compresses them.

```bash
# Create archives
tar -czf archive.tar.gz /path/to/dir/     # Create gzip-compressed archive
tar -cjf archive.tar.bz2 /path/to/dir/   # Create bzip2-compressed archive (smaller, slower)
tar -cf archive.tar /path/to/dir/         # Create uncompressed archive

# Extract archives
tar -xzf archive.tar.gz                   # Extract gzip archive here
tar -xzf archive.tar.gz -C /dest/        # Extract to a specific directory
tar -xjf archive.tar.bz2                  # Extract bzip2 archive

# View contents without extracting
tar -tzf archive.tar.gz                   # List contents of gzip archive

# Flags breakdown
# c = create  x = extract  t = list  v = verbose  f = filename
# z = gzip    j = bzip2    C = change to directory
```

> The flags `-czf` are the ones you'll type constantly. Just remember: **c**reate **z**ip **f**ile.

### gzip / gunzip

```bash
gzip file.txt              # Compress — creates file.txt.gz, removes original
gunzip file.txt.gz         # Decompress — restores file.txt
gzip -k file.txt           # Compress but keep the original
gzip -d file.txt.gz        # Same as gunzip
```

### zip / unzip

```bash
zip archive.zip file1 file2      # Create zip archive
zip -r archive.zip dir/          # Zip a directory recursively
unzip archive.zip                # Extract here
unzip archive.zip -d /dest/      # Extract to specific directory
unzip -l archive.zip             # List contents without extracting
```

### Quick Reference

| Format | Create | Extract |
|---|---|---|
| `.tar.gz` | `tar -czf out.tar.gz dir/` | `tar -xzf out.tar.gz` |
| `.tar.bz2` | `tar -cjf out.tar.bz2 dir/` | `tar -xjf out.tar.bz2` |
| `.tar` | `tar -cf out.tar dir/` | `tar -xf out.tar` |
| `.gz` | `gzip file` | `gunzip file.gz` |
| `.zip` | `zip -r out.zip dir/` | `unzip out.zip` |

---

## 6. Text Processing

### Searching Content

```bash
grep "error" /var/log/syslog              # Find lines containing "error"
grep -i "failed" /var/log/auth.log        # Case-insensitive search
grep -r "password" /etc/                  # Recursive search through directory
grep -n "error" file.log                  # Show line numbers
grep -v "debug" file.log                  # Invert — show lines NOT matching
grep -E "error|warn|crit" syslog          # Extended regex — match multiple patterns
```

### Pipes & Combining Commands

```bash
ps aux | grep nginx                        # Filter process list
cat /var/log/syslog | grep "error" | tail -20   # Chain: get errors, show last 20
ls -la | grep "^d"                         # Show only directories
```

> The pipe `|` takes the output of one command and feeds it as input to the next. This is core Linux — master it.

### Useful Text Tools

```bash
awk '{print $1, $4}' access.log    # Print specific columns (column tool)
sed 's/old/new/g' file.txt         # Find and replace in a file output
sed -i 's/old/new/g' file.txt      # Find and replace in-place (edits the file)
sort file.txt                      # Sort lines alphabetically
sort -n file.txt                   # Sort numerically
uniq -c                            # Count duplicate adjacent lines
wc -l file.txt                     # Count lines in a file
cut -d: -f1 /etc/passwd            # Cut by delimiter, grab field 1 (usernames)
```

### Redirecting Output

```bash
command > file.txt         # Redirect stdout to file (overwrites)
command >> file.txt        # Append stdout to file
command 2> errors.txt      # Redirect stderr only
command 2>/dev/null        # Discard errors silently
command &> file.txt        # Redirect both stdout and stderr
command | tee file.txt     # Output to terminal AND save to file simultaneously
```

> `/dev/null` is the black hole. Anything redirected there is discarded. Commonly used in scripts and cron jobs to suppress noisy output.

---

## 7. Vim — Survival Guide

Vim is a terminal text editor that is installed on almost every Linux system. You will end up in it eventually whether you want to or not. At minimum, know how to get out and make a basic edit.

### Modes

Vim has distinct modes — this is what trips people up. Keys do different things depending on which mode you're in.

| Mode | How to Enter | What It Does |
|---|---|---|
| Normal | `Esc` (always works) | Navigate, delete, copy, paste — default mode |
| Insert | `i` | Type and edit text like a normal editor |
| Visual | `v` | Select text |
| Command | `:` | Run commands (save, quit, search, replace) |

### The Essential Commands

```
# Getting in and out
i          Enter insert mode (start typing before cursor)
a          Enter insert mode (start typing after cursor)
Esc        Return to normal mode
:w         Save (write)
:q         Quit
:wq        Save and quit
:q!        Quit WITHOUT saving (force — use this to escape)
:wq!       Force save and quit

# Navigating in normal mode
h j k l    Left, down, up, right (arrow keys also work)
gg         Go to top of file
G          Go to bottom of file
:50        Go to line 50
Ctrl+f     Page down
Ctrl+b     Page up
w          Jump forward one word
b          Jump back one word

# Editing in normal mode
dd         Delete current line
yy         Copy (yank) current line
p          Paste below cursor
u          Undo
Ctrl+r     Redo
x          Delete character under cursor
dw         Delete word

# Search
/searchterm     Search forward (n = next match, N = previous)
?searchterm     Search backward

# Find and replace
:%s/old/new/g        Replace all occurrences in file
:%s/old/new/gc       Replace with confirmation for each
:10,20s/old/new/g    Replace only in lines 10-20
```

### The Workflow You'll Actually Use

1. Open a file: `vim /etc/nginx/nginx.conf`
2. Press `i` to enter insert mode
3. Make your edit
4. Press `Esc` to return to normal mode
5. Type `:wq` and press Enter to save and quit

If something goes wrong and you want out without saving: `Esc` then `:q!`

> If you accidentally end up in a mode you don't recognize, press `Esc` repeatedly until you're back in normal mode. Then `:q!` to exit without saving.

---

## 8. Bash Scripting Fundamentals

Scripts are how you automate repetitive tasks. At NOC/help desk level you'll read and modify scripts constantly. At cloud/infra level you'll write them.

### The Shebang & Basic Structure

```bash
#!/bin/bash
# This is a comment
# The shebang line tells the OS which interpreter to use

echo "Hello, world"
```

Save as `script.sh`, then make it executable:
```bash
chmod +x script.sh
./script.sh           # Run it
```

### Variables

```bash
#!/bin/bash

NAME="brandon"
AGE=25

echo "Name: $NAME"
echo "Age: $AGE"

# Command output into a variable
CURRENT_DIR=$(pwd)
echo "We are in: $CURRENT_DIR"

# User input
read -p "Enter your name: " USERNAME
echo "Hello, $USERNAME"
```

### Conditionals

```bash
#!/bin/bash

# if / elif / else
if [ "$1" == "hello" ]; then
    echo "You said hello"
elif [ "$1" == "bye" ]; then
    echo "You said bye"
else
    echo "You said something else"
fi

# Check if a file exists
if [ -f "/etc/nginx/nginx.conf" ]; then
    echo "nginx config exists"
fi

# Check if a directory exists
if [ -d "/var/log/nginx" ]; then
    echo "nginx log dir exists"
fi

# Check if a service is running
if systemctl is-active --quiet nginx; then
    echo "nginx is running"
else
    echo "nginx is NOT running"
fi
```

### Common Test Operators

| Operator | Meaning |
|---|---|
| `-f file` | File exists and is a regular file |
| `-d dir` | Directory exists |
| `-e path` | Path exists (file or directory) |
| `-z "$var"` | Variable is empty |
| `-n "$var"` | Variable is not empty |
| `$a == $b` | Strings are equal |
| `$a != $b` | Strings are not equal |
| `$a -eq $b` | Numbers are equal |
| `$a -gt $b` | a is greater than b |
| `$a -lt $b` | a is less than b |

### Loops

```bash
#!/bin/bash

# For loop — iterate over a list
for SERVER in web01 web02 web03; do
    echo "Checking $SERVER"
    ping -c 1 $SERVER
done

# For loop — iterate over files
for FILE in /var/log/*.log; do
    echo "Processing: $FILE"
done

# While loop
COUNT=0
while [ $COUNT -lt 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done

# Loop over lines in a file
while IFS= read -r line; do
    echo "$line"
done < /etc/hosts
```

### Functions

```bash
#!/bin/bash

check_service() {
    SERVICE=$1
    if systemctl is-active --quiet $SERVICE; then
        echo "$SERVICE is running"
    else
        echo "$SERVICE is DOWN"
    fi
}

# Call the function
check_service nginx
check_service sshd
check_service mysql
```

### Exit Codes & Error Handling

```bash
#!/bin/bash

# Every command returns an exit code: 0 = success, non-zero = failure
ls /nonexistent
echo "Exit code: $?"     # $? holds the last command's exit code

# Exit script on any error
set -e

# Exit on error, treat unset variables as errors, pipe failures
set -euo pipefail

# Check if a command succeeded
if ! apt install nginx -y; then
    echo "Install failed"
    exit 1
fi
```

### Practical Script Example — Service Health Check

```bash
#!/bin/bash
# check_services.sh — check if critical services are running

SERVICES=("nginx" "sshd" "cron")
FAILED=0

for SERVICE in "${SERVICES[@]}"; do
    if systemctl is-active --quiet $SERVICE; then
        echo "[OK]   $SERVICE"
    else
        echo "[FAIL] $SERVICE is not running"
        FAILED=$((FAILED + 1))
    fi
done

if [ $FAILED -gt 0 ]; then
    echo "$FAILED service(s) are down"
    exit 1
fi

echo "All services healthy"
exit 0
```

---

## 9. Permissions & Ownership

### Understanding Permission Bits

Every file has three permission sets: **owner**, **group**, **others**.
Each set has three bits: **read (r=4)**, **write (w=2)**, **execute (x=1)**.

```
-rwxr-xr--  1  brandon  devs  4096  Jun 1  script.sh
 ^^^         owner  group
 |||
 ||+-- others: r-- = 4 (read only)
 |+--- group:  r-x = 5 (read + execute)
 +---- owner:  rwx = 7 (read + write + execute)
```

The first character: `-` = file, `d` = directory, `l` = symlink.

### chmod — Change Permissions

```bash
chmod 755 script.sh        # rwxr-xr-x — standard for scripts/executables
chmod 644 file.txt         # rw-r--r-- — standard for regular files
chmod 600 private.key      # rw------- — private files (SSH keys)
chmod 700 ~/.ssh           # rwx------ — private directories
chmod +x script.sh         # Add execute bit (shorthand)
chmod -x script.sh         # Remove execute bit
chmod -R 755 /var/www/     # Apply recursively to directory
```

### chown — Change Ownership

```bash
chown brandon file.txt             # Change owner
chown brandon:devs file.txt        # Change owner and group
chown -R www-data:www-data /var/www/html/   # Recursive (common for web servers)
```

### Common Permission Scenarios

| Situation | Command |
|---|---|
| Script won't run | `chmod +x script.sh` |
| Web server can't read files | `chown -R www-data:www-data /var/www/` |
| SSH key permissions error | `chmod 600 ~/.ssh/id_rsa` |
| SSH directory permissions error | `chmod 700 ~/.ssh` |
| Make config readable only by owner | `chmod 600 /etc/app/secret.conf` |

### sudo — Run as Root

```bash
sudo command               # Run a single command as root
sudo -i                    # Open a root shell (be careful)
sudo -u otheruser command  # Run as a different user
sudo -l                    # List what the current user is allowed to run with sudo
su - username              # Switch to another user (requires their password)
```

> `sudo -l` is useful when you need to know your privilege scope on a shared system. Always use the minimum privilege needed.

### /etc/sudoers — Controlling sudo Access

**Always edit sudoers with `visudo`** — it validates syntax before saving. A typo in sudoers can lock everyone out of sudo.

```bash
sudo visudo                # Open sudoers file safely
```

### Sudoers Syntax

```bash
# Format: WHO  WHERE=(AS_WHO) WHAT
# Examples:

# Give brandon full sudo access (same as being in sudo group)
brandon ALL=(ALL:ALL) ALL

# Allow brandon to run specific commands only
brandon ALL=(ALL) /usr/bin/systemctl restart nginx, /usr/bin/systemctl status nginx

# Allow brandon to run without a password
brandon ALL=(ALL) NOPASSWD: ALL

# Allow the sudo group to run anything
%sudo ALL=(ALL:ALL) ALL

# Allow the devs group to restart web services without a password
%devs ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx, /usr/bin/systemctl restart apache2
```

Fields explained:
- `WHO` — username or `%groupname`
- `WHERE` — which hosts (ALL = any host, fine for most setups)
- `(AS_WHO)` — which user/group to run as (ALL:ALL = any user, any group)
- `WHAT` — which commands (ALL = everything, or comma-separated paths)

### Special Permissions

```bash
# setuid (s) — run as file owner regardless of who runs it
chmod u+s /usr/bin/passwd   # passwd runs as root so it can modify /etc/shadow

# setgid (s) on directory — new files inherit the directory's group
chmod g+s /shared/dir/

# sticky bit (t) — only file owner can delete in this directory
chmod +t /tmp               # /tmp uses this — you can't delete others' files there
```

---

## 10. Users & Groups

### User Management

```bash
useradd username                    # Create user (no home dir by default on some distros)
useradd -m -s /bin/bash username    # Create user with home dir and bash shell
useradd -m -G sudo username         # Create user and add to sudo group
passwd username                     # Set or change a user's password
userdel username                    # Delete user (keeps home directory)
userdel -r username                 # Delete user AND their home directory
usermod -aG groupname username      # Add user to a group (-a = append, don't replace)
usermod -s /bin/bash username       # Change a user's shell
```

> **usermod -aG** — the `-a` flag is critical. Without it, the user is REMOVED from all other groups and only put in the new one. Always use `-aG` together.

### Group Management

```bash
groupadd groupname                  # Create a group
groupdel groupname                  # Delete a group
groups username                     # Show what groups a user belongs to
id username                         # Show UID, GID, and all groups
```

### Key System Files

```bash
cat /etc/passwd       # User accounts (username:x:UID:GID:comment:home:shell)
cat /etc/shadow       # Hashed passwords (readable by root only)
cat /etc/group        # Group definitions (groupname:x:GID:members)
```

> Passwords are not stored in `/etc/passwd` — that `x` means the hash is in `/etc/shadow`. `/etc/passwd` is world-readable; `/etc/shadow` is not.

### Who Is Logged In

```bash
whoami                 # Current user
who                    # Who is logged into this system right now
w                      # Logged-in users + what they're doing
last                   # Login history
last -n 20             # Last 20 logins
lastb                  # Failed login attempts (bad logins)
```

---

## 11. Processes & Signals

### Viewing Processes

```bash
ps aux                          # Snapshot of all running processes
ps aux | grep nginx             # Find a specific process
top                             # Live process viewer (q=quit, M=sort by mem, P=sort by CPU)
htop                            # Better top — colored, mouse-friendly (may need to install)
pgrep nginx                     # Get PID of a process by name
```

### Linux Signals

Signals are how you communicate with running processes. `kill` sends signals — it doesn't just kill things.

| Signal | Number | Name | What It Does |
|---|---|---|---|
| SIGHUP | 1 | Hangup | Reload config without restarting (many daemons support this) |
| SIGINT | 2 | Interrupt | Same as Ctrl+C — polite stop |
| SIGTERM | 15 | Terminate | Graceful shutdown — default signal of `kill` |
| SIGKILL | 9 | Kill | Force kill — cannot be caught or ignored |

```bash
kill PID               # Send SIGTERM (15) — graceful stop
kill -15 PID           # Same as above, explicit
kill -1 PID            # Send SIGHUP — reload config
kill -9 PID            # Send SIGKILL — force kill, no cleanup
kill -HUP $(pidof nginx)           # Reload nginx config gracefully
kill -HUP $(cat /var/run/nginx.pid) # Same, using PID file

killall nginx          # Send SIGTERM to all processes named nginx
pkill -HUP nginx       # Send SIGHUP to processes named nginx
pkill -f "python script.py"   # Kill by matching full command string
```

> **SIGHUP is underused and underappreciated.** Many services (nginx, sshd, rsyslog) reload their config file on SIGHUP without restarting. This means zero downtime config reload: `kill -HUP $(pidof nginx)`. Use this instead of `systemctl restart` when you only changed config.

> Try SIGTERM first. If the process ignores it, then SIGKILL. SIGKILL gives the process no chance to flush buffers or close files cleanly — it can cause data corruption in databases.

### Background & Foreground Jobs

```bash
command &              # Run in background
jobs                   # List background jobs
fg %1                  # Bring job 1 to foreground
bg %1                  # Send job 1 to background
Ctrl + Z               # Suspend current foreground process
Ctrl + C               # Kill current foreground process (SIGINT)
nohup command &        # Run in background, keep running after logout
```

---

## 12. Networking

### View Network Configuration

```bash
ip a                           # All interfaces and IPs (modern — use this)
ip addr show eth0              # Specific interface
ip link show                   # Interface status (up/down)
ip route show                  # Routing table
ip route show default          # Just the default gateway
cat /etc/resolv.conf           # DNS server config
```

> `ifconfig` still exists on many systems but is deprecated. `ip` is the current standard.

### Connectivity Testing

```bash
ping -c 4 8.8.8.8              # Ping 4 times (Linux pings forever without -c)
ping -c 4 google.com           # Test DNS + connectivity
traceroute google.com          # Map hops to destination
mtr google.com                 # Live traceroute with packet loss per hop (better than traceroute)
```

> **Troubleshooting path (same as Windows):** loopback → gateway → 8.8.8.8 → google.com

### DNS

```bash
nslookup google.com                    # Basic DNS lookup
nslookup google.com 8.8.8.8           # Query a specific DNS server
dig google.com                         # Detailed DNS lookup (preferred on Linux)
dig google.com +short                  # Just the IP
dig @8.8.8.8 google.com               # Query specific DNS server with dig
dig -x 8.8.8.8                         # Reverse DNS lookup (IP to hostname)
cat /etc/resolv.conf                   # Which DNS servers is this machine using?
cat /etc/hosts                         # Static hostname overrides (checked before DNS)
```

> `/etc/hosts` is checked before DNS. If a hostname resolves wrong on one machine but fine on others, check `/etc/hosts` first.

### Open Ports & Connections

```bash
ss -tuln                       # Listening ports (TCP + UDP, no DNS resolution)
ss -tulnp                      # Same + process name/PID (requires sudo)
ss -tan                        # All TCP connections
netstat -tuln                  # Same as ss -tuln (older, still common)
lsof -i :80                    # What process is using port 80?
lsof -i :443                   # What process is using port 443?
```

> `ss` is the modern replacement for `netstat`. Both work. `lsof -i :PORT` is the fastest way to find what owns a specific port.

### Testing Port Connectivity

```bash
nc -zv 192.168.1.1 443         # Test if port 443 is open on a host (-z=scan -v=verbose)
nc -zv google.com 80           # Test port 80 on google.com
curl -I https://example.com    # HTTP HEAD request — check if web server responds
curl -v https://example.com    # Verbose — shows full request/response including headers
wget -q --spider https://example.com  # Check if URL is reachable without downloading
```

> `nc` (netcat) is the Linux equivalent of `Test-NetConnection -Port`. Know your ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL), 5432 (PostgreSQL), 6379 (Redis), 27017 (MongoDB).

### Network Configuration Files

| Distro Family | Network Config Location |
|---|---|
| Ubuntu 18.04+ | `/etc/netplan/*.yaml` |
| Debian (older) | `/etc/network/interfaces` |
| RHEL/CentOS 7 | `/etc/sysconfig/network-scripts/ifcfg-eth0` |
| RHEL/CentOS 8+ | NetworkManager via `nmcli` |

```bash
nmcli device status            # NetworkManager: show all devices
nmcli connection show          # List connections
nmcli con reload               # Reload connection config
```

### Firewall (iptables & firewalld & ufw)

```bash
# UFW (Ubuntu default — simpler)
ufw status                     # Is firewall enabled? What rules exist?
ufw allow 22                   # Allow SSH
ufw allow 80/tcp               # Allow HTTP
ufw deny 23                    # Block Telnet
ufw enable                     # Enable firewall
ufw disable                    # Disable firewall

# firewalld (RHEL/CentOS default)
firewall-cmd --state                        # Is firewalld running?
firewall-cmd --list-all                     # Show active rules
firewall-cmd --add-port=443/tcp --permanent # Open a port permanently
firewall-cmd --reload                       # Apply changes

# iptables (lower-level, still common)
iptables -L -n -v              # List all rules with packet counts
iptables -L INPUT -n           # Just the INPUT chain
```

---

## 13. Services & systemd

Modern Linux uses **systemd** as the init system. Services are managed with `systemctl`.

### Managing Services

```bash
systemctl status nginx              # Is nginx running? Any errors?
systemctl start nginx               # Start a service
systemctl stop nginx                # Stop a service
systemctl restart nginx             # Stop then start
systemctl reload nginx              # Reload config without full restart (if supported)
systemctl enable nginx              # Enable at boot
systemctl disable nginx             # Disable at boot
systemctl is-active nginx           # Returns "active" or "inactive"
systemctl is-enabled nginx          # Returns "enabled" or "disabled"
```

### Viewing All Services

```bash
systemctl list-units --type=service             # All loaded services
systemctl list-units --type=service --state=failed  # Only failed services
systemctl list-unit-files --type=service        # All service files + enabled status
```

### Writing a Basic systemd Unit File

Unit files live in `/etc/systemd/system/`. This is how you register a custom script or app as a service.

```ini
# /etc/systemd/system/myapp.service

[Unit]
Description=My Application
After=network.target          # Start after network is up
Wants=network.target

[Service]
Type=simple
User=brandon                  # Run as this user, not root
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/start.sh # Command to start the service
ExecReload=/bin/kill -HUP $MAINPID  # How to reload (optional)
Restart=on-failure            # Restart if it crashes
RestartSec=5                  # Wait 5 seconds before restarting
StandardOutput=journal        # Send stdout to journald
StandardError=journal

[Install]
WantedBy=multi-user.target    # Enable for normal multi-user boot
```

```bash
# After creating or editing a unit file:
systemctl daemon-reload        # Tell systemd to re-read unit files
systemctl enable myapp         # Enable at boot
systemctl start myapp          # Start now
systemctl status myapp         # Verify it's running
```

### systemd Logs (journalctl)

```bash
journalctl                              # All logs (oldest first — pipe to less)
journalctl -f                           # Follow live (like tail -f for the whole system)
journalctl -u nginx                     # Logs for a specific service
journalctl -u nginx -f                  # Follow a specific service live
journalctl -u nginx --since "1 hour ago"  # Recent logs for a service
journalctl -n 50                        # Last 50 lines of journal
journalctl -p err                       # Only error-level and above
journalctl --since "2024-01-01" --until "2024-01-02"  # Time range
journalctl -b                           # Logs since last boot
journalctl -b -1                        # Logs from previous boot
journalctl --vacuum-size=100M           # Clear old journal logs, keep newest 100MB
```

> On modern systemd distros (Ubuntu 20.04+, RHEL 8+), `journalctl -u servicename` is more useful than grepping `/var/log/syslog` for service-specific issues.

---

## 14. Disk & Storage

### Disk Space

```bash
df -h                          # Disk usage for all mounted filesystems (human-readable)
df -h /var                     # Disk usage for a specific path
du -sh /var/log/               # Size of a specific directory
du -sh /var/log/*              # Size of each item inside a directory
du -sh /* 2>/dev/null          # Size of each top-level directory (find what's eating space)
du -h --max-depth=1 /var/      # One level deep size breakdown
```

> **When disk is full:** `df -h` to find which filesystem, then `du -sh /*` drilling down to find the culprit.

### Disk Usage Sorted

```bash
du -sh /var/* | sort -h        # Sort directories by size (smallest to largest)
du -sh /var/* | sort -rh       # Sort largest to smallest (most useful)
```

### Filesystem & Mounts

```bash
lsblk                          # List block devices (disks and partitions) as a tree
fdisk -l                       # List all disks and partition tables (requires sudo)
mount                          # Show all currently mounted filesystems
mount /dev/sdb1 /mnt/data      # Mount a partition
umount /mnt/data               # Unmount
cat /etc/fstab                 # Persistent mount configuration (what mounts at boot)
```

> `/etc/fstab` controls what mounts at boot. A bad entry here can prevent the system from booting. Always test with `mount -a` before rebooting after editing.

### Inodes

```bash
df -i                          # Inode usage (a disk can be "full" of inodes but have free space)
```

> A filesystem can run out of inodes before running out of space — this happens when there are millions of tiny files. `df -h` shows free space but `df -i` shows free inodes.

---

## 15. Logs

### Traditional Log Files

```bash
/var/log/syslog          # General system log (Ubuntu/Debian)
/var/log/messages        # General system log (RHEL/CentOS)
/var/log/auth.log        # Authentication, sudo, SSH logins (Ubuntu/Debian)
/var/log/secure          # Same as auth.log on RHEL/CentOS
/var/log/kern.log        # Kernel messages
/var/log/dmesg           # Boot-time kernel messages
/var/log/apt/            # Package install history (Debian/Ubuntu)
/var/log/yum.log         # Package install history (RHEL/CentOS older)
/var/log/dnf.log         # Package install history (RHEL/CentOS 8+)
/var/log/nginx/          # Nginx access and error logs
/var/log/apache2/        # Apache access and error logs
/var/log/mysql/          # MySQL logs
```

### Reading Logs Effectively

```bash
tail -f /var/log/syslog                        # Follow live
tail -n 100 /var/log/auth.log                  # Last 100 lines
grep "Failed password" /var/log/auth.log       # Find failed SSH attempts
grep "error" /var/log/nginx/error.log          # Nginx errors
dmesg                                          # Kernel ring buffer (hardware issues, boot)
dmesg | grep -i error                          # Kernel errors
dmesg | tail -20                               # Recent kernel messages
```

---

## 16. SSH

### Connecting

```bash
ssh user@hostname              # Connect to a host
ssh user@192.168.1.50          # Connect by IP
ssh -p 2222 user@hostname      # Non-standard port
ssh -i ~/.ssh/mykey user@host  # Use a specific private key
ssh -v user@hostname           # Verbose — debug connection issues
```

### Key-Based Authentication Setup

```bash
ssh-keygen -t ed25519          # Generate an ED25519 key pair (modern, preferred)
ssh-keygen -t rsa -b 4096      # Generate an RSA 4096 key pair
ssh-copy-id user@hostname      # Copy your public key to a remote server's authorized_keys
```

Key files:
```
~/.ssh/id_ed25519       # Private key — never share this
~/.ssh/id_ed25519.pub   # Public key — this goes on the server
~/.ssh/authorized_keys  # Keys allowed to log in (on the server)
~/.ssh/known_hosts      # Fingerprints of hosts you've connected to
~/.ssh/config           # SSH client config (aliases, settings per host)
```

### SSH Key Permissions (Critical)

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
chmod 644 ~/.ssh/known_hosts
```

> SSH will refuse to use your key if the permissions are too open. This is a security feature, not a bug.

### SSH Config File (~/.ssh/config)

```
Host myserver
    HostName 192.168.1.50
    User brandon
    Port 2222
    IdentityFile ~/.ssh/mykey

Host jump-box
    HostName bastion.example.com
    User ec2-user
```

After setting this up: `ssh myserver` instead of `ssh -p 2222 brandon@192.168.1.50`

### Server-Side SSH Config (/etc/ssh/sshd_config)

```
Port 22                         # Port SSH listens on
PermitRootLogin no              # Never allow root to log in directly
PasswordAuthentication no       # Force key-based auth (more secure)
AllowUsers brandon              # Whitelist specific users
MaxAuthTries 3                  # Limit auth attempts
```

> After editing sshd_config: `sudo sshd -t` to check for syntax errors, then `sudo systemctl restart sshd`. A syntax error here with no check can lock you out.

### Copying Files Over SSH

```bash
scp file.txt user@host:/dest/           # Copy local file to remote
scp user@host:/remote/file.txt ./       # Copy remote file to local
scp -r dir/ user@host:/dest/            # Copy directory recursively
rsync -avz dir/ user@host:/dest/        # Sync directory (faster, resumable, preferred)
rsync -avz --delete dir/ user@host:/dest/  # Sync and delete files not in source
```

---

## 17. Package Management

### Debian/Ubuntu (apt)

```bash
apt update                      # Refresh package index (do this first, always)
apt upgrade                     # Upgrade all installed packages
apt install nginx               # Install a package
apt remove nginx                # Remove a package (keep config files)
apt purge nginx                 # Remove package + config files
apt autoremove                  # Remove unused dependency packages
apt search nginx                # Search for a package
apt show nginx                  # Show package details
dpkg -l                         # List all installed packages
dpkg -l | grep nginx            # Check if a specific package is installed
```

### RHEL/CentOS/Rocky (dnf/yum)

```bash
dnf update                      # Update all packages (dnf is yum's replacement)
dnf install nginx               # Install a package
dnf remove nginx                # Remove a package
dnf search nginx                # Search for a package
dnf info nginx                  # Show package details
rpm -qa                         # List all installed packages
rpm -qa | grep nginx            # Check if a specific package is installed
```

---

## 18. Environment & Shell

### Environment Variables

```bash
env                            # Show all environment variables
echo $PATH                     # Show PATH — where the shell looks for commands
echo $HOME                     # Home directory
echo $USER                     # Current username
export MYVAR="value"           # Set an environment variable for current session
echo $MYVAR                    # Use it
unset MYVAR                    # Remove it
```

### Shell Config Files

| File | When It Runs |
|---|---|
| `~/.bashrc` | Every interactive non-login shell (terminal window) |
| `~/.bash_profile` or `~/.profile` | Login shells (SSH, console login) |
| `/etc/profile` | System-wide, runs at login for all users |
| `/etc/bash.bashrc` | System-wide bashrc for all users |

```bash
source ~/.bashrc               # Reload bashrc without restarting terminal
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc  # Add to PATH permanently
```

### Aliases

```bash
alias ll='ls -la'              # Create a shortcut
alias grep='grep --color=auto' # Colored grep output
alias ..='cd ..'               # Quick navigation
```

Put aliases in `~/.bashrc` to make them permanent.

### Useful Shell Tricks

```bash
Ctrl + C          # Kill current process
Ctrl + Z          # Suspend current process
Ctrl + L          # Clear screen (same as clear)
Ctrl + R          # Reverse search command history
!!                # Repeat last command
!$                # Last argument of previous command
history           # Show command history
history | grep ssh  # Search history for ssh commands
```

---

## 19. Cron Jobs (Scheduled Tasks)

```bash
crontab -e                     # Edit current user's cron jobs
crontab -l                     # List current user's cron jobs
crontab -l -u brandon          # List another user's cron jobs (as root)
crontab -r                     # Remove all cron jobs (careful)
```

### Cron Syntax

```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0 and 7 = Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

```bash
# Examples
0 2 * * * /opt/backup.sh           # Every day at 2:00 AM
*/5 * * * * /usr/bin/check.sh      # Every 5 minutes
0 9 * * 1 /usr/bin/report.sh       # Every Monday at 9:00 AM
@reboot /opt/startup.sh            # Run once at system boot
```

System-wide cron jobs: `/etc/cron.d/`, `/etc/cron.daily/`, `/etc/cron.hourly/`

---

## 20. System Information

```bash
uname -a               # Kernel version, hostname, architecture
uname -r               # Just the kernel version
hostnamectl            # Hostname, OS, kernel, virtualization type
cat /etc/os-release    # OS name and version (works across all distros)
lscpu                  # CPU info
free -h                # RAM and swap usage (human-readable)
uptime                 # How long the system has been running + load averages
lspci                  # List PCI devices (GPUs, NICs, etc.)
lsusb                  # List USB devices
dmidecode              # Hardware info from BIOS/firmware (requires sudo)
```

### Load Average

`uptime` shows three numbers: 1-minute, 5-minute, 15-minute load averages. A load average equal to the number of CPU cores means the system is fully utilized. Higher means there are processes waiting for CPU.

```bash
nproc                  # Number of CPU cores
cat /proc/cpuinfo | grep "processor" | wc -l  # Also counts cores
```

---

## 21. AWS-Specific Linux Knowledge

If you're working on EC2 instances or any Linux host in AWS, these are things you need to know.

### EC2 Instance Metadata Service (IMDS)

Every EC2 instance has access to a special IP address — `169.254.169.254` — that serves live metadata about the instance. This is only reachable from within the instance itself.

```bash
# Base metadata endpoint
curl http://169.254.169.254/latest/meta-data/

# Specific metadata values
curl http://169.254.169.254/latest/meta-data/instance-id
curl http://169.254.169.254/latest/meta-data/instance-type
curl http://169.254.169.254/latest/meta-data/local-ipv4
curl http://169.254.169.254/latest/meta-data/public-ipv4
curl http://169.254.169.254/latest/meta-data/public-hostname
curl http://169.254.169.254/latest/meta-data/placement/availability-zone
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

> This is how EC2 instances know who they are and what region/AZ they're in. Also how IAM instance roles deliver temporary credentials — the credentials endpoint rotates them automatically.

### IMDSv2 (Token-Based — Required on Hardened Instances)

Many modern and hardened EC2 instances require IMDSv2 which uses a session token. The old single-step curl above won't work — you need to get a token first.

```bash
# Step 1: Get a token (valid for 21600 seconds = 6 hours)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Step 2: Use the token for all metadata requests
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id
```

### Common EC2 Log Locations

```bash
/var/log/cloud-init.log          # Cloud-init execution log (user data script output)
/var/log/cloud-init-output.log   # stdout/stderr from your user data script
/var/log/amazon/ssm/             # AWS Systems Manager agent logs
/opt/aws/amazon-cloudwatch-agent/logs/  # CloudWatch agent logs
```

> When a user data script doesn't run or runs incorrectly, `/var/log/cloud-init-output.log` is where you look first.

### AWS CLI on Linux

```bash
aws configure                          # Set up credentials and region
aws sts get-caller-identity            # Who am I? (test credentials)
aws s3 ls                              # List S3 buckets
aws s3 cp file.txt s3://mybucket/      # Upload a file
aws s3 sync ./dir s3://mybucket/dir/   # Sync a directory to S3
aws ec2 describe-instances             # List EC2 instances
aws ssm start-session --target i-1234567890abcdef0  # SSM session (no SSH needed)
```

### SSM Session Manager (SSH Without SSH)

AWS Systems Manager Session Manager lets you connect to EC2 instances without opening port 22 or managing SSH keys — as long as the SSM agent is running and the instance has the right IAM role.

```bash
# From your local machine (AWS CLI + session-manager-plugin required)
aws ssm start-session --target i-1234567890abcdef0

# Port forwarding through SSM (e.g. RDS on private subnet)
aws ssm start-session --target i-1234567890abcdef0 \
  --document-name AWS-StartPortForwardingSession \
  --parameters '{"portNumber":["3306"],"localPortNumber":["3306"]}'
```

> In AWS environments, SSM is increasingly preferred over SSH — no open ports, full audit trail in CloudTrail, IAM-controlled access.

---

## 22. Troubleshooting Playbooks

### User Can't Connect via SSH

1. Can you ping the host? `ping -c 4 <host>` — basic connectivity
2. Is SSH port open? `nc -zv <host> 22` — is SSH listening?
3. On the server: `systemctl status sshd` — is the service running?
4. On the server: `journalctl -u sshd -n 50` — any errors?
5. Check `/etc/ssh/sshd_config` — is PasswordAuthentication disabled? Is the user listed in AllowUsers?
6. Check `~/.ssh/authorized_keys` — is the public key in there?
7. Check permissions: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`
8. Try `ssh -v user@host` — verbose output shows exactly where it fails

### Service Not Starting

1. `systemctl status servicename` — what does the error say?
2. `journalctl -u servicename -n 50` — full log with error details
3. Check the config file for syntax errors:
   - nginx: `nginx -t`
   - apache: `apache2ctl configtest`
   - sshd: `sshd -t`
4. Check if the port is already in use: `ss -tulnp | grep :80`
5. Check file permissions: does the service user own its files?

### Disk Full

1. `df -h` — which filesystem is full?
2. `du -sh /* 2>/dev/null | sort -rh | head -20` — what's eating space at root?
3. Drill down: `du -sh /var/* | sort -rh`
4. Common culprits: `/var/log` (logs), `/tmp` (temp files), `/var/cache/apt` (package cache)
5. Clear apt cache: `apt clean` or `apt autoremove`
6. Clear old journal logs: `journalctl --vacuum-size=100M`
7. Find and remove old compressed logs: `find /var/log -name "*.gz" -delete`

### Can't Reach a Host

1. `ping -c 4 127.0.0.1` — loopback working?
2. `ping -c 4 $(ip route show default | awk '/default/ {print $3}')` — gateway reachable?
3. `ping -c 4 8.8.8.8` — internet reachable by IP?
4. `ping -c 4 google.com` — DNS working?
5. `cat /etc/resolv.conf` — what DNS servers are configured?
6. `dig google.com` — detailed DNS test
7. `ip route show` — is there a default route?

### High CPU or Memory

1. `top` or `htop` — what process is consuming resources?
2. `ps aux --sort=-%cpu | head -20` — top CPU consumers
3. `ps aux --sort=-%mem | head -20` — top memory consumers
4. `free -h` — is there still free RAM? Is swap being used heavily?
5. `vmstat 1 5` — 5-second snapshot of CPU, memory, disk, and swap activity
6. Check for zombie processes: `ps aux | grep Z`

---

## 23. Key Config Files Quick Reference

| File | Purpose |
|---|---|
| `/etc/hosts` | Static hostname → IP mappings (checked before DNS) |
| `/etc/resolv.conf` | DNS server configuration |
| `/etc/hostname` | Machine's hostname |
| `/etc/fstab` | Filesystem mount table (what mounts at boot) |
| `/etc/passwd` | User account info (no passwords — those are in shadow) |
| `/etc/shadow` | Hashed passwords (root-readable only) |
| `/etc/group` | Group definitions and membership |
| `/etc/sudoers` | Who can run what with sudo (edit with `visudo` only) |
| `/etc/ssh/sshd_config` | SSH server configuration |
| `/etc/crontab` | System-wide cron jobs |
| `/etc/environment` | System-wide environment variables |
| `/etc/profile` | System-wide shell config (login shells) |
| `/etc/apt/sources.list` | Package repositories (Debian/Ubuntu) |
| `/etc/yum.repos.d/` | Package repositories (RHEL/CentOS) |
| `/etc/systemd/system/` | Custom systemd unit files live here |

> **Always edit `/etc/sudoers` with `visudo`** — it validates syntax before saving. A syntax error in sudoers can lock everyone out of sudo permanently.

---

## 24. Personal Notes

- Everything is a file — disks, devices, processes, kernel state. This isn't abstract; internalize it.
- `/proc` and `/dev` are virtual — nothing there is stored on disk. They exist only while the system is running.
- On modern Linux, `systemctl` and `journalctl` are your primary tools for services and logs — not the old `service` command and scattered log files.
- `ip` has replaced `ifconfig`. `ss` has replaced `netstat`. Both old tools still work on most systems but learn the new ones.
- Permissions matter more on Linux than Windows. Wrong permissions break services in ways that aren't always obvious.
- `/etc/hosts` is checked before DNS — a lifesaver and a footgun depending on the situation.
- Cron and systemd timers are how scheduled tasks work. Know both.
- sudo is not the same as root. sudo runs one command elevated. `sudo -i` gives you a root shell — use it sparingly.
- SSH key auth is the standard. Password auth should be disabled on any internet-facing server.
- SIGHUP reloads config without restarting — prefer it over restart when only config changed.
- Symlinks are everywhere in Linux — when something seems wrong with a path, check with `ls -la` for arrows.
- Bash scripting and Linux admin are the same skill at different levels of abstraction. Every script you write makes you a better admin.
- The AWS metadata endpoint `169.254.169.254` is Linux-only knowledge that maps directly to EC2 work.
- When in doubt: `man commandname` — the manual pages are built in and usually excellent.

---