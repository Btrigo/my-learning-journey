# Windows Cheat Sheet

Fast reference for commands, tools, shortcuts & troubleshooting.

---

## 1. Navigation & System Information

* `systeminfo` — Full system overview (OS, RAM, hotfixes, IP info)
* `winver` — Windows version & build
* `hostname` — Computer name (faster than going to Settings)
* `whoami` — Current logged-in user
* `wmic computersystem get model,name,manufacturer` — Hardware info
* `msinfo32` — System Information GUI
* `dxdiag` — DirectX diagnostic (GPU/driver information)

---

## 2. Networking Commands

### Basic Network Info

```
ipconfig /all          — Full adapter info: IP, subnet, gateway, DNS, MAC, DHCP server
ipconfig /flushdns     — Flush local DNS cache (fix stale name resolution)
ipconfig /release      — Drop the current IP address
ipconfig /renew        — Request a new IP from DHCP
ipconfig /displaydns   — Show cached DNS entries
getmac                 — MAC addresses only
arp -a                 — ARP table (IP-to-MAC mappings on local network)
```

> **169.254.x.x** = APIPA address — DHCP is not responding. Start troubleshooting there.

### Connectivity Tests

```
ping 127.0.0.1         — Test local loopback (is TCP/IP stack working?)
ping <gateway>         — Can you reach your default gateway?
ping 8.8.8.8           — Can you reach the internet by IP?
ping google.com        — Can you resolve DNS AND reach the internet?
tracert google.com     — Map each hop to a destination; find where traffic dies
pathping google.com    — Combines ping + tracert with packet loss per hop
```

> **Troubleshooting path:** loopback → gateway → 8.8.8.8 → google.com. Work up the chain.

### Port & Connection Analysis

```
netstat -ano           — All active connections with PID (find what process owns a port)
netsh interface show interface
netsh int ip reset     — Reset TCP/IP stack (nuclear option for persistent issues)
```

### Network Shares & Mapped Drives

```
net use                          — List all mapped drives and network connections
net use Z: \\server\share        — Map a drive
net use Z: /delete               — Remove a specific mapped drive
net use * /delete                — Remove ALL mapped drives
```

> **When to use:** User says "my drive is missing" or "I can't find the file share." This is your first command.

### Route Management

```
route print                      — View routing table
route add <network> mask <mask> <gateway>   — Add a static route
route delete <network>           — Remove a static route
```

### PowerShell Networking

```powershell
Get-NetAdapter                                          — List all network adapters
Get-NetIPAddress                                        — IP addresses on all adapters
Test-NetConnection -ComputerName google.com -Port 443  — Test TCP connectivity on a specific port
Resolve-DnsName domain.com                             — DNS resolution (like nslookup)
Get-NetTCPConnection                                   — Active TCP connections
Get-DnsClient                                          — DNS client settings
Get-NetFirewallRule                                    — List firewall rules
```

> **Test-NetConnection is your Linux nc equivalent.** Know your ports: 443 (HTTPS), 80 (HTTP), 3389 (RDP), 22 (SSH), 445 (SMB), 53 (DNS).

---

## 3. DNS Tools

```
nslookup domain.com              — Query DNS for a domain
nslookup domain.com 8.8.8.8     — Query a specific DNS server
ipconfig /flushdns               — Clear local DNS cache
ipconfig /displaydns             — View cached DNS entries
Resolve-DnsName domain.com       — PowerShell DNS lookup
Get-DnsClientServerAddress       — See which DNS servers are configured
```

> **It's always DNS.** When an internal app or website stops resolving correctly, flush DNS first, then use nslookup to verify what's actually being returned.

---

## 4. File System & Permissions

### File/Folder Permissions

```
icacls <file or folder>          — View permissions
icacls <path> /grant user:F      — Grant full control to a user
takeown /f <path> /r /d y        — Take ownership of a file or folder
attrib -h -s <filename>          — Remove hidden/system attributes
```

### Copying & Mirroring

```
robocopy <src> <dest> /MIR       — Mirror source to dest (deletes files not in source)
robocopy <src> <dest> /E /Z /R:2 /W:2  — Copy with subdirs, restartable, 2 retries
scp user@host:/path /local       — Secure copy over SSH
```

### Useful Paths & Shortcuts

```
%appdata%              — C:\Users\<name>\AppData\Roaming
%localappdata%         — C:\Users\<name>\AppData\Local
%temp%                 — Temp files (safe to clear)
shell:startup          — Startup folder for current user
C:\Windows\System32    — Core Windows binaries
C:\ProgramData         — System-wide app data (hidden by default)
C:\Windows\Logs        — Windows log files
C:\Users\<name>\AppData\Local   — Per-user app data/logs
```

---

## 5. User & Account Management

### Local Users

```
net user                         — List all local user accounts
net user <username>              — Details on a specific user
net user <username> <password> /add   — Create a local user
net user <username> /delete      — Delete a local user
```

### Local Groups

```
net localgroup                              — List all local groups
net localgroup administrators               — List members of local Administrators
net localgroup administrators <username> /add     — Add user to local Admins
net localgroup administrators <username> /delete  — Remove user from local Admins
```

> **When to use:** VPN troubleshooting, RMM access, remote support where domain isn't reachable. Don't leave temp admin accounts sitting around — clean them up.

### PowerShell User Commands

```powershell
Get-LocalUser                    — List local users
Get-LocalGroup                   — List local groups
whoami /groups                   — See all groups the current user belongs to
```

> **whoami /groups is how you verify access.** When a user says "I should have access to X," check if they're in the right group here first.

---

## 6. Services & Processes

### Service Management

```
services.msc                     — GUI service manager
net stop <service>               — Stop a service
net start <service>              — Start a service
Restart-Service <service>        — PowerShell restart
sc query <service>               — Check service status from CMD
```

### Common Services Worth Knowing

| Service Name | What It Does |
|---|---|
| `spooler` | Print spooler — restart this when printing breaks |
| `wuauserv` | Windows Update |
| `LanmanWorkstation` | SMB client — mapped drives depend on this |
| `Dnscache` | DNS client cache |
| `W32Time` | Windows Time service — affects Kerberos auth on domain |

### Process Tools

```
taskmgr                          — Task Manager GUI
tasklist                         — List all running processes (CMD)
tasklist /svc                    — Show services tied to each process
taskkill /PID <pid> /F           — Force kill a process by PID
Get-Process                      — PowerShell process list
Stop-Process -Name <name>        — PowerShell kill by name
```

> **Pair netstat -ano with tasklist /svc:** netstat gives you the PID using a port, tasklist tells you what that PID actually is.

---

## 7. Group Policy (Domain Environments)

```
gpupdate /force                  — Force immediate Group Policy refresh from DC
gpresult /r                      — Show applied GPOs (summary)
gpresult /h report.html          — Full HTML GP report (open in browser, Ctrl+F to search)
whoami /groups                   — Verify group membership (GP applies based on group)
```

> **gpresult /h report.html is your best friend** when debugging why a policy isn't applying. Open the file in a browser and Ctrl+F for the policy name.

---

## 8. Windows Update & Repair Tools

### System Repairs

```
sfc /scannow                                     — Scan and repair protected system files
DISM /Online /Cleanup-Image /RestoreHealth       — Repair Windows image from Windows Update
```

> Run SFC first. If it fails or finds unfixable errors, run DISM, then SFC again. DISM stands for **Deployment Image Servicing and Management** — it is NOT Dell-specific, it works on all hardware.

### Update Commands

```
wuauclt /detectnow               — Trigger update detection
wuauclt /reportnow               — Force reporting to WSUS
```

---

## 9. Active Directory Tools (Domain Environments)

```
gpresult /r                      — Applied GPOs for current user/computer
gpupdate /force                  — Refresh GP from domain controller
whoami /groups                   — Current user's group memberships
net user <username> /domain      — User account info from AD
net group /domain                — List domain groups
```

### AD MMC Snap-ins

```
dsa.msc    — Active Directory Users and Computers
dssite.msc — AD Sites and Services
```

---

## 10. MMC Snap-ins (Must-Know)

```
eventvwr.msc     — Event Viewer (Security, System, Application logs)
diskmgmt.msc     — Disk Management
devmgmt.msc      — Device Manager
gpedit.msc       — Local Group Policy Editor
secpol.msc       — Local Security Policy
taskschd.msc     — Task Scheduler
compmgmt.msc     — Computer Management (hub for many tools)
lusrmgr.msc      — Local Users and Groups GUI
wf.msc           — Windows Firewall with Advanced Security
```

---

## 11. Firewall & Security Tools

```
wf.msc                           — Firewall GUI
Get-NetFirewallProfile           — PowerShell: view firewall profile status
Set-NetFirewallRule              — PowerShell: modify firewall rules
```

### Common Security Event Logs (in eventvwr.msc)

| Log | What to Look For |
|---|---|
| **Security** | Login attempts, privilege use, account changes (Event IDs 4624, 4625, 4648) |
| **System** | Boot events, hardware errors, service failures |
| **Application** | App crashes and failures |

```powershell
Get-EventLog -LogName System -Newest 50
powershell -Command "Get-WinEvent -LogName Security -MaxEvents 20"
```

---

## 12. Quick GUI Tools

```
msconfig    — Startup & boot configuration
perfmon     — Performance monitor
resmon      — Resource monitor (CPU, disk, network per process)
cleanmgr    — Disk cleanup
mrt         — Windows Malicious Software Removal Tool
ncpa.cpl    — Network adapter settings (fastest way to get to adapter properties)
```

> **ncpa.cpl** beats navigating through Settings every time. Run it from Win+R.

---

## 13. Network Reset (Last Resort)

**Network Reset** resets ALL network adapter settings — removes Wi-Fi profiles, reinstalls NIC drivers, sets everything back to DHCP. Requires a reboot.

Use when: DNS is broken client-side, adapters are in a bad state, ipconfig /release and /renew aren't fixing it, and flushdns didn't help.

Run from: Settings → Network & Internet → Advanced Network Settings → Network Reset
Or: `netsh int ip reset` + `netsh winsock reset` for a partial reset without full NIC reinstall.

---

## 14. Useful Troubleshooting Shortcuts

| Shortcut | Action |
|---|---|
| `Win + X` | Admin menu (quick access to PowerShell, Device Manager, etc.) |
| `Win + R` | Run dialog |
| `Ctrl + Shift + Esc` | Task Manager directly |
| `Win + L` | Lock workstation |
| `Win + S` | Windows search |

---

## 15. Troubleshooting Playbooks

### User can't get online
1. `ipconfig /all` — Do they have a real IP? Gateway? DNS? Is it 169.254.x.x?
2. `ping 127.0.0.1` — Loopback working?
3. `ping <gateway>` — Can they reach the router?
4. `ping 8.8.8.8` — Internet reachable by IP?
5. `ping google.com` — DNS working?
6. `ipconfig /flushdns` + `ipconfig /renew` if needed
7. Network Reset as last resort

### Mapped drive missing
1. `net use` — Is the drive still mapped?
2. `net use * /delete` then remap — Clear stale connections
3. `gpupdate /force` — If drives are GP-deployed, force a refresh
4. Check `LanmanWorkstation` service is running

### User doesn't have access to something
1. `whoami /groups` — Are they in the right group?
2. `icacls <path>` — What are the actual permissions on the resource?
3. `gpresult /h report.html` — Is a GPO blocking or granting access?

### Printer not working
1. Restart the `spooler` service: `net stop spooler` → `net start spooler`
2. Check `services.msc` — is spooler set to Automatic?
3. Check `devmgmt.msc` for driver issues

### Can't reach a specific port/service
1. `Test-NetConnection -ComputerName <host> -Port <port>` — Is the port open?
2. `netstat -ano` — Is anything listening on that port locally?
3. `wf.msc` — Is the Windows firewall blocking it?

---

## 16. Personal Notes

- VLANs and switches — understand Layer 2 segmentation and how inter-VLAN routing works
- Layer 3 switches are often the default gateway for end devices (they do the routing, not a router)
- DHCP relay agents forward DHCP broadcasts across VLANs to a central DHCP server
- Firewall rules and ACLs control traffic at the perimeter and between network segments
- CCNA concepts (subnetting, routing, switching) make all of the above click faster
- `route print` is useful when a machine has multiple NICs or VPN and you need to see which path traffic takes

---

**This cheat sheet will grow as you master Windows administration and help desk workflows.**