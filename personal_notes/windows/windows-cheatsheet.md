# Windows Cheat Sheet

Fast reference for commands, tools, shortcuts & troubleshooting.

---

## 1. Navigation & System Information

* `systeminfo` — Full system overview
* `winver` — Windows version & build
* `hostname` — Computer name
* `wmic computersystem get model,name,manufacturer` — Hardware info
* `msinfo32` — System Information GUI
* `dxdiag` — DirectX diagnostic (GPU/driver information)

---

## 2. Networking Commands

### Basic Network Info

```

ipconfig /all
ipconfig /flushdns
ipconfig /release
ipconfig /renew
getmac 
arp
```

### Connectivity Tests

```
ping google.com
tracert google.com
pathping google.com
```

### Port & Connection Analysis

```
netstat -ano
netsh interface show interface
netsh int ip reset
```

### PowerShell Networking

```
Get-NetAdapter
Get-NetIPAddress
Test-NetConnection -Port 443 -ComputerName google.com
Resolve-DnsName domain.com
```

---

## 3. DNS Tools

```

Network reset — Resets all network adapters, removes Wi-Fi profiles, reinstalls NIC drivers (Last-resort fix)
nslookup domain.com
Resolve-DnsName domain.com
Get-DnsClientServerAddress
ipconfig /displaydns
```

Useful when troubleshooting:

* DNS outages
* Slow name resolution
* Incorrect DNS server settings

---

## 4. File System & Permissions

### File/Folder Permissions

```
icacls <file or folder>
takeown /f <path> /r /d y
attrib -h -s <filename>
```

### Copying & Mirroring

```
scp - secure copy 
robocopy <src> <dest> /MIR
robocopy <src> <dest> /E /Z /R:2 /W:2
```

### Useful Paths

```
%appdata%
%localappdata%
%temp%
shell:startup
C:\Windows\System32
C:\ProgramData
```

---

## 5. Services & Processes

### Service Management

```
services.msc
net stop <service>
net start <service>
Restart-Service <service>
```

### Process Tools

```
taskmgr
Get-Process
Stop-Process -Name <name>
```

### Common Services

* **spooler** (printing)
* **wuauserv** (Windows updates)
* **LanmanWorkstation** (SMB access)
* **Dnscache** (DNS client)

---

## 6. Windows Update & Repair Tools

### Commands

```
wuauclt /detectnow
wuauclt /reportnow
```

### System Repairs

```
sfc /scannow
DISM /Online /Cleanup-Image /RestoreHealth
```

Use when dealing with:

* Corrupt Windows updates
* Broken system files
* Boot issues

---

## 7. MMC Snap-ins (Must-Know)

```
eventvwr.msc
diskmgmt.msc
devmgmt.msc
gpedit.msc
secpol.msc
taskschd.msc
compmgmt.msc
lusrmgr.msc
```

---

## 8. Active Directory Tools (When on Domain)

```
gpresult /r
gpupdate /force
whoami /groups
net user /domain
net group /domain
```

### MMC Snap-ins for AD

```
dsa.msc   — Active Directory Users and Computers
dssite.msc — Sites and Services
```

---

## 9. PowerShell Essentials

### System Commands

```
Get-LocalUser
Get-LocalGroup
Get-Service
Restart-Service spooler
Get-EventLog -LogName System -Newest 50
```

### Network Commands

```
route print
arp -a
ncpa.cpl
Get-NetTCPConnection
Get-DnsClient
Get-NetFirewallRule
```

---

## 10. Firewall & Security Tools

```
wf.msc
Get-NetFirewallProfile
Set-NetFirewallRule
```

### Common Security Logs

* **Security** log (authentication)
* **System** log (boot, hardware errors)
* **Application** log (app failures)

---

## 11. Useful Troubleshooting Shortcuts

* `Win + X` — Admin menu
* `Win + R` — Run dialog
* `Ctrl + Shift + Esc` — Task Manager
* `Win + L` — Lock workstation
* `Win + .` — Emoji/clipboard tools
* `Win + S` - Enter windows search bar

---

## 12. Quick GUI Tools

* **msconfig** — Startup & boot configuration
* **perfmon** — Performance monitor
* **resmon** — Resource monitor
* **cleanmgr** — Disk cleanup
* **mrt** — Windows malicious software removal tool

---

## 13. Common Log Locations

```
C:\Windows\Logs
C:\Windows\SoftwareDistribution
C:\ProgramData\Microsoft\Windows\Start Menu
C:\Users\<name>\AppData\Local
```

---

## 14. Commands Worth Memorizing

```
powershell -Command "Get-WinEvent -LogName Security -MaxEvents 20"
Get-WindowsCapability -Online
shutdown /r /t 0
```

---

## 15. Notes Section (My Personal Additions)

Add your own commands, tools, fixes, or scripts here.

- ccna can be important for network understanding 
- vlans and switches - learn dis 
- understanding layer three switches are often set as the default gateway for a device. (dhcp relay)
- firewall rules and/or ACLs 

route print
route add <network> mask <mask> <gateway> 
route delete <network>
network reset
ncpa.cpl


---

**This cheat sheet will grow as you master Windows administration and help desk workflows.**
