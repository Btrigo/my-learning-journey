# TryHackMe – Extending Your Network

## Overview

The **Extending Your Network** room on TryHackMe builds on core networking fundamentals by introducing the technologies that allow networks to grow beyond a single local environment and communicate securely over the Internet. The room focuses on how traffic is routed between networks, how access is controlled, and how private networks can be securely extended.

The key technologies explored include **routers**, **switches**, **port forwarding**, **firewalls**, and **Virtual Private Networks (VPNs)**. These concepts are foundational for understanding enterprise networks, cloud networking, and modern security architectures.

---

## Core Networking Devices

### Routers

A **router** is a Layer 3 (Network Layer) device responsible for connecting **different networks** and forwarding data between them using IP addressing.

Routing is the process of determining the most appropriate path for data to travel across multiple networks. Routers make forwarding decisions based on factors such as:

- Shortest available path
- Reliability of the path
- Speed and type of the transmission medium

Routers often provide administrative interfaces that allow configuration of additional network controls, including **port forwarding**, **firewall rules**, and **VPN connections**.

Routers do not connect individual devices directly; instead, they connect entire networks together.

---

### Switches

A **switch** is a device used to connect multiple devices within the **same network**.

#### Layer 2 Switches

Layer 2 switches operate at the Data Link layer and forward **frames** using **MAC addresses**. Their responsibility is to ensure frames are delivered to the correct device on a local network.

Layer 2 switches do not perform routing and cannot forward traffic between different IP networks.

#### Layer 3 Switches

Layer 3 switches combine the functionality of a switch and a router. They:

- Forward frames within a network (Layer 2)
- Route packets between networks or VLANs using IP addresses (Layer 3)

Layer 3 switches are commonly used for **internal network segmentation** and inter-VLAN routing.

---

## Network Segmentation with VLANs

A **Virtual Local Area Network (VLAN)** allows a single physical switch to be logically divided into multiple isolated networks.

Using VLANs:
- Devices can share the same physical infrastructure
- Traffic between groups can be restricted by policy
- Network segmentation improves both performance and security

In practice, VLANs allow departments (such as Sales and Accounting) to access shared resources like the Internet while remaining isolated from each other unless explicitly permitted.

---

## Port Forwarding

**Port forwarding** is a technique that allows services hosted on a private network to be accessed from an external network, such as the Internet.

By default, devices with private IP addresses are not reachable from outside their local network. Port forwarding solves this by configuring a router to:

- Listen on a specific port on its **public IP address**
- Forward incoming traffic on that port to a specific internal IP address and port

Port forwarding determines **where traffic is sent**, not whether it is allowed. Even if a port is forwarded, firewall rules may still block the traffic.

Port forwarding is commonly used to expose services such as web servers, game servers, or remote administration tools.

---

## Firewalls

A **firewall** is a device or software component that controls whether network traffic is allowed to enter or exit a network.

Firewalls evaluate traffic based on attributes such as:
- Source address
- Destination address
- Port number
- Protocol (TCP, UDP, etc.)

### Stateful Firewalls

Stateful firewalls track the **state of active connections** and make decisions based on the full context of a communication session.

Characteristics:
- Understand TCP handshakes and session state
- Automatically allow return traffic for established connections
- Consume more system resources

If a connection is determined to be malicious, a stateful firewall can block all traffic associated with that connection or device.

### Stateless Firewalls

Stateless firewalls inspect packets **individually** using static rules.

Characteristics:
- No awareness of connection state
- Lower resource usage
- Effectiveness depends entirely on rule accuracy

Stateless firewalls are well-suited for handling large volumes of traffic and are commonly used in DDoS mitigation scenarios.

---

## Virtual Private Networks (VPNs)

A **Virtual Private Network (VPN)** allows devices on separate networks to communicate securely by creating an **encrypted tunnel** over the Internet.

Devices connected through a VPN form a **logical private network**, even though the underlying infrastructure is public.

### VPN Benefits

- Securely connects networks in different geographical locations
- Protects data confidentiality through encryption
- Allows private resources to remain inaccessible from the public Internet

TryHackMe uses a VPN to allow users to interact with vulnerable machines without exposing those machines directly to the Internet.

### VPN Technologies

- **PPP (Point-to-Point Protocol):** Handles authentication and encryption but is not routable on its own
- **PPTP:** Easy to deploy but uses weak encryption and is considered insecure
- **IPsec:** Provides strong encryption and is widely used in enterprise and cloud environments

---

## Practical Network Simulation

The practical exercise in this room demonstrates how a TCP packet travels from one device to another across multiple networks.

In the simulation:
- Devices on different local networks communicate through a router
- Routing decisions determine whether traffic is sent locally or to the default gateway
- ARP is used to resolve IP addresses to MAC addresses at each hop
- A full TCP three-way handshake occurs before data is transmitted

This exercise reinforces how multiple OSI layers work together:
- Layer 4 establishes reliable communication
- Layer 3 determines routing between networks
- Layer 2 ensures local frame delivery

---

## Key Takeaways

- Routers connect networks; switches connect devices
- Routing decisions are based on IP addressing and network topology
- VLANs provide logical network segmentation on shared infrastructure
- Port forwarding exposes internal services through a public interface
- Firewalls determine whether traffic is permitted
- VPNs securely extend private networks over public infrastructure
- Real network communication relies on coordination across multiple OSI layers
