→ Public subnet

If not:
→ Private subnet

---

## 8. Route Tables

Route tables determine how traffic leaves a subnet.

Each route includes:
- Destination (e.g., 0.0.0.0/0)
- Target (IGW, NAT, VGW, etc.)

Every subnet must be associated with a route table.

---

## 9. Internet Gateway (IGW)

- Enables internet communication
- Attached to a VPC (not to a subnet)
- Subnets gain internet access via route table pointing to IGW

---

## 10. NAT Gateway

- Placed in a public subnet
- Allows private subnet instances to access the internet outbound
- Blocks inbound internet traffic

Use case:
Private EC2 instances needing OS updates or external API calls.

---

## 11. Public IP vs Elastic IP

### Public IP
- Automatically assigned
- Changes if instance stops/starts

### Elastic IP (EIP)
- Static IPv4 address
- Manually allocated
- Persists across instance restarts
- Useful for production services

---

## 12. Security Groups vs Network ACLs

### Security Groups
- Stateful
- Applied at instance level
- Default:
  - Deny inbound
  - Allow outbound
- No explicit deny rules

### Network ACLs
- Stateless
- Applied at subnet level
- Allow AND deny rules
- Evaluated in order

| Feature | Security Group | Network ACL |
|----------|---------------|-------------|
| Scope | Instance | Subnet |
| Stateful | Yes | No |
| Explicit Deny | No | Yes |

---

## 13. Packet Flow Understanding

Instance A → Instance B (different subnet)

1. Outbound Security Group of A
2. Outbound NACL of Subnet A
3. Inbound NACL of Subnet B
4. Inbound Security Group of B

Return traffic:
- Security Groups allow automatically (stateful)
- NACLs re-evaluate every time (stateless)

---

## 14. Hybrid Connectivity

### Site-to-Site VPN
- IPSec encrypted tunnel
- Uses Virtual Private Gateway
- Cost-effective
- Runs over public internet

### Client VPN
- Managed VPN for remote users
- Advanced authentication
- Elastic scaling

### Direct Connect
- Dedicated physical connection
- Higher bandwidth
- Lower latency
- More consistent performance
- Expensive

Common pattern:
Direct Connect + VPN failover.

---

## 15. Amazon Route 53 (DNS)

DNS translates domain names into IP addresses.

Routing policies:
- Latency-based
- Geolocation
- Weighted
- Failover
- Health check-based

---

## 16. DNS Resolution Flow

1. Browser cache
2. OS cache
3. Recursive resolver (ISP DNS)
4. Root server
5. TLD server (.com, .org, etc.)
6. Authoritative server

DNS changes:
- Made at authoritative server
- Propagate based on TTL (Time To Live)
- Temporary overlap possible due to caching

Both:
- Browser
- Recursive resolver

Maintain DNS caches.

---

## 17. Amazon CloudFront

- Content Delivery Network (CDN)
- Uses edge locations
- Caches content closer to users
- Improves latency
- Reduces origin load

---

## 18. AWS Global Accelerator

- Uses static Anycast IPs
- Routes via AWS global backbone
- Improves performance
- Fast failover

Route 53 = DNS-level routing  
Global Accelerator = Network-layer routing  

---

## 19. PrivateLink

Allows:
- Private connection from VPC to AWS service
- Traffic stays on AWS network
- No internet exposure
- No public IP required

Important understanding:
PrivateLink allows secure, private access to services like S3 without traversing the public internet.

---

## 20. Storage & Database Placement

### EBS
- Block storage
- Attached to EC2
- Lives in one AZ

### EFS
- Shared file storage
- Can span multiple AZs

### S3
- Object storage
- Regional service
- Not deployed in your subnet

### RDS
- Managed database
- Handles compute + storage
- Storage managed by AWS
- Typically deployed in private subnets

Important clarification:
Database services like RDS handle both the database engine and the underlying storage layer.

---

## 21. Three-Tier Architecture Overview

User  
↓  
Route 53  
↓  
CloudFront  
↓  
Load Balancer  
↓  
Public Subnet (ALB)  
↓  
Private Subnet (App servers)  
↓  
Private Subnet (RDS)

---

# Summary of Modules 4 & 5

You now understand:

- AWS global infrastructure
- High availability strategies
- VPC architecture
- Subnet segmentation
- Route logic
- Internet access control
- Security enforcement layers
- Hybrid connectivity options
- DNS resolution mechanics
- Edge networking services
- PrivateLink use case
- Storage architecture fundamentals

This is foundational cloud architecture knowledge.