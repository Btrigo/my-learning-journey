# Network Fundamentals - Comprehensive Study Notes
**Date:** December 20, 2024  
**Platform:** TryHackMe  
**Rooms Completed:** What is Networking, Intro to LAN, OSI Model  
**Focus:** Building foundational networking knowledge for NOC career path

---

## Table of Contents
1. [What is Networking?](#what-is-networking)
2. [Network Identification & Addressing](#network-identification--addressing)
3. [Network Protocols](#network-protocols)
4. [Network Topologies](#network-topologies)
5. [Network Devices](#network-devices)
6. [Subnetting Deep Dive](#subnetting-deep-dive)
7. [OSI Model](#osi-model)
8. [NOC Applications & Troubleshooting](#noc-applications--troubleshooting)

---

## What is Networking?

### Core Concept
**Networks** are simply interconnected entities that share information or resources. In computing, networks consist of devices (computers, servers, printers, IoT devices, etc.) connected to communicate and share data.

### Network Scale
- **Minimum:** 2 devices
- **Maximum:** Billions of devices (the Internet)
- **Real-world examples:** Home WiFi (5-10 devices), corporate networks (hundreds to thousands), data centers (tens of thousands), the Internet (billions)

### Historical Context
**ARPANET (Late 1960s)**
- First documented network in action
- Funded by U.S. Department of Defense
- Initially connected four universities
- Foundation for modern Internet architecture

**World Wide Web (1989)**
- Invented by Tim Berners-Lee at CERN
- Transformed Internet from data exchange network to information repository
- Introduced HTTP, HTML, and URL concepts
- Changed Internet from academic/military tool to public resource

### Private vs. Public Networks

**Private Networks:**
- Internal networks within organizations (home, business, school)
- Use private IP address ranges (RFC 1918):
  - 10.0.0.0 to 10.255.255.255 (Class A)
  - 172.16.0.0 to 172.31.255.255 (Class B)
  - 192.168.0.0 to 192.168.255.255 (Class C)
- Not directly routable on the Internet
- Require NAT (Network Address Translation) for Internet access

**Public Networks:**
- The Internet - connects private networks globally
- Uses public IP addresses (routable)
- Managed by ISPs (Internet Service Providers)

**Key Principle:** Multiple devices on the same private network can share a single public IP address through NAT.

---

## Network Identification & Addressing

Devices require two forms of identification to communicate on networks:

### 1. IP Addresses (Logical Addressing - Layer 3)

#### IPv4 Addressing

**Structure:**
```
192.168.1.10
 │   │   │  │
 └───┴───┴──┴─── Four octets (8 bits each = 32 bits total)
Each octet: 0-255 (2^8 = 256 possible values)
```

**Key Characteristics:**
- **Temporary/Dynamic:** Can change when device reconnects or lease expires
- **Logical:** Assigned by network configuration, not hardware
- **Hierarchical:** Contains network and host portions
- **Cannot be duplicated** within the same network (causes IP conflict)

**IPv4 Address Space:**
- Total addresses: 2^32 = 4,294,967,296 (~4.29 billion)
- **Problem:** With 50+ billion connected devices (Cisco 2021 estimate), we've exhausted available addresses
- **Solution:** IPv6 and NAT technologies

#### IPv6 Addressing

**Structure:**
```
2a00:22c4:a531:c500:425f:cce6:c36b:f64d
 │    │    │    │    │    │    │    │
 └────┴────┴────┴────┴────┴────┴────┴─── Eight groups (16 bits each = 128 bits total)
Hexadecimal notation (0-9, a-f)
```

**Key Improvements:**
- **Address space:** 2^128 = 340 undecillion addresses (340 trillion trillion trillion)
- **No NAT required:** Every device can have unique public address
- **Simplified header:** More efficient routing
- **Built-in security:** IPSec mandatory
- **Autoconfiguration:** SLAAC (Stateless Address Autoconfiguration)
- **No broadcasts:** Uses multicast instead (more efficient)

**Adoption Status (2024):**
- ~40% of global Internet traffic uses IPv6
- Major services (Google, Facebook, Netflix) fully support IPv6
- Dual-stack (IPv4 + IPv6) is current standard during transition

#### Public vs. Private IP Addresses

**Example from TryHackMe:**
```
Device Name      Private IP      Public IP       Use Case
DESKTOP-KJE57FD  192.168.1.77   86.157.52.21    Internal communication / Internet access
CMNatic-PC       192.168.1.74   86.157.52.21    Internal communication / Internet access
```

**Key Points:**
- Both devices communicate internally using private IPs (192.168.1.x)
- Both share the same public IP (86.157.52.21) when accessing Internet
- ISP assigns public IP (usually dynamically, sometimes static for fee)
- Router performs NAT to map private IPs to public IP

**NOC Relevance:** When troubleshooting connectivity:
1. Verify device has valid private IP: `ipconfig` / `ip addr show`
2. Verify gateway is reachable: `ping [gateway_IP]`
3. Verify NAT is working: `curl ifconfig.me` (shows public IP)
4. Check if public IP matches ISP assignment

---

### 2. MAC Addresses (Physical Addressing - Layer 2)

#### Structure and Format

**MAC Address Anatomy:**
```
a4:c3:f0:85:ac:2d
│      │      │
└──────┘      └─────── Device-specific (24 bits) - Unique identifier
   │
   └───────────────── OUI (24 bits) - Manufacturer identifier

Full format: 48 bits = 6 bytes = 12 hexadecimal characters
```

**OUI (Organizationally Unique Identifier) Examples:**
- `00:50:56:xx:xx:xx` = VMware
- `00:1A:2B:xx:xx:xx` = Cisco
- `08:00:27:xx:xx:xx` = VirtualBox
- `EC:5C:68:xx:xx:xx` = Intel
- `DC:A6:32:xx:xx:xx` = Raspberry Pi

**Alternative Notations:**
- Colon-separated: `AA:BB:CC:DD:EE:FF` (Linux/Unix standard)
- Hyphen-separated: `AA-BB-CC-DD-EE-FF` (Windows)
- Cisco format: `aabb.ccdd.eeff`
- No separators: `AABBCCDDEEFF`

#### Key Characteristics

**Physical/Hardware Address:**
- Burned into NIC (Network Interface Card) during manufacturing
- Also called: Hardware address, Physical address, BIA (Burned-In Address)
- Stored in NIC's ROM or EEPROM

**Permanence:**
- Tied to physical hardware
- Removing NIC = removing that MAC address
- Installing NIC in different computer = MAC moves with it
- **Exception:** Can be spoofed at software level (more on this below)

**Uniqueness:**
- Globally unique (in theory - manufacturers should never duplicate)
- Each physical network interface has its own MAC
  - Laptop with Ethernet + WiFi = 2 MAC addresses
  - Desktop with dual NICs = 2 MAC addresses
  - Virtual machines = Virtual MAC addresses (assigned by hypervisor)

#### Layer 2 Operation

**How Switches Use MAC Addresses:**

Switches maintain a **MAC Address Table** (CAM table - Content Addressable Memory):

```
Port     MAC Address         VLAN    Age
------   -----------------   ----    ---
Gi0/1    AA:BB:CC:DD:EE:FF   10      5 min
Gi0/2    11:22:33:44:55:66   10      2 min
Gi0/3    77:88:99:AA:BB:CC   20      10 min
```

**Learning Process:**
1. Frame arrives on Port 1 with Source MAC = AA:BB:CC:DD:EE:FF
2. Switch learns: "AA:BB:CC:DD:EE:FF is connected to Port 1"
3. Switch checks Destination MAC in frame
4. If destination MAC is in table → forward to that specific port only
5. If destination MAC is unknown → flood to all ports except source (until it learns)

**Cisco Commands:**
```
# View entire MAC address table
show mac address-table

# View MACs on specific interface
show mac address-table interface gi0/1

# View specific MAC address
show mac address-table address aaaa.bbbb.cccc

# View MACs in specific VLAN
show mac address-table vlan 10

# Clear MAC address table (force re-learning)
clear mac address-table dynamic
```

#### MAC Address Types

**1. Unicast MAC (Specific Device):**
- Format: Any address where first byte is even
- Example: `AA:BB:CC:DD:EE:FF`
- Destination: Single specific device
- Usage: Normal frame forwarding

**2. Broadcast MAC (All Devices):**
- Format: `FF:FF:FF:FF:FF:FF` (all 1s in binary)
- Destination: Every device on local network segment
- Usage: ARP requests, DHCP discovery, network announcements
- **Important:** Broadcasts do NOT cross router boundaries (Layer 3 boundary)

**3. Multicast MAC (Group of Devices):**
- Format: First byte is odd (least significant bit = 1)
- IPv4 multicast range: `01:00:5E:xx:xx:xx`
- IPv6 multicast range: `33:33:xx:xx:xx:xx`
- Usage: Routing protocols (OSPF, EIGRP), streaming, group communications

#### MAC Spoofing

**What is MAC Spoofing?**
- Changing MAC address at software/OS level
- Hardware MAC remains unchanged, but OS presents different MAC to network
- Original MAC still in NIC, but OS overrides it

**How to Spoof (Linux):**
```bash
# View current MAC
ip link show eth0

# Bring interface down
sudo ip link set eth0 down

# Change MAC address
sudo ip link set eth0 address AA:BB:CC:DD:EE:FF

# Bring interface up
sudo ip link set eth0 up

# Verify change
ip link show eth0
```

**How to Spoof (Windows):**
```powershell
# View current MAC
Get-NetAdapter | Select-Object Name, MacAddress

# Change via Device Manager → Network Adapter → Advanced → Network Address
# Or via Registry:
# HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\[adapter_number]
# Add "NetworkAddress" value
```

**Security Implications:**

**Attack Scenarios:**
1. **Bypassing MAC filtering:** Guest WiFi systems that allow only paid MAC addresses
2. **ARP spoofing/poisoning:** Impersonate gateway to intercept traffic
3. **Evading network access control (NAC):** Pretend to be authorized device
4. **Session hijacking:** Take over another device's session

**Defense Mechanisms:**
1. **Port Security (Cisco switches):**
   ```
   interface GigabitEthernet0/1
     switchport mode access
     switchport port-security
     switchport port-security maximum 1
     switchport port-security mac-address sticky
     switchport port-security violation shutdown
   ```
2. **802.1X authentication:** Requires credentials, not just MAC
3. **DHCP snooping:** Prevents rogue DHCP servers
4. **Dynamic ARP Inspection (DAI):** Validates ARP packets
5. **IP Source Guard:** Prevents IP spoofing

**TryHackMe Practical Example:**
- Hotel WiFi scenario: Router allows only Alice's MAC (she paid)
- Bob spoofs his MAC to match Alice's MAC
- Router now accepts Bob's traffic (thinks he's Alice)
- **Real-world impact:** Revenue loss, unauthorized access

**NOC Detection:**
- Monitor for duplicate MACs on network
- Watch for MAC flapping (same MAC appearing on multiple ports)
- Alert on MAC address changes for critical devices
- Log format: `%SW_MATM-4-MACFLAP_NOTIF: Host aaaa.bbbb.cccc in vlan 10 is flapping between port Gi0/1 and port Gi0/2`

---

## Network Protocols

### ICMP (Internet Control Message Protocol)

**Purpose:**
- Network diagnostics and error reporting
- Does NOT carry application data
- Layer 3 protocol (works with IP)

**Common ICMP Message Types:**

| Type | Name                    | Purpose                               | Code Example        |
|------|-------------------------|---------------------------------------|---------------------|
| 0    | Echo Reply              | Response to ping                      | Ping response       |
| 3    | Destination Unreachable | Cannot reach destination              | Network unreachable |
| 5    | Redirect                | Better route available                | Route optimization  |
| 8    | Echo Request            | Ping request                          | Ping initiation     |
| 11   | Time Exceeded           | TTL expired (traceroute uses this)    | Traceroute hops     |
| 30   | Traceroute              | Path discovery                        | Network mapping     |

#### Ping Command

**Basic Syntax:**
```bash
# Linux
ping [IP_address or hostname]
ping 192.168.1.1
ping google.com

# Windows (sends 4 packets by default)
ping 192.168.1.1

# Linux (continuous until Ctrl+C)
ping -c 4 192.168.1.1  # Send only 4 packets
```

**What Ping Tells You:**
```
PING 192.168.1.254 (192.168.1.254) 56(84) bytes of data.
64 bytes from 192.168.1.254: icmp_seq=1 ttl=64 time=4.16 ms
64 bytes from 192.168.1.254: icmp_seq=2 ttl=64 time=3.89 ms
64 bytes from 192.168.1.254: icmp_seq=3 ttl=64 time=4.05 ms

--- 192.168.1.254 ping statistics ---
6 packets transmitted, 6 received, 0% packet loss, time 5008ms
rtt min/avg/max/mdev = 3.89/4.16/4.52/0.23 ms
```

**Interpreting Results:**
- **Time (RTT - Round Trip Time):** How long packet took (lower = better)
  - <1 ms: Same local network
  - 1-30 ms: Excellent (same city/region)
  - 30-100 ms: Good (cross-country)
  - >100 ms: High latency (international or congested)
- **TTL (Time To Live):** Number of router hops remaining
  - 64 = likely Linux/Unix
  - 128 = likely Windows
  - 255 = likely network device (router/switch)
- **Packet loss:** Percentage of packets that didn't return
  - 0% = excellent
  - 1-5% = acceptable
  - >5% = problem (investigate)

**NOC Troubleshooting with Ping:**
```bash
# Test local connectivity
ping 127.0.0.1          # Loopback (tests TCP/IP stack)
ping [own_IP]           # Tests own NIC

# Test local network
ping [gateway_IP]       # Tests local network connectivity
ping [another_local_IP] # Tests switch/VLAN

# Test external connectivity
ping 8.8.8.8           # Google DNS (tests Internet without DNS)
ping google.com        # Tests Internet + DNS resolution

# Advanced ping options
ping -c 100 -i 0.2 192.168.1.1  # 100 packets, 0.2s interval (stress test)
ping -s 1472 192.168.1.1        # Jumbo frame test (MTU discovery)
ping -W 2 192.168.1.1           # 2 second timeout
```

**Common Ping Errors:**
- **"Destination Host Unreachable":** No route to host (routing issue)
- **"Request Timed Out":** No response (firewall, device down, or network issue)
- **"Network Unreachable":** No route configured to that network
- **"TTL Expired in Transit":** Too many hops (routing loop)

---

### ARP (Address Resolution Protocol)

**Purpose:** Maps IP addresses (Layer 3) to MAC addresses (Layer 2) on local networks.

**Why ARP is Necessary:**
- IP addresses are logical (can change)
- MAC addresses are physical (tied to hardware)
- Switches forward frames based on MAC addresses, not IP addresses
- When you know destination IP but need destination MAC → use ARP

#### ARP Process (Step-by-Step)

**Scenario:** Computer A (192.168.1.10) wants to talk to Computer B (192.168.1.20)

**Step 1: ARP Request (Broadcast)**
```
Computer A thinks: "I know the IP (192.168.1.20), but I need the MAC address."

Computer A sends ARP broadcast:
  Source MAC:  01:00:AB:78:99:33 (Computer A's MAC)
  Dest MAC:    FF:FF:FF:FF:FF:FF (Broadcast - everyone gets this)
  Message:     "Who has IP 192.168.1.20? Tell 192.168.1.10"
```

**Step 2: ARP Reply (Unicast)**
```
Computer B receives broadcast, recognizes its IP:

Computer B sends ARP reply directly to Computer A:
  Source MAC:  18:AC:33:12:88:29 (Computer B's MAC)
  Dest MAC:    01:00:AB:78:99:33 (Computer A's MAC)
  Message:     "192.168.1.20 is at MAC 18:AC:33:12:88:29"
```

**Step 3: Communication Proceeds**
```
Computer A now knows:
  192.168.1.20 = 18:AC:33:12:88:29

Computer A caches this in ARP table for future use.
Computer A can now send data directly to Computer B using its MAC.
```

#### ARP Cache/Table

**Purpose:** Store IP-to-MAC mappings to avoid repeated ARP requests.

**Viewing ARP Cache:**

**Windows:**
```cmd
C:\> arp -a

Interface: 192.168.1.10 --- 0x4
  Internet Address      Physical Address      Type
  192.168.1.1          00-50-56-c0-00-08     dynamic
  192.168.1.20         18-ac-33-12-88-29     dynamic
  192.168.1.255        ff-ff-ff-ff-ff-ff     static
```

**Linux:**
```bash
# Method 1: arp command (older)
$ arp -n
Address         HWtype  HWaddress           Flags Mask     Iface
192.168.1.1     ether   00:50:56:c0:00:08   C              eth0
192.168.1.20    ether   18:ac:33:12:88:29   C              eth0

# Method 2: ip command (modern)
$ ip neighbor show
192.168.1.1 dev eth0 lladdr 00:50:56:c0:00:08 REACHABLE
192.168.1.20 dev eth0 lladdr 18:ac:33:12:88:29 STALE
```

**Entry Types:**
- **Dynamic:** Learned via ARP, expires after timeout (typically 2-10 minutes)
- **Static:** Manually configured, never expires
- **REACHABLE:** Recently confirmed active
- **STALE:** Not recently confirmed, may be outdated
- **INCOMPLETE:** ARP request sent but no reply yet

**Managing ARP Cache:**
```bash
# Clear entire ARP cache (Windows)
arp -d *

# Clear specific entry (Windows)
arp -d 192.168.1.20

# Clear ARP cache (Linux)
sudo ip neighbor flush all

# Add static ARP entry (Windows)
arp -s 192.168.1.20 18-ac-33-12-88-29

# Add static ARP entry (Linux)
sudo arp -s 192.168.1.20 18:ac:33:12:88:29
```

#### ARP Security Concerns

**ARP Spoofing/Poisoning Attack:**

**Attack Scenario:**
1. Attacker sends fake ARP replies:
   ```
   "192.168.1.1 (gateway) is at AA:BB:CC:DD:EE:FF (attacker's MAC)"
   ```
2. Victim caches this fake entry
3. All traffic to gateway now goes to attacker
4. Attacker can intercept, modify, or drop traffic
5. This is a **Man-in-the-Middle (MITM)** attack

**Real-World Impact:**
- Password theft
- Session hijacking
- Data exfiltration
- Network disruption (DoS)

**Detection:**
- Monitoring for duplicate IP-to-MAC mappings
- Watching for ARP replies without ARP requests
- Tracking sudden MAC address changes for critical IPs (gateway, DNS server)

**Defenses:**
1. **Static ARP entries** (for critical devices like gateway)
2. **Dynamic ARP Inspection (DAI)** on switches:
   ```
   ip arp inspection vlan 10
   interface GigabitEthernet0/1
     ip arp inspection trust
   ```
3. **DHCP Snooping** (prevents rogue DHCP servers that enable ARP attacks)
4. **Network segmentation** (limits attack scope)
5. **ARP monitoring tools:** arpwatch (Linux), XArp (Windows)

**NOC Response to ARP Attack:**
```bash
# Check for duplicate IPs
arp -a | sort

# Monitor ARP changes in real-time (Linux)
sudo tcpdump -i eth0 arp -vv

# Check switch for MAC flapping
show mac address-table | include [suspicious_MAC]
show logging | include MACFLAP
```

#### ARP and Routers

**Critical Limitation:** ARP only works on the **local network segment**.

**Why?**
- ARP uses broadcast (FF:FF:FF:FF:FF:FF)
- Routers do NOT forward broadcasts
- Therefore, ARP cannot cross subnets

**Example:**
```
Computer A: 192.168.1.10 (Subnet 1)
Computer B: 192.168.2.20 (Subnet 2)
Router: 192.168.1.1 (Subnet 1 side), 192.168.2.1 (Subnet 2 side)

Computer A cannot ARP for Computer B directly.
Instead:
1. Computer A ARPs for default gateway (192.168.1.1)
2. Computer A sends packet to router
3. Router strips off Layer 2 header (Computer A's MAC)
4. Router adds new Layer 2 header with router's MAC
5. Router forwards to Computer B's subnet
6. On Subnet 2, router ARPs for Computer B (192.168.2.20)
7. Communication proceeds
```

**Key Insight:** MAC addresses change at every Layer 3 hop (router), but IP addresses remain the same (until NAT).

---

### DHCP (Dynamic Host Configuration Protocol)

**Purpose:** Automatically assign IP addresses and network configuration to devices.

**Why DHCP?**
- Manual IP assignment doesn't scale (imagine configuring 1,000+ devices)
- Prevents IP conflicts (DHCP tracks assignments)
- Centralized management (change network settings in one place)
- IP address recycling (release unused IPs)

#### DHCP Process: DORA

**D**iscover → **O**ffer → **R**equest → **A**cknowledge

**Step 1: DHCP Discover (Broadcast)**
```
Client: "Hey! I'm new here. Is there anyone who can give me an IP address?"

Packet details:
  Source IP:    0.0.0.0 (client has no IP yet)
  Dest IP:      255.255.255.255 (broadcast)
  Source MAC:   [Client's MAC]
  Dest MAC:     FF:FF:FF:FF:FF:FF (broadcast)
  Message:      DHCP Discover
```

**Step 2: DHCP Offer (Broadcast or Unicast)**
```
DHCP Server: "Sure! You can have 192.168.1.10. Here are the details."

Packet details:
  Source IP:    192.168.1.1 (DHCP server)
  Dest IP:      255.255.255.255 (often broadcast) or client IP
  Message:      DHCP Offer
  Offered IP:   192.168.1.10
  Subnet:       255.255.255.0
  Gateway:      192.168.1.1
  DNS:          8.8.8.8, 8.8.4.4
  Lease time:   86400 seconds (24 hours)
```

**Step 3: DHCP Request (Broadcast)**
```
Client: "Yes! I'll take 192.168.1.10. Please reserve it for me."

Packet details:
  Source IP:    0.0.0.0 (still no IP officially)
  Dest IP:      255.255.255.255 (broadcast - tells all DHCP servers)
  Message:      DHCP Request
  Requested IP: 192.168.1.10

Why broadcast? If multiple DHCP servers offered IPs, this tells 
the rejected servers that client chose a different offer.
```

**Step 4: DHCP ACK (Acknowledgment - Broadcast or Unicast)**
```
DHCP Server: "Okay, great! 192.168.1.10 is now officially yours for 24 hours."

Packet details:
  Source IP:    192.168.1.1
  Dest IP:      192.168.1.10 (or broadcast)
  Message:      DHCP ACK
  
Client now configures itself:
  - IP: 192.168.1.10/24
  - Gateway: 192.168.1.1
  - DNS: 8.8.8.8, 8.8.4.4
  - Starts lease timer
```

#### DHCP Lease Management

**Lease Duration:**
- Typical: 24 hours (86,400 seconds)
- Can be as short as minutes or as long as weeks
- Shorter leases = more DHCP traffic, better for dynamic environments (guest WiFi)
- Longer leases = less DHCP traffic, better for stable environments (office)

**Lease Renewal Process:**

**T1 Timer (50% of lease - 12 hours for 24-hour lease):**
```
Client sends DHCP Request directly to original DHCP server:
  "Can I renew my lease for 192.168.1.10?"
  
If server responds with DHCP ACK:
  Lease renewed for another full period
  
If no response:
  Wait for T2 timer
```

**T2 Timer (87.5% of lease - 21 hours for 24-hour lease):**
```
Client broadcasts DHCP Request:
  "Any DHCP server - can I renew 192.168.1.10?"
  
If any server responds with DHCP ACK:
  Lease renewed
  
If no response by lease expiration:
  Client must release IP and start DORA process over
```

**Lease Release:**
```
Client sends DHCP Release when disconnecting:
  "I'm done with 192.168.1.10. You can give it to someone else."
  
Server marks IP as available in pool.
```

#### DHCP Server Configuration

**Information DHCP Provides:**

| Parameter       | Description                              | Example              |
|-----------------|------------------------------------------|----------------------|
| IP Address      | Device's unique address                  | 192.168.1.100        |
| Subnet Mask     | Network boundary                         | 255.255.255.0        |
| Default Gateway | Router for external communication        | 192.168.1.1          |
| DNS Servers     | Domain name resolution                   | 8.8.8.8, 1.1.1.1     |
| Lease Duration  | How long IP is valid                     | 86400 sec (24 hrs)   |
| Domain Name     | Local domain                             | company.local        |
| TFTP Server     | For PXE boot                             | 192.168.1.50         |
| NTP Server      | Time synchronization                     | pool.ntp.org         |

**DHCP Scope Example (Windows Server):**
```
Scope: IT_Department
  IP Range:       192.168.10.100 - 192.168.10.200
  Subnet:         255.255.255.0
  Gateway:        192.168.10.1
  DNS:            192.168.1.5, 8.8.8.8
  Lease:          8 hours
  Exclusions:     192.168.10.150-192.168.10.160 (static servers)
  Reservations:   00:50:56:AA:BB:CC → 192.168.10.50 (printer)
```

#### DHCP Relay (IP Helper)

**Problem:** DHCP uses broadcasts, which don't cross routers.

**Scenario:**
```
Subnet 1 (192.168.1.0/24)
  ├── DHCP Server (192.168.1.5)
  └── Clients
  
Router
  
Subnet 2 (192.168.2.0/24)
  └── Clients (no DHCP server here)
```

**Without DHCP Relay:**
- Clients in Subnet 2 broadcast DHCP Discover
- Router blocks broadcast
- Clients get no IP address (DHCP fails)

**With DHCP Relay:**
- Router configured with "IP helper address" pointing to DHCP server
- Client in Subnet 2 broadcasts DHCP Discover
- Router converts broadcast to unicast, forwards to DHCP server (192.168.1.5)
- DHCP server sends offer back through router
- Router forwards to client
- Process completes successfully

**Cisco Configuration:**
```
interface GigabitEthernet0/1
  description Subnet 2 - no local DHCP
  ip address 192.168.2.1 255.255.255.0
  ip helper-address 192.168.1.5
```

#### DHCP Security

**Rogue DHCP Server Attack:**
1. Attacker sets up unauthorized DHCP server
2. Attacker's server responds faster than legitimate server
3. Clients get malicious configuration:
   - Wrong gateway IP (attacker's IP) → MITM attack
   - Wrong DNS server → DNS poisoning
   - No gateway → denial of service

**DHCP Starvation Attack:**
1. Attacker requests thousands of IP addresses
2. DHCP pool exhausted
3. Legitimate clients cannot get IPs
4. Network denial of service

**Defenses:**

**1. DHCP Snooping (Cisco switches):**
```
ip dhcp snooping
ip dhcp snooping vlan 10

interface GigabitEthernet0/24
  description Uplink to DHCP Server
  ip dhcp snooping trust

# All other ports untrusted by default
# Untrusted ports can only send DHCP requests (not offers/acks)
```

**2. Port Security:**
```
interface range GigabitEthernet0/1-23
  switchport port-security
  switchport port-security maximum 1
  switchport port-security violation shutdown
```

**3. Monitoring:**
```bash
# View DHCP leases (Linux server)
cat /var/lib/dhcp/dhcpd.leases

# View DHCP snooping binding (Cisco)
show ip dhcp snooping binding

# Monitor DHCP traffic
sudo tcpdump -i eth0 port 67 or port 68 -vv
```

**NOC Troubleshooting:**
```bash
# Client can't get IP - check these:

1. Client side:
   ipconfig /release
   ipconfig /renew
   
2. Verify DHCP server is reachable:
   ping [DHCP_server_IP]
   
3. Check if client is sending DHCP Discover:
   sudo tcpdump -i eth0 port 67 or port 68
   
4. Check DHCP server logs:
   tail -f /var/log/syslog | grep dhcp
   
5. Verify DHCP pool not exhausted:
   show ip dhcp pool
   show ip dhcp binding
   
6. Check DHCP relay (if different subnet):
   show ip interface [interface] | include Helper
```

---

## Network Topologies

Network topology refers to the physical or logical arrangement of devices in a network. Understanding topologies is essential for NOC work because it affects troubleshooting approach, network performance, and failure scenarios.

### Star Topology

**Design:**
- All devices connect to a central device (switch or hub)
- Most common topology in modern networks
- Used in: Offices, data centers, homes (via wireless access points)

**Advantages:**
✅ **Scalability:** Easy to add new devices (just plug into switch)  
✅ **Isolation:** One device failure doesn't affect others  
✅ **Easy troubleshooting:** Problem traced to specific port/device  
✅ **Performance:** Dedicated bandwidth per device (with switches)  
✅ **Centralized management:** Monitor/configure from central device

**Disadvantages:**
❌ **Cost:** Requires switch/hub + more cabling  
❌ **Single point of failure:** If central device fails, entire network down  
❌ **Cable requirements:** More cabling than bus topology  
❌ **Physical space:** All cables must reach central point

**NOC Considerations:**
- Central switch is critical infrastructure (use redundant power, quality hardware)
- Monitor switch health closely (temperature, port status, error counters)
- Map which devices connect to which ports for faster troubleshooting
- Consider stacking switches or using redundant switches for high availability

**Troubleshooting Star Topology:**
```
User reports: "I can't access the network."

Diagnostic steps:
1. Can user ping own IP? → Tests NIC
2. Can user ping gateway? → Tests switch connectivity
3. Can other users ping gateway? → Differentiates device vs switch issue
4. Check switch port status:
   show interface gi0/5
   show interface gi0/5 status
5. Check for errors on port:
   show interface gi0/5 | include error
6. Check if port is disabled:
   show running-config interface gi0/5

If all ports down → Central switch failure
If one port down → Cable, port, or device NIC issue
```

---

### Bus Topology

**Design:**
- All devices connect to a single cable (backbone/trunk)
- Data travels along cable until it reaches destination
- Terminators at both ends prevent signal reflection

**Advantages:**
✅ **Cost-effective:** Minimal cabling required  
✅ **Simple installation:** Just tap into backbone cable  
✅ **Good for small networks:** 5-10 devices

**Disadvantages:**
❌ **Single point of failure:** Cable break = entire network down  
❌ **Performance degradation:** More devices = more collisions, slower network  
❌ **Difficult troubleshooting:** Hard to identify which device causing issues  
❌ **Scalability limitations:** Adding devices increases collision domain  
❌ **Cable length limits:** Signal degrades over distance  
❌ **No fault isolation:** One malfunctioning device can bring down network

**Why Rarely Used Today:**
- Ethernet hubs (which create bus topology electrically) replaced by switches
- Collision domains are inefficient compared to switched networks
- Fiber optic and modern twisted pair don't support bus topology well

**Historical Context:**
- Common in early Ethernet (10BASE-2, 10BASE-5)
- Thick coaxial cable (10BASE-5) or thin coaxial (10BASE-2)
- "Vampire taps" physically punctured cable to connect devices

**NOC Note:** If you encounter bus topology, it's likely a legacy network requiring urgent upgrade.

---

### Ring Topology

**Design:**
- Devices connected in a closed loop
- Data travels in one direction (or both in dual-ring)
- Each device acts as a repeater, forwarding data to next device
- Also known as "Token Ring" topology

**How It Works:**
1. Device has data to send → waits for "token" (permission to transmit)
2. Device captures token, sends data
3. Data passes device-to-device around ring until reaching destination
4. Destination copies data, marks as received
5. Data continues to sender
6. Sender removes data from ring, releases token

**Advantages:**
✅ **Predictable performance:** Token prevents collisions  
✅ **Equal access:** Every device gets fair chance to transmit  
✅ **No collisions:** Token-based access control  
✅ **Easy fault detection:** Break in ring is quickly identified  
✅ **Can cover longer distances:** Each device regenerates signal

**Disadvantages:**
❌ **Single point of failure:** One broken device or cable = network down  
❌ **Reconfiguration challenges:** Adding/removing devices disrupts network  
❌ **Slower than switched networks:** Data may traverse many devices  
❌ **Troubleshooting complexity:** Must trace ring to find issue  
❌ **Unidirectional:** Data must travel full circle (inefficient for nearby devices)

**Modern Implementation: FDDI (Fiber Distributed Data Interface):**
- Dual counter-rotating rings (redundancy)
- If primary ring breaks, secondary ring activates
- Creates self-healing network
- Used in: Campus backbones, critical infrastructure

**Token Ring (IEEE 802.5):**
- Obsolete technology, replaced by Ethernet
- Speeds: 4 Mbps or 16 Mbps (vs Gigabit+ Ethernet)
- Required special Token Ring NICs and MAUs (Multistation Access Units)

**NOC Note:** Ring topologies rare in modern LANs but still used in metropolitan area networks (MANs) and SONET/SDH telecommunications.

---

### Mesh Topology

**Design:**
- Every device connected to every other device (full mesh)
- Or many connections but not all (partial mesh)

**Full Mesh:**
- n devices require n(n-1)/2 connections
- Example: 5 devices = 5(4)/2 = 10 connections
- Example: 10 devices = 10(9)/2 = 45 connections

**Advantages:**
✅ **Redundancy:** Multiple paths between any two devices  
✅ **Fault tolerance:** If one link fails, traffic reroutes  
✅ **No single point of failure:** Network stays operational  
✅ **Load balancing:** Traffic can use multiple paths  
✅ **High availability:** Critical for enterprise/data center

**Disadvantages:**
❌ **Expensive:** Requires massive cabling/interfaces  
❌ **Complex:** Difficult to configure and maintain  
❌ **Scalability issues:** Connections grow exponentially  
❌ **Overkill for small networks**

**Use Cases:**
- Internet backbone (partial mesh)
- Data center interconnects
- Wireless mesh networks (WiFi extenders)
- Critical infrastructure (financial, healthcare)

**NOC Application:**
- Understand redundant paths for troubleshooting
- If one link down, verify traffic successfully rerouted
- Monitor all links (not just primary) for degradation

---

### Hybrid Topologies

**Definition:** Combination of two or more basic topologies.

**Common Example: Star-Bus Hybrid**
- Multiple star networks connected via backbone (bus)
- Each office/floor has star topology
- Stars connected via building backbone

**Advantages:**
- Leverages benefits of multiple topologies
- Flexible design for complex environments
- Scalable while maintaining performance

---

## Network Devices

### Switches (Layer 2 Devices)

**Purpose:** Connect multiple devices on the same network, forward traffic based on MAC addresses.

**How Switches Work:**

**1. MAC Address Learning:**
```
Frame arrives on Port 1:
  Source MAC: AA:BB:CC:DD:EE:FF
  
Switch thinks: "AA:BB:CC:DD:EE:FF is on Port 1"
Switch adds to MAC address table:
  Port 1 → AA:BB:CC:DD:EE:FF
```

**2. Forwarding Decision:**
```
Frame has Destination MAC: 11:22:33:44:55:66

Switch checks table:
  - If MAC in table → Forward to that port only
  - If MAC not in table → Flood to all ports except source
  - If MAC is broadcast (FF:FF:FF:FF:FF:FF) → Flood to all ports except source
```

**3. MAC Address Table Management:**
- **Learning:** Constantly updates as frames arrive
- **Aging:** Entries expire after timeout (typically 300 seconds / 5 minutes)
- **Size:** Enterprise switches: 8K-32K MACs, Data center switches: 128K+ MACs

**Switch vs. Hub:**

| Feature              | Hub                        | Switch                          |
|----------------------|----------------------------|---------------------------------|
| OSI Layer            | Physical (Layer 1)         | Data Link (Layer 2)             |
| Forwarding           | Floods to all ports        | Intelligent, MAC-based          |
| Bandwidth            | Shared among all devices   | Dedicated per port              |
| Collision Domain     | Single (all ports)         | Separate per port               |
| Performance          | Poor (collisions)          | Excellent                       |
| Price                | Cheap                      | More expensive                  |
| Use Today            | Obsolete                   | Standard                        |

**Switch Port Counts:**
- Small office: 8-port, 16-port, 24-port
- Enterprise: 48-port (most common)
- Data center: 48-port + high-density modules

**Switch Types:**

**1. Unmanaged Switch:**
- Plug and play, no configuration
- No CLI/GUI access
- Fixed operation
- Home/small office use

**2. Managed Switch:**
- Full configuration capability
- VLANs, QoS, port security, monitoring
- CLI and/or web interface
- Enterprise standard

**3. Layer 3 Switch:**
- Switch + Router capabilities
- Can route between VLANs
- Faster than external router for inter-VLAN routing

**Key Switch Concepts for NOC:**

**VLANs (Virtual LANs):**
```
Physical switch logically divided:
  VLAN 10: Engineering
  VLAN 20: HR
  VLAN 30: Guest

Devices in VLAN 10 can only talk to other VLAN 10 devices
(unless router/Layer 3 switch routes between VLANs)

Benefits:
- Segmentation (security)
- Broadcast domain control
- Logical grouping regardless of physical location
```

**Spanning Tree Protocol (STP):**
- Prevents Layer 2 loops
- If redundant switch links exist, STP blocks redundant paths
- If primary path fails, STP activates backup path
- Without STP: Broadcast storms (network meltdown)

**Port Mirroring (SPAN):**
```
Copy traffic from Port 1 to Port 24 for monitoring:
  
monitor session 1 source interface gi0/1
monitor session 1 destination interface gi0/24

Use case: Connect packet analyzer to Port 24 to capture Port 1 traffic
```

**Switch Commands (Cisco):**
```
# View MAC address table
show mac address-table

# View specific port status
show interface gi0/1 status
show interface gi0/1

# View port statistics (errors, collisions, etc.)
show interface gi0/1 | include error|collision|CRC

# View VLANs
show vlan brief

# View STP status
show spanning-tree

# View port security
show port-security interface gi0/1
```

---

### Routers (Layer 3 Devices)

**Purpose:** Connect different networks, forward traffic based on IP addresses, make routing decisions.

**Router vs. Switch:**

| Feature              | Switch                     | Router                          |
|----------------------|----------------------------|---------------------------------|
| OSI Layer            | Layer 2                    | Layer 3                         |
| Forwards based on    | MAC addresses              | IP addresses                    |
| Scope                | Local network (same subnet)| Between networks (subnets)      |
| Broadcasts           | Forwards within VLAN       | Blocks broadcasts               |
| Address type         | Physical (MAC)             | Logical (IP)                    |
| Primary function     | Segment collision domains  | Segment broadcast domains       |

**How Routers Work:**

**1. Routing Table:**
```
Destination Network  Next Hop        Interface   Metric
192.168.1.0/24      Directly Conn.  Gi0/0       0
192.168.2.0/24      Directly Conn.  Gi0/1       0
10.0.0.0/8          192.168.1.254   Gi0/0       10
0.0.0.0/0 (default) 203.0.113.1     Gi0/2       1

Router receives packet destined for 10.5.5.5:
1. Checks routing table
2. Best match: 10.0.0.0/8 (matches 10.5.5.5)
3. Forwards to next hop: 192.168.1.254 via Gi0/0
```

**2. Packet Forwarding Process:**
```
Packet arrives at Router:
  Source IP: 192.168.1.10
  Dest IP: 192.168.2.20
  Source MAC: AA:BB:CC:DD:EE:FF (Computer A)
  Dest MAC: 11:22:33:44:55:66 (Router's Gi0/0 MAC)

Router performs:
1. Strips Layer 2 header (removes Computer A's MAC)
2. Checks routing table for 192.168.2.0/24
3. Finds it's directly connected on Gi0/1
4. ARPs for 192.168.2.20 on Gi0/1 subnet
5. Adds new Layer 2 header with:
   - Source MAC: Router's Gi0/1 MAC
   - Dest MAC: Computer B's MAC (from ARP)
6. Forwards packet out Gi0/1

Key insight: IP addresses unchanged, MAC addresses replaced at each hop
```

**3. Routing Protocols:**

**Purpose:** Routers share routing information with each other to build routing tables automatically.

**Static Routing:**
```
# Manually configure route
ip route 10.5.5.0 255.255.255.0 192.168.1.254

Advantages:
- Predictable
- No protocol overhead
- Secure (no route advertisements)

Disadvantages:
- Manual configuration
- No automatic failover
- Doesn't scale
```

**Dynamic Routing Protocols:**

**RIP (Routing Information Protocol):**
- Distance vector protocol
- Metric: Hop count (max 15 hops)
- Updates every 30 seconds
- Legacy, rarely used today
- Simple but inefficient

**OSPF (Open Shortest Path First):**
- Link-state protocol
- Metric: Cost (based on bandwidth)
- Hierarchical (areas) for scalability
- Fast convergence
- Industry standard for enterprise

**EIGRP (Enhanced Interior Gateway Routing Protocol):**
- Cisco proprietary (now available on other vendors)
- Hybrid protocol (distance vector + link-state features)
- Fast convergence
- Low bandwidth usage

**BGP (Border Gateway Protocol):**
- Path vector protocol
- Routes between autonomous systems (AS)
- Runs the Internet
- Used by ISPs
- Complex, policy-based

**Routing Decision Factors (from TryHackMe):**
1. **Shortest path:** Fewest hops/lowest cost
2. **Reliability:** Avoid paths with packet loss
3. **Speed:** Faster physical connection (fiber > copper)

**Router Commands (Cisco):**
```
# View routing table
show ip route

# View specific route
show ip route 10.5.5.0

# View OSPF neighbors
show ip ospf neighbor

# View OSPF database
show ip ospf database

# View BGP summary
show ip bgp summary

# View interface status
show ip interface brief

# Test routing
ping 10.5.5.5
traceroute 10.5.5.5
```

**NAT (Network Address Translation):**

**Purpose:** Allow multiple private IP devices to share one public IP address.

**Types:**

**1. Static NAT (1:1 mapping):**
```
Private IP      Public IP
192.168.1.10 ←→ 203.0.113.5

Always same translation
Used for servers that need consistent public IP
```

**2. Dynamic NAT (Pool mapping):**
```
Private IPs: 192.168.1.0/24
Public IP Pool: 203.0.113.5 - 203.0.113.10

First device gets .5, second gets .6, etc.
When device disconnects, public IP returns to pool
```

**3. PAT (Port Address Translation / NAT Overload):**
```
Private IP:Port        Public IP:Port
192.168.1.10:5000  →  203.0.113.5:50000
192.168.1.11:6000  →  203.0.113.5:50001
192.168.1.12:7000  →  203.0.113.5:50002

Many private IPs share ONE public IP
Different source ports differentiate connections
This is what home routers use
```

**How PAT Works:**
```
Internal device 192.168.1.10 browses to 1.1.1.1:80

Outbound packet:
  Source: 192.168.1.10:5000
  Dest: 1.1.1.1:80

Router translates:
  Source: 203.0.113.5:50000 (router's public IP + unique port)
  Dest: 1.1.1.1:80

Router stores in NAT table:
  192.168.1.10:5000 ←→ 203.0.113.5:50000

Return packet from 1.1.1.1:
  Source: 1.1.1.1:80
  Dest: 203.0.113.5:50000

Router looks up 50000 in table, finds 192.168.1.10:5000
Translates back:
  Source: 1.1.1.1:80
  Dest: 192.168.1.10:5000

Delivers to internal device
```

**NOC Troubleshooting - Routers:**
```
User: "Can't reach the Internet"

Diagnostic path:
1. Can user ping gateway?
   ping 192.168.1.1 → Tests local network
   
2. Can user ping external IP?
   ping 8.8.8.8 → Tests routing without DNS
   
3. Can user ping domain name?
   ping google.com → Tests DNS resolution
   
4. Check user's routing table:
   route print (Windows) / ip route show (Linux)
   
5. Check router's routing table:
   show ip route
   
6. Trace path to destination:
   traceroute 8.8.8.8
   
   If stops at first hop → Gateway issue
   If stops at ISP → ISP routing issue
   If reaches destination → DNS or application issue
```

---

## Subnetting Deep Dive

**Critical Note:** The TryHackMe content on subnetting was extremely brief. This section provides the comprehensive technical detail required for NOC work.

### Why Subnetting Matters

**Without Subnetting:**
- All devices in one broadcast domain
- Broadcast storms (ARP, DHCP, NetBIOS, etc.)
- Security nightmare (every device sees every packet)
- No logical segmentation
- Difficult to manage

**With Subnetting:**
- Logical network segmentation
- Reduced broadcast traffic
- Improved security (VLANs + subnets)
- Easier troubleshooting (isolate issues to specific subnet)
- Efficient IP address utilization
- Hierarchical network design

### IP Address Classes (Historical Context)

**Classful Addressing (Obsolete but important to understand):**

| Class | First Octet Range | Default Subnet Mask | Network Bits | Host Bits | # Networks | # Hosts/Network |
|-------|-------------------|---------------------|--------------|-----------|------------|-----------------|
| A     | 1-126             | 255.0.0.0           | 8            | 24        | 126        | 16,777,214      |
| B     | 128-191           | 255.255.0.0         | 16           | 16        | 16,384     | 65,534          |
| C     | 192-223           | 255.255.255.0       | 24           | 8         | 2,097,152  | 254             |
| D     | 224-239           | N/A (Multicast)     | N/A          | N/A       | N/A        | N/A             |
| E     | 240-255           | N/A (Reserved)      | N/A          | N/A       | N/A        | N/A             |

**Special Addresses:**
- `127.0.0.0/8`: Loopback (127.0.0.1 most common)
- `0.0.0.0`: Default route, unspecified address
- `255.255.255.255`: Limited broadcast

**Why Classful is Obsolete:**
- Wasteful (Class A gives 16M addresses to single org)
- Inflexible (stuck with /8, /16, or /24)
- Exhausted IP space quickly

**Modern Solution: CIDR (Classless Inter-Domain Routing)**
- Any subnet mask length allowed
- Example: /25, /26, /27, /28, /30, etc.
- Efficient address allocation
- Variable-Length Subnet Masking (VLSM)

### Subnet Mask Mechanics

**Binary Representation:**

**Subnet Mask Purpose:** Divide IP address into **Network portion** and **Host portion**.

**Example: 255.255.255.0**
```
Decimal:  255      .255      .255      .0
Binary:   11111111.11111111.11111111.00000000
          ^^^^^^^^ ^^^^^^^^ ^^^^^^^^ ^^^^^^^^
          Network  Network  Network  Host

All 1s = Network bits (cannot change, identifies the network)
All 0s = Host bits (can change, identifies devices within network)
```

**IP Address Breakdown:**
```
IP Address:    192.168.1.100
Subnet Mask:   255.255.255.0

Binary IP:     11000000.10101000.00000001.01100100
Binary Mask:   11111111.11111111.11111111.00000000
               ^^^^^^^^ ^^^^^^^^ ^^^^^^^^ ^^^^^^^^
               Network portion   Host

Network Address (all host bits = 0):  192.168.1.0
Broadcast (all host bits = 1):        192.168.1.255
Usable range:                         192.168.1.1 - 192.168.1.254
```

### CIDR Notation

**Format:** `IP_address/prefix_length`

**Examples:**
- `192.168.1.0/24` = 255.255.255.0 (24 network bits, 8 host bits)
- `10.0.0.0/8` = 255.0.0.0 (8 network bits, 24 host bits)
- `172.16.0.0/16` = 255.255.0.0 (16 network bits, 16 host bits)
- `192.168.1.0/25` = 255.255.255.128 (25 network bits, 7 host bits)

**CIDR to Subnet Mask Conversion:**

| CIDR | Subnet Mask       | Binary Last Octet |
|------|-------------------|-------------------|
| /24  | 255.255.255.0     | 00000000          |
| /25  | 255.255.255.128   | 10000000          |
| /26  | 255.255.255.192   | 11000000          |
| /27  | 255.255.255.224   | 11100000          |
| /28  | 255.255.255.240   | 11110000          |
| /29  | 255.255.255.248   | 11111000          |
| /30  | 255.255.255.252   | 11111100          |
| /31  | 255.255.255.254   | 11111110          |
| /32  | 255.255.255.255   | 11111111          |

### Calculating Subnets

**Formula Reference:**

**Number of Subnets:**
```
2^(borrowed_bits) = Number of subnets

Example: /24 network subnetted to /26
Borrowed bits = 26 - 24 = 2
2^2 = 4 subnets
```

**Number of Hosts per Subnet:**
```
2^(host_bits) - 2 = Usable hosts

Why -2? 
  - Network address (all host bits = 0)
  - Broadcast address (all host bits = 1)

Example: /26 network
Host bits = 32 - 26 = 6
2^6 - 2 = 64 - 2 = 62 usable hosts
```

**Subnet Size (Block Size):**
```
256 - last_octet_of_subnet_mask = Block size

Example: /26 = 255.255.255.192
256 - 192 = 64
Subnets increment by 64
```

### Practical Subnetting Examples

**Example 1: Standard /24 Network**

```
Network: 192.168.1.0/24
Subnet Mask: 255.255.255.0

Network Address:    192.168.1.0
First usable IP:    192.168.1.1 (typically gateway)
Last usable IP:     192.168.1.254
Broadcast:          192.168.1.255
Total IPs:          256
Usable hosts:       254 (256 - 2)
```

**Use Case:** Small to medium office (up to 254 devices)

---

**Example 2: Subdividing /24 into /26 Subnets**

```
Original: 192.168.1.0/24
Goal: Create 4 subnets with ~60 hosts each
Solution: Use /26 (255.255.255.192)

Calculations:
- Borrowed bits: 2 (26 - 24 = 2)
- Number of subnets: 2^2 = 4 ✓
- Host bits: 32 - 26 = 6
- Hosts per subnet: 2^6 - 2 = 62 ✓
- Block size: 256 - 192 = 64

Subnet 1: 192.168.1.0/26
  Network:     192.168.1.0
  First Host:  192.168.1.1
  Last Host:   192.168.1.62
  Broadcast:   192.168.1.63

Subnet 2: 192.168.1.64/26
  Network:     192.168.1.64
  First Host:  192.168.1.65
  Last Host:   192.168.1.126
  Broadcast:   192.168.1.127

Subnet 3: 192.168.1.128/26
  Network:     192.168.1.128
  First Host:  192.168.1.129
  Last Host:   192.168.1.190
  Broadcast:   192.168.1.191

Subnet 4: 192.168.1.192/26
  Network:     192.168.1.192
  First Host:  192.168.1.193
  Last Host:   192.168.1.254
  Broadcast:   192.168.1.255
```

**Use Case:** Office with 4 departments, each needing isolated subnet

---

**Example 3: Point-to-Point Links (/30)**

```
Goal: Connect two routers with minimal IP waste
Solution: /30 (255.255.255.252)

Calculations:
- Host bits: 32 - 30 = 2
- Total IPs: 2^2 = 4
- Usable hosts: 4 - 2 = 2 (perfect for 2 routers)
- Block size: 256 - 252 = 4

Example Link: 10.0.0.0/30
  Network:     10.0.0.0
  Router A:    10.0.0.1
  Router B:    10.0.0.2
  Broadcast:   10.0.0.3

Next link: 10.0.0.4/30, then 10.0.0.8/30, etc.
```

**Use Case:** WAN links, router-to-router connections

---

**Example 4: Variable-Length Subnet Masking (VLSM)**

```
Scenario: Company has 192.168.10.0/24, needs:
  - Server subnet: 30 hosts
  - Sales dept: 50 hosts
  - Engineering: 100 hosts
  - Guest WiFi: 20 hosts
  - WAN link to ISP: 2 IPs

Solution: Different subnet sizes based on needs

1. Engineering (100 hosts):
   Requirement: 100 hosts → need 2^7 = 128 IPs → /25
   192.168.10.0/25
   Range: 192.168.10.0 - 192.168.10.127 (126 usable)

2. Sales (50 hosts):
   Requirement: 50 hosts → need 2^6 = 64 IPs → /26
   192.168.10.128/26
   Range: 192.168.10.128 - 192.168.10.191 (62 usable)

3. Server subnet (30 hosts):
   Requirement: 30 hosts → need 2^5 = 32 IPs → /27
   192.168.10.192/27
   Range: 192.168.10.192 - 192.168.10.223 (30 usable)

4. Guest WiFi (20 hosts):
   Requirement: 20 hosts → need 2^5 = 32 IPs → /27
   192.168.10.224/27
   Range: 192.168.10.224 - 192.168.10.255 (30 usable)

5. WAN link (2 IPs):
   From another subnet or use 192.168.11.0/30
```

**Benefits of VLSM:**
- Efficient IP usage (no wasted addresses)
- Right-sized subnets for each department
- Room for future growth

---

### Special Subnet Addresses

**Network Address (All Host Bits = 0):**
- Identifies the subnet itself
- Cannot be assigned to a device
- Used in routing tables
- Example: 192.168.1.0/24 (network address is 192.168.1.0)

**Broadcast Address (All Host Bits = 1):**
- Sends to all devices in subnet
- Cannot be assigned to a device
- Example: 192.168.1.0/24 (broadcast is 192.168.1.255)

**Directed Broadcast:**
- Broadcast to specific subnet
- Example: Ping 192.168.1.255 (broadcasts to all devices in 192.168.1.0/24)

**Limited Broadcast:**
- 255.255.255.255
- Broadcast to local subnet only
- Doesn't cross routers

**Default Gateway:**
- Router interface on subnet
- Typically first usable IP (.1) or last usable IP (.254)
- Example: 192.168.1.1 for 192.168.1.0/24 network

### Three Key Address Types from TryHackMe

| Type              | Purpose                                      | Example (192.168.1.0/24) |
|-------------------|----------------------------------------------|--------------------------|
| Network Address   | Identifies the subnet, used in routing       | 192.168.1.0              |
| Host Address      | Assigned to actual devices                   | 192.168.1.100            |
| Default Gateway   | Router for external traffic                  | 192.168.1.1 (or .254)    |

### Subnetting Benefits

**1. Efficiency:**
- Reduce broadcast traffic (broadcasts confined to subnet)
- Better bandwidth utilization
- Less congestion

**2. Security:**
- Isolate sensitive systems (servers, finance, HR)
- Control traffic flow with ACLs
- Contain security breaches to one subnet
- Example: Guest WiFi on separate subnet can't reach corporate network

**3. Full Control:**
- Granular network design
- Traffic engineering (QoS per subnet)
- Scalability (add subnets as needed)
- Logical organization matches business structure

### Real-World Subnetting (TryHackMe Café Example)

**Scenario:** Coffee shop with two networks

**Network 1: Employee Network (192.168.10.0/24)**
- Cash registers: 192.168.10.10-20
- POS system: 192.168.10.50
- Office computers: 192.168.10.100-110
- Security cameras: 192.168.10.200-210
- Gateway: 192.168.10.1
- No public access

**Network 2: Guest WiFi (192.168.20.0/24)**
- DHCP pool: 192.168.20.100-200
- Gateway: 192.168.20.1
- Isolated from employee network (firewall rules)
- Internet access only

**Security Implementation:**
```
Firewall rules:
- 192.168.20.0/24 → Internet: ALLOW
- 192.168.20.0/24 → 192.168.10.0/24: DENY
- 192.168.10.0/24 → Internet: ALLOW
- 192.168.10.0/24 → Any: ALLOW (internal access)
```

**Benefits:**
- Guests can't access cash registers or cameras
- Employee traffic prioritized (QoS)
- Separate DHCP scopes
- If guest network compromised, employee network safe

### NOC Subnetting Applications

**1. Troubleshooting:**
```
User: "I can't reach the server."

Questions to ask:
- What's your IP? 192.168.1.50
- What's the server IP? 192.168.2.100

Analysis:
- User: 192.168.1.50 (likely /24 → 192.168.1.0/24)
- Server: 192.168.2.100 (likely /24 → 192.168.2.0/24)
- Different subnets → Traffic must go through router
- Check: Can user ping gateway (192.168.1.1)?
- Check: Does router have route to 192.168.2.0/24?
- Check: Is there ACL blocking 192.168.1.x → 192.168.2.x?
```

**2. IP Planning:**
```
New office needs network design:
- 500 employees
- 50 servers
- 30 printers
- 20 VoIP phones (separate VLAN for QoS)
- Guest WiFi

Design:
- Employee: 10.10.0.0/23 (510 hosts)
- Servers: 10.10.2.0/26 (62 hosts)
- Printers: 10.10.2.64/27 (30 hosts)
- VoIP: 10.10.2.96/27 (30 hosts - separate for QoS)
- Guest: 10.10.3.0/24 (254 hosts)
```

**3. Documentation:**
```
Every NOC should maintain subnet documentation:

| Subnet          | VLAN | Description       | Gateway      | DHCP Range        |
|-----------------|------|-------------------|--------------|-------------------|
| 10.10.0.0/23    | 10   | Employee LAN      | 10.10.0.1    | .100-.500         |
| 10.10.2.0/26    | 20   | Server Farm       | 10.10.2.1    | N/A (static)      |
| 10.10.2.64/27   | 30   | Printers          | 10.10.2.65   | .70-.94 (static)  |
| 10.10.2.96/27   | 40   | VoIP              | 10.10.2.97   | .100-.126         |
| 10.10.3.0/24    | 50   | Guest WiFi        | 10.10.3.1    | .50-.250          |
```

### Quick Subnetting Reference

**Common Subnet Masks:**

| CIDR | Subnet Mask       | Hosts | Use Case                  |
|------|-------------------|-------|---------------------------|
| /8   | 255.0.0.0         | 16M   | Massive enterprise        |
| /16  | 255.255.0.0       | 65K   | Large campus              |
| /24  | 255.255.255.0     | 254   | Standard office           |
| /25  | 255.255.255.128   | 126   | Medium department         |
| /26  | 255.255.255.192   | 62    | Small department          |
| /27  | 255.255.255.224   | 30    | Small team                |
| /28  | 255.255.255.240   | 14    | Very small subnet         |
| /29  | 255.255.255.248   | 6     | Tiny network              |
| /30  | 255.255.255.252   | 2     | Point-to-point link       |
| /32  | 255.255.255.255   | 1     | Single host (host route)  |

**Subnetting Cheat Sheet:**

```
Quick calculations:

Host bits = 32 - CIDR
Usable hosts = (2^host_bits) - 2
Block size = 256 - last_octet_of_mask

Example: /26
Host bits = 32 - 26 = 6
Usable = 2^6 - 2 = 62
Block = 256 - 192 = 64
Subnets: .0, .64, .128, .192
```

---

## OSI Model

The OSI (Open Systems Interconnection) Model is a conceptual framework for understanding network communication. It divides networking into 7 layers, each with specific responsibilities. This model is essential for troubleshooting because it allows you to isolate problems to specific layers.

### Why OSI Model Matters for NOC

**Troubleshooting Framework:**
```
User: "The website is down."

NOC approach using OSI:
Layer 7 (Application): Is the web service running?
Layer 6 (Presentation): SSL/TLS certificate valid?
Layer 5 (Session): Session established?
Layer 4 (Transport): TCP connection successful?
Layer 3 (Network): Can we ping the server?
Layer 2 (Data Link): Are frames being sent?
Layer 1 (Physical): Is cable plugged in?

Work bottom-up or top-down to isolate issue efficiently.
```

**Communication:** When reporting issues to vendors/teams, specifying the OSI layer helps:
- "We have a Layer 1 issue" = Physical problem (cable, connector)
- "We have a Layer 3 issue" = Routing problem
- "We have a Layer 7 issue" = Application problem

### OSI Layer Overview

```
7. Application  ← User interfaces with network (HTTP, FTP, DNS)
6. Presentation ← Data formatting, encryption (SSL/TLS, JPEG)
5. Session      ← Connection management (NetBIOS, RPC)
4. Transport    ← Reliable delivery (TCP, UDP)
3. Network      ← Routing, logical addressing (IP, ICMP, routers)
2. Data Link    ← Physical addressing, frame switching (MAC, switches)
1. Physical     ← Bits on wire (cables, hubs, signals)
```

**Mnemonic (Top to Bottom):**
- **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing

**Mnemonic (Bottom to Top):**
- **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way

---

### Layer 1: Physical

**Purpose:** Transmission of raw bits over physical medium.

**Characteristics:**
- Electrical signals (copper), light (fiber), radio waves (wireless)
- Deals with voltages, frequencies, timing
- No addressing, no error checking
- Simply transports 1s and 0s

**Components:**
- **Cables:** Ethernet (Cat5e, Cat6, Cat7), fiber optic (single-mode, multi-mode)
- **Connectors:** RJ45, LC/SC (fiber), BNC (coax)
- **Hubs:** Layer 1 devices (dumb repeaters, flood all ports)
- **Repeaters:** Amplify/regenerate signals over distance
- **Transceivers:** Convert between media types (copper to fiber)
- **Network Interface Cards (NICs):** Physical interface to network

**Cable Types:**

| Type             | Speed        | Distance   | Use Case           |
|------------------|--------------|------------|--------------------|
| Cat5e (copper)   | 1 Gbps       | 100m       | Legacy             |
| Cat6 (copper)    | 1-10 Gbps    | 55-100m    | Standard today     |
| Cat6a (copper)   | 10 Gbps      | 100m       | Enterprise         |
| Single-mode fiber| 100 Gbps+    | 40+ km     | Long-haul          |
| Multi-mode fiber | 100 Gbps     | 500m       | Data center        |

**Binary Transmission:**
```
Bit stream: 1 0 1 1 0 0 0 1

Copper Ethernet:
  1 = +2.5V (or higher voltage)
  0 = -2.5V (or lower voltage)

Fiber optic:
  1 = Light pulse present
  0 = No light pulse

Wireless:
  1 = Specific frequency/amplitude
  0 = Different frequency/amplitude
```

**NOC Troubleshooting - Layer 1:**

**Symptoms:**
- No link lights on NIC or switch port
- "Cable unplugged" error
- Intermittent connectivity (bad cable)

**Diagnostic Steps:**
```
1. Check physical connections:
   - Cable plugged in both ends?
   - Connector damaged?
   - Cable crimped/bent?

2. Check link lights:
   - Green/amber = link established
   - No light = no physical connection
   - Flashing = data transmission

3. Test with known-good cable

4. Check switch port status:
   show interface gi0/1
   Look for: "line protocol down" = Layer 1 issue

5. Cable tester:
   - Continuity test
   - Wire mapping
   - Length measurement
   - Attenuation test

6. Check for interference (wireless):
   - Other WiFi networks
   - Microwave ovens
   - Bluetooth devices
   - Physical obstructions
```

**Common Layer 1 Problems:**
- Damaged cables (bent, cut, chewed by rodents)
- Wrong cable type (crossover vs. straight-through - less common with auto-MDIX)
- Distance limitations exceeded (>100m for copper)
- EMI (Electromagnetic Interference) from power lines, motors
- Bad connectors (oxidation, poor crimping)
- Duplex mismatch (half-duplex vs. full-duplex)

---

### Layer 2: Data Link

**Purpose:** Reliable data transfer across physical link, error detection, frame switching.

**Key Functions:**
1. **Framing:** Package data into frames
2. **Physical Addressing:** MAC addresses
3. **Error Detection:** CRC (Cyclic Redundancy Check)
4. **Flow Control:** Prevent buffer overflow
5. **Media Access Control:** Who can transmit when (CSMA/CD for Ethernet)

**Sub-layers:**
- **MAC (Media Access Control):** Controls hardware addressing and media access
- **LLC (Logical Link Control):** Flow control, error handling

**Frame Structure (Ethernet II):**
```
| Preamble | Dest MAC | Source MAC | Type | Data (Payload) | FCS |
| 7 bytes  | 6 bytes  | 6 bytes    | 2 B  | 46-1500 bytes  | 4 B |

Preamble: Synchronization (10101010... pattern)
Dest MAC: Destination hardware address
Source MAC: Source hardware address
Type: Protocol type (0x0800 = IPv4, 0x0806 = ARP, 0x86DD = IPv6)
Data: Actual payload (IP packet)
FCS: Frame Check Sequence (error detection via CRC-32)
```

**How Layer 2 Works:**

**Scenario:** Computer A sends data to Computer B on same switch

```
1. Computer A receives packet from Layer 3 with Dest IP
2. Computer A checks ARP cache for MAC of destination
3. If no MAC, Computer A sends ARP request (broadcast)
4. Computer B replies with its MAC
5. Computer A creates Ethernet frame:
   - Dest MAC: Computer B's MAC
   - Source MAC: Computer A's MAC
   - Payload: IP packet
   - FCS: Calculated checksum
6. Frame sent to switch
7. Switch checks Dest MAC in frame
8. Switch looks up MAC in CAM table
9. Switch forwards frame to Computer B's port only (unicast)
10. Computer B receives frame, checks FCS
11. If FCS valid → pass to Layer 3
12. If FCS invalid → drop frame (corrupted)
```

**Devices:**
- **Switches:** Learn MAC addresses, forward frames intelligently
- **Bridges:** Connect network segments, filter traffic
- **Network Interface Cards (NICs):** Hardware address resides here

**Protocols:**
- **Ethernet (IEEE 802.3):** Wired LAN standard
- **Wi-Fi (IEEE 802.11):** Wireless LAN standard
- **PPP (Point-to-Point Protocol):** WAN links
- **ARP:** Maps IP to MAC (technically spans Layer 2 and 3)
- **STP (Spanning Tree Protocol):** Prevents loops
- **VLANs (Virtual LANs):** Logical segmentation

**Error Detection - FCS/CRC:**

**How it works:**
```
1. Sender calculates checksum (CRC-32) of frame contents
2. Sender appends checksum to frame (FCS field)
3. Receiver recalculates checksum
4. Receiver compares its calculation to received FCS
5. If match → frame intact, pass to Layer 3
6. If mismatch → frame corrupted, drop it

Note: Layer 2 detects errors but does NOT correct them.
Retransmission is handled by Layer 4 (TCP).
```

**NOC Troubleshooting - Layer 2:**

**Symptoms:**
- Connectivity works, but slow/unreliable
- CRC errors in interface statistics
- Duplicate MAC addresses
- STP topology changes
- MAC flapping

**Diagnostic Steps:**
```
1. Check switch port errors:
   show interface gi0/1
   show interface gi0/1 | include error|CRC|collision
   
   Look for:
   - CRC errors (bad cable, EMI)
   - Collisions (half-duplex or hub)
   - Runts (undersized frames)
   - Giants (oversized frames)

2. Check MAC address table:
   show mac address-table
   show mac address-table interface gi0/1
   
   Look for:
   - Multiple MACs on one port (normal for uplink, bad for access port)
   - Duplicate MACs on different ports (spoofing or VM migration)

3. Check STP status:
   show spanning-tree
   show spanning-tree interface gi0/1
   
   Look for:
   - Frequent topology changes (flapping link)
   - Forwarding/blocking states incorrect

4. Check VLANs:
   show vlan brief
   show interface gi0/1 switchport
   
   Verify device in correct VLAN

5. Monitor for Layer 2 loops:
   show logging | include STP|LOOP

6. Packet capture:
   Use port mirroring + Wireshark
   Look for: excessive broadcasts, malformed frames, ARP storms
```

**Common Layer 2 Problems:**
- MAC address table overflow (CAM table full - potential attack)
- Broadcast storms (no STP, Layer 2 loop)
- VLAN misconfig (device in wrong VLAN)
- Duplex mismatch (one side full, other half)
- Trunk port misconfiguration (allowed VLANs incorrect)

---

### Layer 3: Network

**Purpose:** Routing, logical addressing, path determination between networks.

**Key Functions:**
1. **Logical Addressing:** IP addresses
2. **Routing:** Path selection across multiple networks
3. **Packet Forwarding:** Send packets toward destination
4. **Fragmentation/Reassembly:** Split large packets if needed

**Protocols:**
- **IPv4 / IPv6:** Addressing and packet structure
- **ICMP:** Error reporting, diagnostics (ping, traceroute)
- **OSPF, EIGRP, BGP, RIP:** Routing protocols
- **ARP (spans L2/L3):** Resolves IP to MAC
- **IGMP:** Multicast group management

**Devices:**
- **Routers:** Forward packets between networks
- **Layer 3 Switches:** Switch with routing capability
- **Firewalls:** Filter based on IP addresses/ports

**IP Packet Structure (IPv4):**
```
| Ver | IHL | ToS | Total Length | Identification | Flags | Frag Offset |
| TTL | Protocol | Header Checksum | Source IP | Dest IP | Options | Data |

Key fields:
- TTL (Time To Live): Hop limit (decremented at each router)
- Protocol: Upper layer (6=TCP, 17=UDP, 1=ICMP)
- Source IP: Originating device
- Dest IP: Destination device
```

**Routing Process (Detailed):**

**Scenario:** Packet from 192.168.1.10 to 10.5.5.5

```
Step 1: Source device checks destination IP
  - Is 10.5.5.5 on local subnet (192.168.1.0/24)?
  - No → must send to default gateway

Step 2: Source ARPs for gateway MAC (192.168.1.1)
  - Gets gateway's MAC address

Step 3: Source creates IP packet:
  - Source IP: 192.168.1.10
  - Dest IP: 10.5.5.5
  - TTL: 64

Step 4: Source creates Ethernet frame:
  - Source MAC: Device's MAC
  - Dest MAC: Gateway's MAC (not destination device!)
  - Payload: IP packet

Step 5: Gateway (router) receives frame:
  - Strips Ethernet header (Layer 2)
  - Examines IP packet (Layer 3)
  - Decrements TTL (64 → 63)
  - Checks routing table for 10.5.5.5
  - Finds next hop: 203.0.113.1

Step 6: Gateway creates new Ethernet frame:
  - Source MAC: Gateway's outbound interface MAC
  - Dest MAC: Next hop router's MAC (203.0.113.1)
  - Payload: Same IP packet (IPs unchanged!)

Step 7: Process repeats at each router until destination reached

Key insight: 
  - IP addresses stay the same end-to-end
  - MAC addresses change at every Layer 3 hop
```

**TTL (Time To Live):**

**Purpose:** Prevent routing loops

**How it works:**
```
Packet starts with TTL = 64 (typical)
Each router decrements: 64 → 63 → 62 → 61...
If TTL reaches 0 → router drops packet, sends ICMP "Time Exceeded" to source

Traceroute exploits this:
  - Sends packet with TTL=1 → first router drops, replies
  - Sends packet with TTL=2 → second router drops, replies
  - Continues until destination reached
  - Maps path through network
```

**Routing Protocols (from earlier, reinforced):**

**OSPF (Open Shortest Path First):**
```
Type: Link-state
Metric: Cost (based on bandwidth)
Convergence: Fast
Scalability: Excellent (areas)
Standard: Open (RFC 2328)

Use: Enterprise LANs, data centers
```

**RIP (Routing Information Protocol):**
```
Type: Distance-vector
Metric: Hop count (max 15)
Convergence: Slow
Scalability: Poor
Standard: Open (RFC 2453)

Use: Small networks, legacy
```

**NOC Troubleshooting - Layer 3:**

**Symptoms:**
- Can ping gateway, can't ping Internet
- Can ping by IP, not by hostname (DNS issue, not routing)
- Traceroute stops at specific hop
- Routing protocol adjacencies down

**Diagnostic Steps:**
```
1. Verify IP configuration:
   ipconfig (Windows) / ip addr show (Linux)
   
   Check:
   - Valid IP address?
   - Correct subnet mask?
   - Default gateway set?

2. Test connectivity progressively:
   ping 127.0.0.1 (loopback - tests TCP/IP stack)
   ping [own_IP] (tests NIC)
   ping [gateway_IP] (tests local routing)
   ping [remote_IP] (tests routing beyond gateway)

3. Trace route to destination:
   tracert 8.8.8.8 (Windows)
   traceroute 8.8.8.8 (Linux)
   
   Identifies where packets stop

4. Check routing table:
   route print (Windows)
   ip route show (Linux)
   show ip route (Cisco)
   
   Verify default route exists:
   0.0.0.0/0 or "default" route

5. On router, check routes:
   show ip route
   show ip route [destination_network]
   
   Look for:
   - Missing routes
   - Wrong next hop
   - Routing protocol issues

6. Check routing protocol status:
   show ip ospf neighbor
   show ip eigrp neighbors
   show ip bgp summary

7. Test with different destinations:
   - Some IPs work, others don't → routing issue
   - No IPs work → Layer 1/2 or gateway issue

8. Check for asymmetric routing:
   Packets go out one path, return via different path
   Can cause issues with stateful firewalls
```

**Common Layer 3 Problems:**
- Wrong subnet mask (devices think they're on same subnet when they're not)
- Missing default route
- Routing loops
- ACL blocking traffic
- NAT misconfiguration
- Firewall rules blocking return traffic
- MTU mismatch (fragmentation issues)

---

### Layer 4: Transport

**Purpose:** Reliable end-to-end communication, segmentation, flow control, error recovery.

**Key Functions:**
1. **Segmentation:** Break large messages into segments
2. **Reassembly:** Rebuild messages from segments
3. **Flow Control:** Prevent overwhelming receiver
4. **Error Recovery:** Retransmit lost segments (TCP only)
5. **Multiplexing:** Multiple applications share network (ports)

**Protocols:**
- **TCP (Transmission Control Protocol):** Reliable, connection-oriented
- **UDP (User Datagram Protocol):** Unreliable, connectionless

**Port Numbers:**
- Identify applications on a device
- Source port (random, ephemeral) + Destination port (well-known)
- Range: 0-65535
  - 0-1023: Well-known ports (HTTP=80, HTTPS=443, SSH=22)
  - 1024-49151: Registered ports (applications can request)
  - 49152-65535: Dynamic/ephemeral (random client ports)

#### TCP (Transmission Control Protocol)

**Characteristics:**
- **Connection-oriented:** Establishes connection before data transfer
- **Reliable:** Guarantees delivery (acknowledgments, retransmissions)
- **Ordered:** Segments arrive in order
- **Flow control:** Window size adjustment
- **Error checking:** Checksums

**TCP Header:**
```
| Source Port | Dest Port | Sequence Number | Ack Number |
| Flags (SYN, ACK, FIN, RST) | Window Size | Checksum | Data |

Flags:
- SYN: Synchronize (establish connection)
- ACK: Acknowledge (confirm receipt)
- FIN: Finish (close connection gracefully)
- RST: Reset (abort connection)
- PSH: Push (send data immediately)
- URG: Urgent (prioritize data)
```

**TCP Three-Way Handshake (Connection Establishment):**

```
Client                                Server
  |                                     |
  | SYN (seq=100)                       |
  |------------------------------------>|
  |                                     |
  |           SYN-ACK (seq=300, ack=101)|
  |<------------------------------------|
  |                                     |
  | ACK (seq=101, ack=301)              |
  |------------------------------------>|
  |                                     |
  | Connection Established              |
  | Data transfer can begin             |

Step 1 (SYN): 
  Client → Server: "I want to connect. My sequence starts at 100."
  
Step 2 (SYN-ACK):
  Server → Client: "OK! My sequence starts at 300. I got your 100, expecting 101 next."
  
Step 3 (ACK):
  Client → Server: "Confirmed! I got your 300, expecting 301 next."

Now both sides synchronized and can exchange data.
```

**Why SYN-ACK vs. DHCP DORA?**

These are **different protocols** for **different purposes**:

**TCP SYN-ACK:** Establishes reliable connection for data transfer  
**DHCP DORA:** Obtains IP address configuration

**TCP Connection Termination (Four-Way Handshake):**

```
Client                                Server
  |                                     |
  | FIN (seq=500)                       |
  |------------------------------------>|
  |                                     |
  |                    ACK (ack=501)    |
  |<------------------------------------|
  |                                     |
  |                    FIN (seq=800)    |
  |<------------------------------------|
  |                                     |
  | ACK (ack=801)                       |
  |------------------------------------>|
  |                                     |
  | Connection Closed                   |

Step 1: Client says "I'm done sending data" (FIN)
Step 2: Server acknowledges (ACK)
Step 3: Server says "I'm done too" (FIN)
Step 4: Client acknowledges (ACK)

Both sides cleanly close connection.
```

**TCP Flow Control (Sliding Window):**

```
Purpose: Prevent sender from overwhelming receiver

Receiver advertises "window size" (buffer space available)
Sender cannot send more data than window allows

Example:
  Receiver advertises window = 64KB
  Sender can send up to 64KB before waiting for ACK
  Receiver ACKs first 32KB → window slides forward
  Sender can now send next 32KB
  
If receiver buffer full → window = 0 → sender pauses
When buffer space available → window opens → sender resumes
```

**TCP Retransmission:**

```
Sender sends segments 1, 2, 3, 4, 5
Receiver gets 1, 2, 4, 5 (segment 3 lost)

Receiver ACKs: 1, 2 (but not 3)
Receiver sends duplicate ACK for 2 (still waiting for 3)

After 3 duplicate ACKs OR timeout:
  Sender retransmits segment 3
  
Receiver gets 3 → ACKs through 5
Transmission complete
```

**When to Use TCP:**
- HTTP/HTTPS (web)
- FTP (file transfer)
- SSH (secure shell)
- SMTP (email)
- Any application where data integrity critical

#### UDP (User Datagram Protocol)

**Characteristics:**
- **Connectionless:** No handshake, just send
- **Unreliable:** No guarantees (no ACKs, no retransmission)
- **Unordered:** Segments may arrive out of order
- **No flow control:** Sender sends at will
- **Lightweight:** Minimal overhead

**UDP Header:**
```
| Source Port | Dest Port | Length | Checksum | Data |

Much simpler than TCP!
No sequence numbers, no flags, no connection state
```

**When to Use UDP:**
- **DNS:** Fast queries, can retry if needed
- **DHCP:** Broadcast-based, simple request/response
- **VoIP:** Real-time audio (late packets useless, drop them)
- **Video streaming:** Better to skip lost frames than pause
- **Online gaming:** Low latency critical, some loss acceptable
- **SNMP:** Simple network monitoring

**UDP Advantages:**
- Lower latency (no handshake delay)
- Less overhead (smaller headers)
- Broadcast/multicast support
- Faster for small transactions (DNS query = 1 packet)

**UDP Disadvantages:**
- No reliability (application must handle loss)
- No congestion control (can flood network)
- No ordering (application must reorder)

#### Port Numbers (Critical for NOC)

**Common Well-Known Ports:**

| Port  | Protocol | Service           | Description                     |
|-------|----------|-------------------|---------------------------------|
| 20/21 | TCP      | FTP               | File transfer (20=data, 21=control) |
| 22    | TCP      | SSH               | Secure shell                    |
| 23    | TCP      | Telnet            | Insecure remote access          |
| 25    | TCP      | SMTP              | Email sending                   |
| 53    | TCP/UDP  | DNS               | Domain name resolution          |
| 67/68 | UDP      | DHCP              | IP address assignment           |
| 80    | TCP      | HTTP              | Web traffic (unencrypted)       |
| 110   | TCP      | POP3              | Email retrieval                 |
| 123   | UDP      | NTP               | Time synchronization            |
| 143   | TCP      | IMAP              | Email retrieval (better than POP3) |
| 161/162 | UDP    | SNMP              | Network monitoring              |
| 443   | TCP      | HTTPS             | Web traffic (encrypted)         |
| 445   | TCP      | SMB               | Windows file sharing            |
| 3389  | TCP      | RDP               | Remote Desktop Protocol         |
| 3306  | TCP      | MySQL             | Database                        |
| 5432  | TCP      | PostgreSQL        | Database                        |
| 8080  | TCP      | HTTP-Alt          | Alternative web (proxies)       |

**NOC Troubleshooting - Layer 4:**

**Symptoms:**
- Connection timeouts
- Slow performance (TCP retransmissions)
- Application unreachable but ping works
- Firewall blocking specific services

**Diagnostic Steps:**
```
1. Test port connectivity:
   telnet [IP] [port]
   nc -zv [IP] [port] (Linux - netcat)
   Test-NetConnection -ComputerName [IP] -Port [port] (PowerShell)
   
   Example:
   telnet 192.168.1.100 80
   If connects → port open
   If times out → port blocked/closed

2. Check listening ports:
   netstat -an (Windows/Linux)
   ss -tuln (Linux - modern)
   
   Look for:
   - LISTENING state = server accepting connections
   - ESTABLISHED = active connection
   - TIME_WAIT = connection closing

3. Packet capture:
   Wireshark filter: tcp.port == 80
   
   Look for:
   - SYN sent, no SYN-ACK = port blocked/server down
   - SYN-ACK received, no ACK sent = client issue
   - Retransmissions = packet loss
   - RST packets = connection rejected

4. Check firewall rules:
   Windows Firewall: netsh advfirewall show allprofiles
   Linux (iptables): iptables -L -v
   Linux (firewalld): firewall-cmd --list-all
   
   Verify port allowed inbound/outbound

5. Check service status:
   Windows: services.msc
   Linux: systemctl status [service]
   
   Verify application running and listening on correct port

6. Check for port conflicts:
   netstat -anb (Windows - shows process)
   lsof -i :[port] (Linux - shows process using port)
   
   Example: Two services trying to use port 80

7. TCP performance analysis:
   Look for:
   - High retransmission rate (packet loss)
   - Window size too small (throttling)
   - Latency (RTT) too high
   - Duplicate ACKs (out-of-order segments)
```

**Common Layer 4 Problems:**
- Firewall blocking ports
- Service not listening on expected port
- Port conflicts (two apps on same port)
- MTU issues (fragmentation, black hole routers)
- TCP window scaling disabled (limits throughput)
- Asymmetric routing breaking TCP state

---

### Layer 5: Session

**Purpose:** Establish, maintain, and terminate sessions between applications.

**Key Functions:**
1. **Session Establishment:** Authenticate, negotiate parameters
2. **Session Maintenance:** Keep connection alive, manage dialog
3. **Session Termination:** Graceful close, release resources
4. **Checkpointing:** Save state during long transfers (resume if interrupted)
5. **Synchronization:** Coordinate communication

**Characteristics:**
- Sessions are **unique** - data cannot cross between sessions
- Manages **dialog control** (half-duplex vs. full-duplex)
- Handles **token management** (who can transmit when)

**Protocols/APIs:**
- **NetBIOS:** Windows network sessions
- **RPC (Remote Procedure Call):** Client-server communication
- **SQL sessions:** Database connections
- **TLS/SSL handshake:** Secure session setup (often considered Layer 6)

**Session vs. Connection:**
- **TCP connection (Layer 4):** Transport-level pipe
- **Session (Layer 5):** Application-level conversation

**Example:**
```
Web browser opens TCP connection to server (Layer 4)
HTTP session begins (Layer 5)
  - Sends cookies for session tracking
  - Maintains login state
  - Exchanges multiple requests/responses
HTTP session ends (logout or timeout)
TCP connection closes (Layer 4)
```

**Session Management:**

**Authentication:**
```
User logs into web application:
1. User sends credentials
2. Server validates
3. Server creates session ID
4. Server sends session ID to client (cookie)
5. Client includes session ID in subsequent requests
6. Server maintains session state (shopping cart, preferences)
7. Session expires after timeout or explicit logout
```

**Checkpointing (from TryHackMe):**
```
Large file transfer in progress:
- Session layer saves progress periodically
- If connection lost, can resume from last checkpoint
- Prevents restarting from beginning

Example: FTP resume, rsync, BitTorrent
```

**NOC Relevance:**
- Less commonly troubleshot directly (APIs abstract this)
- Session timeouts can cause application issues
- Monitor session counts (database connections, concurrent logins)

---

### Layer 6: Presentation

**Purpose:** Data formatting, encryption, compression, translation.

**Key Functions:**
1. **Data Translation:** Convert between application and network formats
2. **Encryption/Decryption:** Secure data (SSL/TLS)
3. **Compression/Decompression:** Reduce bandwidth usage
4. **Character Encoding:** ASCII, Unicode, EBCDIC conversions

**Protocols/Standards:**
- **SSL/TLS:** Encryption (HTTPS)
- **JPEG, GIF, PNG:** Image formats
- **MPEG, MP4:** Video formats
- **ASCII, Unicode, UTF-8:** Character encoding

**Data Representation:**

**Example: Sending Email with Attachment**
```
Application Layer (Layer 7):
  - User writes email: "Hello!"
  - Attaches image: photo.jpg

Presentation Layer (Layer 6):
  - Converts email to MIME format
  - Encodes image as Base64 (for text-only email protocol)
  - Compresses if enabled
  - Encrypts if using TLS

Transport Layer (Layer 4):
  - Segments data
  - Adds TCP header

...continues down stack
```

**Encryption (TLS Handshake):**
```
Client                           Server
  |                                |
  | ClientHello                    |
  |----- (Supported ciphers) ----->|
  |                                |
  |                  ServerHello   |
  |<-- (Selected cipher, cert) ----|
  |                                |
  | Key Exchange                   |
  |------------------------------->|
  |                                |
  | ChangeCipherSpec               |
  |------------------------------->|
  |                                |
  |               ChangeCipherSpec |
  |<-------------------------------|
  |                                |
  | Encrypted Application Data     |
  |<------------------------------>|

Now all data encrypted (HTTPS, FTPS, etc.)
```

**Character Encoding Issues:**
```
Problem: Email shows "Â" instead of apostrophe

Cause: Character encoding mismatch
  - Sender: UTF-8 encoding
  - Receiver: ASCII interpretation

Solution: Ensure consistent encoding (UTF-8 standard today)
```

**NOC Relevance:**
- SSL/TLS certificate issues (expired, invalid, self-signed)
- Encryption troubleshooting (cipher mismatch, version incompatibility)
- Compression issues (file corruption)
- Character encoding problems (internationalization)

**Troubleshooting Presentation Layer:**
```
1. Certificate issues:
   openssl s_client -connect example.com:443
   
   Check:
   - Certificate valid?
   - Certificate matches domain?
   - Certificate chain complete?
   - Certificate not expired?

2. Cipher negotiation:
   nmap --script ssl-enum-ciphers -p 443 example.com
   
   Identifies supported ciphers, weak encryption

3. Encoding issues:
   file [filename] (Linux - detects file type/encoding)
   
   Verify file format matches expectation
```

---

### Layer 7: Application

**Purpose:** User interfaces, application services, network process to application.

**Key Functions:**
1. **User Interface:** What users interact with
2. **Application Services:** Email, file transfer, web browsing
3. **Network Services:** DNS, DHCP, FTP, HTTP

**Characteristics:**
- Closest to end user
- Provides protocols applications use
- Includes GUI applications (browsers, email clients)

**Protocols:**
- **HTTP/HTTPS:** Web
- **FTP/SFTP:** File transfer
- **SMTP/IMAP/POP3:** Email
- **DNS:** Name resolution
- **SSH:** Secure remote access
- **Telnet:** Insecure remote access
- **SNMP:** Network management
- **DHCP:** IP assignment

**DNS (Domain Name System) - Critical for NOC:**

**Purpose:** Translate domain names to IP addresses

**DNS Query Process:**
```
User types: www.example.com

1. Browser checks local cache
   If cached → done
   
2. OS checks local DNS cache
   If cached → done
   
3. Query recursive DNS server (ISP or 8.8.8.8)
   
4. Recursive server checks its cache
   If cached → return to client
   
5. If not cached, recursive server queries:
   a. Root DNS server → "Ask .com server"
   b. .com DNS server → "Ask example.com's authoritative server"
   c. example.com DNS server → "www.example.com = 93.184.216.34"
   
6. Recursive server caches response
7. Returns IP to client
8. Client caches response (TTL: 300 seconds, etc.)
9. Browser connects to 93.184.216.34
```

**DNS Record Types:**

| Type  | Purpose                    | Example                          |
|-------|----------------------------|----------------------------------|
| A     | IPv4 address               | example.com → 93.184.216.34      |
| AAAA  | IPv6 address               | example.com → 2606:2800:220:1... |
| CNAME | Alias (canonical name)     | www → example.com                |
| MX    | Mail server                | mail.example.com (priority 10)   |
| NS    | Name server                | ns1.example.com                  |
| TXT   | Text records               | SPF, DKIM, verification          |
| PTR   | Reverse DNS (IP → name)    | 34.216.184.93.in-addr.arpa       |

**HTTP/HTTPS (Web Traffic):**

**HTTP Request:**
```
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
Connection: keep-alive

(Blank line indicates end of headers)
```

**HTTP Response:**
```
HTTP/1.1 200 OK
Date: Fri, 20 Dec 2024 12:00:00 GMT
Server: Apache/2.4.41
Content-Type: text/html
Content-Length: 1234

<!DOCTYPE html>
<html>
<head><title>Example</title></head>
...
</html>
```

**HTTP Status Codes:**

| Code | Meaning              | Description                          |
|------|----------------------|--------------------------------------|
| 200  | OK                   | Success                              |
| 301  | Moved Permanently    | Redirect (old → new URL)             |
| 302  | Found (Temp Redirect)| Temporary redirect                   |
| 400  | Bad Request          | Client error (malformed request)     |
| 401  | Unauthorized         | Authentication required              |
| 403  | Forbidden            | Access denied                        |
| 404  | Not Found            | Resource doesn't exist               |
| 500  | Internal Server Error| Server-side problem                  |
| 502  | Bad Gateway          | Proxy/gateway error                  |
| 503  | Service Unavailable  | Server overloaded/down               |

**NOC Troubleshooting - Layer 7:**

**Symptoms:**
- Specific application doesn't work (others do)
- DNS resolution fails
- Web page errors (404, 500, etc.)
- Email not sending/receiving
- Slow application performance

**Diagnostic Steps:**
```
1. Test DNS resolution:
   nslookup example.com
   dig example.com (Linux - more detailed)
   
   Check:
   - Does domain resolve?
   - Correct IP returned?
   - Try different DNS server (8.8.8.8)

2. Test HTTP/HTTPS:
   curl -I http://example.com (headers only)
   curl -v https://example.com (verbose)
   wget http://example.com
   
   Check:
   - HTTP status code
   - Response time
   - Certificate validity (HTTPS)

3. Test specific application protocol:
   telnet mail.example.com 25 (SMTP)
   telnet mail.example.com 110 (POP3)
   telnet mail.example.com 143 (IMAP)
   
   Manually send protocol commands to verify server

4. Check application logs:
   - Web server: /var/log/apache2/error.log
   - Mail server: /var/log/mail.log
   - Application: varies by app

5. Packet capture at application layer:
   Wireshark filter: http or dns or ftp
   
   Examine:
   - Request/response format
   - Error messages
   - Response times

6. Test from different locations:
   - Same result everywhere → application issue
   - Different results → network path issue

7. Check application resources:
   - CPU usage
   - Memory usage
   - Disk space
   - Database connections
   
   Resource exhaustion causes Layer 7 failures
```

**Common Layer 7 Problems:**
- DNS misconfiguration (wrong IP, missing records)
- Web application errors (code bugs, database issues)
- Certificate expired/invalid (HTTPS)
- Firewall blocking application protocol
- Application server down/crashed
- Database connection pool exhausted
- Authentication failures

---

### OSI Model Summary Table

| Layer | Name         | PDU*    | Addressing    | Devices              | Protocols              | Troubleshooting      |
|-------|--------------|---------|---------------|----------------------|------------------------|----------------------|
| 7     | Application  | Data    | N/A           | Proxy, L7 firewall   | HTTP, FTP, DNS, SMTP   | App logs, curl, nslookup |
| 6     | Presentation | Data    | N/A           | Gateway              | SSL/TLS, JPEG, MPEG    | Certificate check    |
| 5     | Session      | Data    | N/A           | Gateway              | NetBIOS, RPC, SQL      | Session timeout      |
| 4     | Transport    | Segment | Port numbers  | L4 firewall          | TCP, UDP               | Telnet, netstat      |
| 3     | Network      | Packet  | IP addresses  | Router, L3 switch    | IP, ICMP, OSPF, BGP    | Ping, traceroute     |
| 2     | Data Link    | Frame   | MAC addresses | Switch, bridge       | Ethernet, ARP, STP     | show mac, port errors|
| 1     | Physical     | Bits    | N/A           | Hub, cable, NIC      | N/A (electrical/light) | Cable test, link lights |

*PDU = Protocol Data Unit (name of data at each layer)

### Encapsulation Process

**Data Flow Down the Stack (Sending):**

```
Application Layer (7): User sends email
  ↓ [Email content]

Presentation Layer (6): Format, encrypt
  ↓ [Formatted, encrypted email]

Session Layer (5): Establish session
  ↓ [Session info + email]

Transport Layer (4): Segment, add TCP header
  ↓ [TCP segment: Header + Data]

Network Layer (3): Add IP header
  ↓ [IP packet: IP Header + TCP segment]

Data Link Layer (2): Add Ethernet header & trailer
  ↓ [Ethernet frame: Header + IP packet + FCS]

Physical Layer (1): Convert to bits, transmit
  ↓ [Electrical signals on wire: 10110011...]
```

**Data Flow Up the Stack (Receiving):**

```
Physical Layer (1): Receive bits, convert to frame
  ↓

Data Link Layer (2): Check FCS, strip Ethernet header
  ↓ [If FCS valid, pass IP packet to Layer 3]

Network Layer (3): Check destination IP, strip IP header
  ↓ [If IP matches, pass TCP segment to Layer 4]

Transport Layer (4): Check port, reassemble segments
  ↓ [Pass complete data to Layer 5]

Session Layer (5): Manage session
  ↓

Presentation Layer (6): Decrypt, format
  ↓

Application Layer (7): Deliver to email app
  ↓ [User sees email]
```

**Key Principle:** Each layer adds its header (encapsulation going down), removes it (decapsulation going up).

---

## NOC Applications & Troubleshooting

### Systematic Troubleshooting Approach

**Top-Down (Application to Physical):**
- Start at Layer 7, work down to Layer 1
- Use when: Application-specific problem
- Example: "Website not loading" → Check DNS → Check HTTP → Check TCP → Check routing → Check switching → Check cable

**Bottom-Up (Physical to Application):**
- Start at Layer 1, work up to Layer 7
- Use when: Total connectivity failure
- Example: "Nothing works" → Check cable → Check switch → Check gateway → Check routing → Check firewall → Check application

**Divide-and-Conquer:**
- Start at Layer 3 (ping) to quickly identify L1/L2 vs. L3+ issues
- If ping works → problem is L4-L7
- If ping fails → problem is L1-L3

**OSI-Based Ticket Documentation:**

```
Ticket #12345: Email server unreachable

Issue: Users cannot send email (SMTP)

Troubleshooting performed:
[L1] Physical: Link lights green on server NIC ✓
[L2] Data Link: Switch port shows no errors ✓
     MAC address in table: show mac address-table | include [server_MAC] ✓
[L3] Network: Ping 192.168.10.50 successful ✓
     Traceroute reaches destination ✓
[L4] Transport: Telnet 192.168.10.50 25 - CONNECTION REFUSED ✗

Root cause: SMTP service not running on server (Layer 7)

Resolution: Restarted Postfix service
  systemctl start postfix
  systemctl status postfix - now active ✓
  
Verification: Telnet 192.168.10.50 25 - connected ✓
  220 mail.example.com ESMTP Postfix

Status: RESOLVED
```

### Critical NOC Commands by OSI Layer

**Layer 1 (Physical):**
```bash
# Check interface status
show interface gi0/1 (Cisco)
ethtool eth0 (Linux)

# Check cable
# Physical cable tester required

# Check link lights
# Visual inspection
```

**Layer 2 (Data Link):**
```bash
# View MAC table
show mac address-table (Cisco)
brctl showmacs br0 (Linux bridge)

# View interface errors
show interface gi0/1 | include error
ip -s link show eth0 (Linux)

# View VLANs
show vlan brief (Cisco)

# View ARP cache
arp -a (Windows/Linux)
show ip arp (Cisco)
```

**Layer 3 (Network):**
```bash
# Test connectivity
ping [IP]
traceroute [IP]

# View routing table
show ip route (Cisco)
ip route show (Linux)
route print (Windows)

# View IP config
ipconfig (Windows)
ip addr show (Linux)
show ip interface brief (Cisco)
```

**Layer 4 (Transport):**
```bash
# Test port connectivity
telnet [IP] [port]
nc -zv [IP] [port] (Linux)
Test-NetConnection -ComputerName [IP] -Port [port] (PowerShell)

# View connections
netstat -an
ss -tuln (Linux)

# View listening ports
netstat -anp | grep LISTEN
lsof -i :[port]
```

**Layer 7 (Application):**
```bash
# Test DNS
nslookup [domain]
dig [domain]

# Test HTTP
curl -I http://[domain]
wget http://[domain]

# Test SMTP
telnet mail.example.com 25

# View application status
systemctl status [service] (Linux)
services.msc (Windows)
```

---

## Key Takeaways for NOC Career

**1. Networking Fundamentals:**
- Understand both logical (IP) and physical (MAC) addressing
- Know when to use static vs. DHCP addressing
- Recognize public vs. private IP ranges
- Understand NAT operation

**2. Protocols:**
- ICMP for diagnostics (ping, traceroute)
- ARP for IP-to-MAC resolution
- DHCP for automated IP assignment
- TCP for reliable, UDP for fast/real-time
- DNS for name resolution

**3. Topologies:**
- Star (most common, central switch)
- Understand single points of failure
- Design for redundancy in production

**4. Devices:**
- Switches operate at Layer 2 (MAC forwarding)
- Routers operate at Layer 3 (IP routing)
- Know when packets cross Layer 3 boundaries

**5. Subnetting:**
- Calculate network/broadcast addresses
- Understand CIDR notation
- Size subnets appropriately for needs
- Document subnet allocations

**6. OSI Model:**
- Use as troubleshooting framework
- Isolate issues to specific layers
- Communicate problems clearly using layer terminology

**7. Tools:**
- Master ping, traceroute, nslookup/dig
- Understand netstat/ss for connection monitoring
- Use telnet/nc for port testing
- Learn Wireshark for packet analysis
- Know show commands for network devices

**8. Documentation:**
- Maintain accurate network diagrams
- Document IP allocations and subnets
- Log troubleshooting steps
- Create runbooks for common issues

**Next Steps:**
- Practice subnetting calculations
- Lab with GNS3 (build topologies, configure routing)
- Study Wireshark packet captures
- Learn vendor-specific commands (Cisco, Juniper)
- Understand monitoring tools (SNMP, syslog, NetFlow)

---

## Glossary

**ARP (Address Resolution Protocol):** Maps IP addresses to MAC addresses on local networks.

**Broadcast:** Transmission to all devices on a network segment (MAC: FF:FF:FF:FF:FF:FF, IP: x.x.x.255).

**CIDR (Classless Inter-Domain Routing):** IP addressing method using prefix length (/24, /26, etc.).

**Default Gateway:** Router interface that devices use to reach external networks.

**DHCP (Dynamic Host Configuration Protocol):** Automatically assigns IP configuration to devices.

**DNS (Domain Name System):** Translates domain names to IP addresses.

**Encapsulation:** Adding headers/trailers to data as it moves down OSI layers.

**Frame:** Layer 2 PDU (Ethernet frame with MAC addresses).

**ICMP (Internet Control Message Protocol):** Network diagnostics (ping, traceroute).

**IP Address:** Logical Layer 3 address for network communication.

**MAC Address:** Physical Layer 2 address burned into NICs.

**NAT (Network Address Translation):** Maps private IPs to public IPs.

**Packet:** Layer 3 PDU (IP packet with source/destination IPs).

**Port:** Layer 4 identifier for applications (0-65535).

**Router:** Layer 3 device that forwards packets between networks.

**Segment:** Layer 4 PDU (TCP segment or UDP datagram).

**Subnet Mask:** Defines network vs. host portion of IP address.

**Switch:** Layer 2 device that forwards frames based on MAC addresses.

**TCP (Transmission Control Protocol):** Reliable, connection-oriented Layer 4 protocol.

**TTL (Time To Live):** Hop limit for packets, prevents routing loops.

**UDP (User Datagram Protocol):** Unreliable, connectionless Layer 4 protocol.

**VLAN (Virtual LAN):** Logical segmentation of Layer 2 network.

---

**End of Day Study Notes**

Total Topics Covered: 3 TryHackMe Rooms  
Total Study Time: [Your time]  
Next Session: Packets & Frames, Extending Your Network, GNS3 Lab

---

*These notes created for NOC career preparation - comprehensive, accurate, and ready for real-world application.*