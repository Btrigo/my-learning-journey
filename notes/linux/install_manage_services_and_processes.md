# Linux Services and Processes - Comprehensive Study Notes

## Table of Contents
1. [Package Management](#package-management)
2. [Linux Repositories](#linux-repositories)
3. [Services Management](#services-management)
4. [Process Management](#process-management)
5. [Background and Foreground Processes](#background-and-foreground-processes)
6. [Process Priorities](#process-priorities)
7. [Troubleshooting Processes](#troubleshooting-processes)

---

## Package Management

### Core Concepts

**Application vs Package**
- **Application**: Software that can be installed and run on the operating system (e.g., web browsers, FTP servers, text editors)
- **Package**: Installation files created for specific Linux distributions containing the application and its metadata
  - Same application may have different packages for different distributions
  - Example: Google Chrome provides different packages for Debian/Ubuntu (.deb) vs Fedora/openSUSE (.rpm)

**Package Manager**
- A tool that allows users to install, remove, upgrade, configure, and manage software packages on the OS
- Handles dependencies and package relationships
- Different distributions use different package managers

### Package Management Systems by Distribution Family

**Debian Family (Debian, Ubuntu, Linux Mint)**
- Package format: `.deb`
- Package managers:
  - `dpkg` - Low-level package manager
  - `apt-get` / `apt` - High-level package manager

**Fedora Family (Fedora, RHEL, CentOS)**
- Package format: `.rpm`
- Package managers:
  - `rpm` - Low-level package manager
  - `yum` / `dnf` - High-level package manager

**SUSE Family (openSUSE, SUSE Linux Enterprise)**
- Package format: `.rpm`
- Package managers:
  - `rpm` - Low-level package manager
  - `zypper` - High-level package manager

### dpkg vs apt-get/apt

**dpkg (Debian Package Manager)**
- Low-level package manager
- Works directly with `.deb` files
- **Cannot** automatically download and install dependencies
- Must have the `.deb` file already downloaded

**Common dpkg Commands:**
```bash
dpkg --list                      # List all installed packages
sudo dpkg --install package.deb  # Install a .deb package
dpkg --status package_name       # Check package installation status
sudo dpkg --remove package_name  # Remove a package (keeps config files)
sudo dpkg --purge package_name   # Remove package and config files
```

**apt-get/apt (Advanced Package Tool)**
- High-level package manager
- **Does NOT** work directly with `.deb` files
- Works with package names from repositories
- **Automatically** resolves and installs dependencies
- Downloads packages from configured repositories

**Common apt Commands:**
```bash
apt search package_name          # Search for packages (searches descriptions)
apt-cache search -n package_name # Search package names only
sudo apt update                  # Update local package cache from repositories
sudo apt install package_name    # Install a package with dependencies
sudo apt remove package_name     # Remove a package
sudo apt upgrade                 # Upgrade all installed packages
apt list -a package_name         # List all available versions of a package
```

**IMPORTANT: Always run `sudo apt update` before installing packages**
- Updates the local package cache with latest repository information
- Prevents issues with outdated or non-existent packages

### Installing Firefox Example
```bash
# Search for Firefox
apt search firefox

# Update package cache (best practice)
sudo apt update

# Install Firefox
sudo apt install firefox
# Password for sudo: P@ssw0rd (in lab environment)

# Launch Firefox
firefox
# Or: Applications → Internet → Firefox Web Browser
```

---

## Linux Repositories

### What is a Repository?

A **repository** (repo) is a storage location from which a Linux system retrieves and installs OS updates and applications. Think of it as an app store or marketplace for Linux.

**Types of Repositories:**
- **Official distribution repositories**: Maintained by the distribution developers
- **Third-party repositories**: Maintained by software vendors or community

### Adding Repositories

**add-apt-repository Command**
- Python script that adds APT repositories
- Adds repository entries to:
  - `/etc/apt/sources.list` (main file)
  - `/etc/apt/sources.list.d/` (directory for separate repo files)

**Syntax:**
```bash
add-apt-repository [options] repository
apt-add-repository <repository_url>
```

### MongoDB Installation Example (Custom Repository)

```bash
# Method 1: Using echo and tee
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

# Update package cache to include new repository
sudo apt update

# Install MongoDB from the new repository
sudo apt install -y mongodb-org

# Verify installation
apt list -a mongodb-org
```

**Explanation:**
- `echo` - Outputs the repository line
- `|` - Pipes the output to the next command
- `sudo tee` - Writes the output to the file with elevated privileges
- Repository line format: `deb <url> <distribution> <component>`
- After adding repository, must run `apt update` before installing packages

---

## Services Management

### What is a Service?

A **service** is a program that runs continuously in the background, waiting for requests and responding to them. Services are also called **daemons**.

**Key Characteristics:**
- Run continuously in the background
- Start automatically at boot (if enabled)
- Listen for incoming requests
- Provide specific functionality (web serving, network management, etc.)

**Daemon Naming Convention:**
- Most (but not all) daemons end with the letter "d"
- Examples:
  - `httpd` - Apache HTTP server
  - `sshd` - SSH server for remote connections
  - `bluetoothd` - Bluetooth service
  - `network-manager` - Network management service

### Services vs Processes vs Applications

**Application**
- User-facing software meant to be directly used by users
- Example: Calculator, Firefox, text editor

**Service (Daemon)**
- Background programs providing always-on functionality
- Example: Web server (Apache), SSH server, Bluetooth service

**Process**
- Any running instance of a program in memory
- Both applications and services run as processes
- A service is a group of processes running continuously in the background

### Why Services Matter for Servers

On servers, services are the primary type of program running:
- Web servers host web pages (Apache, Nginx)
- Database servers handle data storage (MySQL, PostgreSQL)
- SSH servers enable remote access
- Users connect via IP or domain name to access these services

### Service Management with systemctl

**systemctl** is the command used to manage services in modern Linux distributions using systemd.

**Core systemctl Commands:**

```bash
# Check service status
systemctl status service_name
# Shows: active (running), inactive (dead), enabled/disabled

# Start a service (immediate action)
sudo systemctl start service_name

# Stop a service (immediate action)
sudo systemctl stop service_name

# Restart a service
sudo systemctl restart service_name

# Enable a service (auto-start at boot)
sudo systemctl enable service_name

# Disable a service (prevent auto-start at boot)
sudo systemctl disable service_name

# List all services
systemctl list-unit-files --type service --all

# List running services only
systemctl | grep running
```

**CRITICAL DISTINCTION:**
- **start/stop**: Immediate action (affects running state RIGHT NOW)
- **enable/disable**: Boot behavior (affects what happens AFTER REBOOT)

**To ensure a service runs and survives reboots:**
```bash
sudo systemctl start service_name    # Start now
sudo systemctl enable service_name   # Start on every boot
```

### Apache2 Web Server Example

**Testing Localhost Connection:**
- IP address `127.0.0.1` is the localhost/loopback address
- Connects a computer to itself over the network
- Used for testing network services locally
- URL: `http://127.0.0.1`

**Apache2 Service Management:**

```bash
# Check Apache status
systemctl status apache2
# Look for: Active: active (running) in bold green

# Stop Apache
sudo systemctl stop apache2
systemctl status apache2
# Shows: Active: inactive (dead)
# Browser shows: "Unable to connect"

# Disable Apache (survives reboot)
sudo systemctl disable apache2
# Reboot system
# After reboot: service still stopped

# Start Apache
sudo systemctl start apache2
systemctl status apache2
# Shows: Active: active (running)
# Browser shows: Apache2 Default Page
# BUT: Will NOT survive reboot

# Enable Apache (auto-start on boot)
sudo systemctl enable apache2
# Now service will start automatically after reboot
```

**Creating Custom Web Page:**
```bash
# Apache web root directory
cd /var/www/html

# Create custom HTML file
sudo nano brandon.html

# Access in browser
http://127.0.0.1/brandon.html
```

---

## Process Management

### What is a Process?

A **process** is a running instance of a program or program code loaded in memory. Every program that executes becomes one or more processes.

**Process Characteristics:**
- Has a unique Process ID (PID)
- Has a Parent Process ID (PPID)
- Consumes system resources (CPU, memory)
- Has an execution state
- Has an owner (user who started it)

### Process Hierarchy

**The init Process (PID 1)**
- First process started by the kernel during boot
- Has PID = 1
- Has PPID = 0 (no parent - started by kernel)
- The "grandfather" of all processes
- All other processes can trace their lineage back to init

**Parent-Child Relationships:**
- Every process (except init) is started by another process
- The starting process = parent
- The started process = child
- A child's PPID equals its parent's PID
- A parent can have multiple children
- A child can only have one parent
- Process lineage can extend to multiple levels

**Example Hierarchy:**
```
init (PID=1, PPID=0)
├── Process1 (PID=101, PPID=1)
│   └── Process2 (PID=3240, PPID=101)
└── Process3 (PID=1034, PPID=1)
    ├── Process4 (PID=1888, PPID=1034)
    │   ├── Process6 (PID=1289, PPID=1888)
    │   └── Process7 (PID=1844, PPID=1888)
    └── Process5 (PID=2056, PPID=1034)
```

**Key Points:**
- Each PID is unique
- Duplicate PPIDs are allowed (siblings share same parent)
- Terminating a parent process kills all its children

### Types of Processes

**Daemon Process**
- Background service that starts at boot time
- Provides specific system or network functionality
- Examples: `httpd`, `sshd`, `bluetoothd`, `network-manager`
- Most (not all) daemon names end with "d"

**Zombie Process**
- Process whose execution has completed
- Still appears in process list
- Occurs when parent hasn't read child's exit status
- Takes up a process table entry but minimal resources

### Viewing Processes

**ps Command** - Process Status

**Basic syntax:**
```bash
ps [options]
```

**Common ps Commands:**

```bash
# Show ALL processes with full details
ps -eaf
# -e : all processes
# -a : all processes except session leaders
# -f : full format listing

# Page through process list
ps -eaf | more
ps -eaf | less

# Count number of running processes
ps -eaf | wc -l

# Search for specific process (case-insensitive)
ps -eaf | grep -i firefox

# Show specific columns with custom formatting
ps -eo pid,ppid,%mem,%cpu,cmd --sort=-%mem | head

# BSD-style format showing memory and CPU usage
ps aux --sort -rss | head
```

**ps -eaf Output Columns:**
- **UID**: User ID who started the process
- **PID**: Process ID (unique identifier)
- **PPID**: Parent Process ID
- **C**: CPU utilization percentage
- **STIME**: Start time of the process
- **TTY**: Terminal associated with the process
- **TIME**: Cumulative CPU time
- **CMD**: Command that started the process

**Finding Firefox Processes:**
```bash
ps -eaf | grep firefox

# Note: Firefox spawns multiple processes
# First process is the main process (parent)
# Other processes are children (note PPID matches parent PID)
```

### top and htop Commands

**top** - Real-time process monitoring
```bash
top
# Shows dynamic, real-time view of running processes
# Default sort: CPU usage
# Press 'q' to quit
# Press 'M' to sort by memory
# Press 'P' to sort by CPU
# Press 'k' to kill a process (enter PID)
```

**htop** - Enhanced interactive process viewer
```bash
# Install htop
sudo apt update
sudo apt install htop

# Run htop
htop

# Interactive features:
# F6: Sort by different columns (PERCENT_CPU, PERCENT_MEM, etc.)
# F9: Kill process
# F10 or 'q': Quit
# Arrow keys: Navigate
```

**Sorting in htop:**
1. Press `F6`
2. Use arrow keys to highlight sort column (e.g., PERCENT_CPU)
3. Press `Enter`

### Finding Memory-Intensive Processes

**Top 10 memory consumers (simple):**
```bash
ps aux --sort -rss | head
# -rss : resident set size (physical memory usage)
```

**Top 10 memory consumers (custom fields):**
```bash
ps -eo pid,ppid,%mem,%cpu,cmd --sort=-%mem | head
```

**Using top in batch mode:**
```bash
top -c -b -o +%MEM | head -n 20 | tail -15
# -c : show full command line
# -b : batch mode (non-interactive)
# -o +%MEM : sort by memory
# head -n 20 : first 20 lines
# tail -15 : last 15 of those (skips header lines)
```

**Important Note: RSS Column**
- RSS = Resident Set Size
- Shows actual physical RAM usage at time of command
- This is "real memory usage" not virtual memory

---

## Background and Foreground Processes

### Foreground vs Background

**Foreground Process**
- Runs in the terminal and blocks the prompt
- User must wait for process to complete
- Cannot execute other commands in same terminal
- Receives keyboard input
- Displays output directly to terminal

**Background Process**
- Runs without blocking the terminal prompt
- User can continue using terminal
- Does NOT receive keyboard input from terminal
- May display output to terminal (can be distracting)

### Running Processes in Background

**Method 1: Start directly in background**
```bash
# Append '&' to command
firefox &

# Terminal prompt immediately available
# Firefox runs in background
```

**Method 2: Move running process to background**
```bash
# Start process in foreground
firefox

# Press Ctrl+Z to suspend process
# Prompt returns, but Firefox is FROZEN

# Resume in background
bg

# Firefox now runs normally in background
```

**CRITICAL: The bg command is essential!**
- `Ctrl+Z` only suspends (freezes) the process
- Process remains frozen until `bg` or `fg` is executed
- Without `bg`, the application window will be unresponsive

### Keyboard Shortcuts

**Ctrl+C**
- Terminate the foreground process
- Sends SIGINT (interrupt signal)
- May cause errors if process is abruptly terminated

**Ctrl+Z**
- Suspend (pause) the foreground process
- Brings back the terminal prompt
- Process is frozen until resumed

### Managing Background Jobs

**jobs Command** - List background jobs
```bash
jobs

# Output shows:
# [1]+ Running    firefox &
# [2]- Stopped    gedit

# [1], [2] = job numbers
# + = current job
# - = previous job
```

**fg Command** - Bring job to foreground
```bash
# Bring current job (marked with +) to foreground
fg

# Bring specific job to foreground
fg %1    # Job number 1
fg %2    # Job number 2
```

**Job Management Example:**
```bash
# Close all Firefox and terminal windows, start fresh terminal

# 1. Start Firefox in foreground
firefox
# Terminal blocked, cannot type commands

# 2. Terminate Firefox
# Press Ctrl+C
# Terminal available again

# 3. Start Firefox again
firefox

# 4. Suspend Firefox
# Press Ctrl+Z
# Terminal available but Firefox frozen

# 5. Resume Firefox in background
bg
# Firefox works normally, terminal available

# 6. List background jobs
jobs
# Shows: [1]+ Running    firefox &

# 7. Bring Firefox to foreground
fg %1
# Or just: fg
```

---

## Process Priorities

### Understanding Process Priority

**The Problem:**
- Processes consume system resources (CPU, memory)
- Resource-hungry processes can starve other processes
- System becomes slow or unresponsive
- Sometimes you can't terminate the problematic process

**The Solution: Nice Values**
- Assign priority to processes for resource allocation
- Controls CPU time allocation
- Does NOT directly control memory usage

### Nice Value System

**Range: -20 to +19**
- **Default**: 0
- **Lower number** = Higher priority = More CPU time
- **Higher number** = Lower priority = Less CPU time

**Priority Scale:**
```
-20  ← Highest priority (most CPU time)
-19
...
 -1
  0  ← Default priority
  1
...
 18
 19  ← Lowest priority (least CPU time)
```

**Important Note:**
- Nice values affect CPU scheduling only
- Do NOT directly control memory allocation
- Extremely low nice values can starve other processes

### Viewing Nice Values

**With ps command:**
```bash
# Show nice values (NI column)
ps -l

# Full format with nice values
ps -leaf | grep process_name

# Custom format showing nice value
ps -eo pid,ni,cmd
```

**With htop:**
```bash
htop
# NI column shows nice value for each process
# Default: 0
```

### Changing Process Priority

**renice Command** - Change nice value of running process

**Syntax:**
```bash
sudo renice -n <nice_value> -p <PID>
```

**Example: Reducing Firefox Priority**

```bash
# 1. Find Firefox PID
ps -eaf | grep firefox
# Or use htop and note PID

# 2. Reduce priority (increase nice value)
sudo renice -n 5 -p 12345
# Replace 12345 with actual Firefox PID

# 3. Verify change
htop
# Check NI column for Firefox process

# Or use ps
ps -leaf | grep firefox
# NI column shows new value
```

**Starting Process with Specific Priority:**
```bash
# Use nice command to start with priority
nice -n 10 firefox
# Starts Firefox with nice value of 10 (lower priority)
```

**Permission Requirements:**
- Increasing nice value (lowering priority): Any user
- Decreasing nice value (raising priority): Requires root/sudo
- Setting negative nice values: Requires root/sudo

---

## Troubleshooting Processes

### Killing Processes

**When to Kill Processes:**
- Process is unresponsive (hung)
- Process consuming too many resources
- Process causing system issues
- Need to restart a service

### kill Command

**Syntax:**
```bash
kill [signal] <PID>
```

**Common Signals:**
- **SIGTERM (15)**: Graceful termination (default)
  - Allows process to clean up
  - Can be ignored by process
  - Syntax: `kill <PID>` or `kill -15 <PID>`

- **SIGKILL (9)**: Forceful termination
  - Cannot be ignored
  - Immediate termination
  - No cleanup
  - Syntax: `kill -9 <PID>` or `kill -s SIGKILL <PID>`

**Examples:**
```bash
# Graceful termination (allows cleanup)
kill 1515

# Forceful termination
kill -9 1515

# Alternative syntax for SIGKILL
kill -s SIGKILL 1515
```

**Killing Firefox Example:**
```bash
# 1. Start Firefox
firefox &

# 2. Find Firefox PID
ps -eaf | grep firefox
# Note: Multiple processes may be shown
# First entry is usually the main (parent) process

# 3. Kill main Firefox process
kill -9 12345  # Replace with actual PID

# Result: Firefox window closes immediately
# All child processes also terminated
```

### killall Command

**Purpose:** Kill all processes by name
- Convenient when multiple instances exist
- No need to find individual PIDs
- Kills ALL processes matching the name

**Syntax:**
```bash
killall [options] process_name
```

**Examples:**
```bash
# Kill all Firefox processes
killall firefox

# Graceful termination
killall firefox

# Forceful termination
killall -9 firefox

# Kill multiple process types
killall firefox chrome
```

### Process Troubleshooting Workflow

**1. Identify the problem process**
```bash
# Check CPU usage
top
# Press 'P' to sort by CPU
# Or
htop
# Press F6, select PERCENT_CPU

# Check memory usage
ps aux --sort -rss | head
# Or in htop, press F6, select PERCENT_MEM
```

**2. Determine if you can terminate it**
- Is it a system-critical process? (Be careful!)
- Is it your own process or another user's?
- Do you have permission to kill it?

**3. Try graceful termination first**
```bash
kill <PID>
# Wait a few seconds
systemctl status service_name  # For services
ps -p <PID>                    # Check if still running
```

**4. Use forceful termination if needed**
```bash
kill -9 <PID>
# Or for multiple instances
killall -9 process_name
```

**5. Verify termination**
```bash
ps -eaf | grep process_name
# Should show no results

# Or for services
systemctl status service_name
# Should show "inactive (dead)"
```

### Service-Specific Troubleshooting

**For services managed by systemd:**
```bash
# Check status
systemctl status service_name

# View logs
journalctl -u service_name
# -f flag for real-time following
journalctl -f -u service_name

# Restart instead of kill
sudo systemctl restart service_name

# If restart fails, stop then start
sudo systemctl stop service_name
sudo systemctl start service_name
```

---

## Important Reminders and Best Practices

### Package Management
1. Always run `sudo apt update` before installing packages
2. Use `apt` for dependency management, not `dpkg` alone
3. Verify repository authenticity before adding third-party repos
4. Use `apt list -a package_name` to verify available versions

### Service Management
5. Remember: start/stop = immediate, enable/disable = boot behavior
6. Always check status after starting/stopping services
7. Test services locally with 127.0.0.1 before exposing to network
8. Both start AND enable services that should survive reboots

### Process Management
9. Parent process death kills all children
10. Nice values affect CPU, not memory allocation
11. Lower nice value = higher priority (counterintuitive!)
12. Try graceful termination (kill) before forceful (kill -9)

### Background Processes
13. Use `bg` after Ctrl+Z or process remains frozen
14. Use `&` when starting to run directly in background
15. Use `jobs` to track background processes in current session
16. Use `fg` to bring processes back to foreground when needed

### General
17. Daemon names usually (not always) end with "d"
18. init process is PID 1, PPID 0
19. Use `ps -eaf` for detailed process information
20. Use `htop` for interactive, visual process management
21. sudo password in lab environment: P@ssw0rd

### Common Mistakes to Avoid
- Forgetting to enable services (they won't survive reboot)
- Using kill -9 as first resort (try kill first)
- Confusing PID with PPID
- Thinking higher nice value = higher priority (it's opposite!)
- Not running `apt update` before installing packages
- Suspending with Ctrl+Z but forgetting to run `bg`

---

## Quick Reference Commands

### Package Management
```bash
apt search package_name
sudo apt update
sudo apt install package_name
sudo apt remove package_name
sudo apt upgrade
dpkg --list
apt list -a package_name
```

### Service Management
```bash
systemctl status service_name
sudo systemctl start service_name
sudo systemctl stop service_name
sudo systemctl restart service_name
sudo systemctl enable service_name
sudo systemctl disable service_name
systemctl list-unit-files --type service
```

### Process Viewing
```bash
ps -eaf                              # All processes
ps -eaf | grep process_name          # Search processes
ps aux --sort -rss | head            # Top memory users
ps -eo pid,ppid,%mem,%cpu,cmd        # Custom format
top                                  # Real-time monitoring
htop                                 # Interactive monitoring
```

### Process Control
```bash
kill <PID>                          # Graceful termination
kill -9 <PID>                       # Forceful termination
killall process_name                # Kill all by name
sudo renice -n <value> -p <PID>    # Change priority
```

### Background/Foreground
```bash
command &                           # Run in background
Ctrl+Z                             # Suspend foreground process
bg                                 # Resume in background
fg                                 # Bring to foreground
jobs                               # List background jobs
```

---

## Lab Exercise Summary

Today's exercises covered:
1. ✓ Searching and installing Firefox using apt
2. ✓ Managing Apache2 web server service
3. ✓ Viewing processes with ps -eaf
4. ✓ Identifying Firefox parent and child processes
5. ✓ Killing processes with kill -9
6. ✓ Running Firefox in foreground/background
7. ✓ Using Ctrl+C and Ctrl+Z for process control
8. ✓ Managing background jobs with bg, fg, jobs
9. ✓ Installing and using htop
10. ✓ Sorting processes by CPU and memory usage
11. ✓ Changing process priority with renice

---

*These notes cover comprehensive Linux service and process management concepts learned on Day 4.*
*All technical details have been verified for accuracy.*