# Brando's Learning Journey
**Cloud Engineer in Training | Networking & Security Foundation**

> ***"Life happens for us, not to us. Every challenge is a chance to learn, adapt, and improve."***

---

## Who I Am

I'm Brandon Trigo — someone who genuinely loves how infrastructure works.

Not just at the surface level. I mean the fact that there are fiber cables running across the floor of the ocean carrying electrical signals that get translated into readable information in milliseconds. The fact that when you load a webpage, you're probably not even talking to the origin server — you're hitting a CDN edge node somewhere close to you. The fact that you can define an entire network topology in code and a cloud provider will go build it for you.

That stuff fascinates me. It always has.

My background is physical — I've racked servers, terminated fiber, managed structured cabling, and handled remote hands operations in a live colocation environment. I understand infrastructure from the ground up, literally. Now I'm taking that foundation and building upward into cloud architecture, network engineering, and security.

This repository is my public proof of work. Every day I'm learning something. Most of it ends up here.

---

## 🎯 Target Role

**Cloud Engineer** — with a networking focus and security foundation.

I want to build and manage cloud environments that are well-architected, properly networked, and defensible. Not just keeping the lights on — understanding *why* the lights are on and making sure they stay that way.

---

## 🏗️ Where I'm At

### Certifications
- ✅ **CompTIA Security+** (SY0-701) - August 2025
- ✅ **AWS Certified Cloud Practitioner** (CLF-C02) — April 2026
- ✅ Cybersecurity Bootcamp — Adelphi University / StackRoute
- ✅ Associate's Degree — Nassau Community College | 4.0 GPA | Summa Cum Laude

### Active focus
- 🔄 **AWS Solutions Architect Associate** (SAA-C03)
- 🔄 **Building a production-grade, multi-tier cloud environment on AWS** — provisioned in Terraform, deployed through CI/CD, secured and monitored
        - Multi-tier architecture (load balancer → compute → database) across a custom VPC
        - CI/CD automation via GitHub Actions
        - Security hardening and least-privilege access
        - Monitoring and observability
        - Containers and orchestration (Docker, Kubernetes)
        - Multi-account AWS setup
        - Python/Boto3 automation
- 🔄 **Networking fundamentals** — Ongoing. Cisco packet tracer labs, hands-on routing and switching, constantly keeping myself sharp. 
- 🔄 **TryHackMe** - Occasional. Used when needed. 

---

## ✅ Completed Projects

- **[Static Portfolio Site — Secure AWS Deployment](projects/AWS/deploy_static_portfolio_S3_CloudFront.md)** — Full console build: S3 (private) + CloudFront + OAC + ACM + Route 53 custom domain. This is what currently serves the live site.
- **[Static Portfolio Site — Terraform IaC (v1)](projects/AWS/01-terraform-static-portfolio)** — Same core architecture (S3, CloudFront, OAC) rebuilt as code, single `main.tf`
- **[Static Portfolio Site — Terraform IaC Rebuild (v2)](projects/AWS/02-terraform-static-portfolio-rebuild)** — Refactored into 5 separated files with inline documentation and `force_destroy` handling; full `init → fmt → validate → plan → apply → destroy` lifecycle

*Note: the Terraform builds intentionally use the default `*.cloudfront.net` endpoint rather than the live custom domain, to practice the full IaC lifecycle (including destroy) without risking the production site. The custom domain (ACM + Route 53) remains console-managed for now.*

*(This site — [brandontrigo.com](https://brandontrigo.com) — currently runs on the console-built infrastructure above.)*

## 🛠️ Technical Background

**H5 Data Centers — Remote Hands Technician**
Real production environment. SLA-driven ticket resolution, hardware installs, structured cabling, physical security, SolarWinds monitoring. This is where I learned that infrastructure is unforgiving and documentation matters.

**SSRD Cybersecurity Internship — CTF Developer**
Built 12+ capture the flag challenges targeting real-world vulnerabilities — XSS, SQL injection, RCE, privilege escalation. Deployed via Docker. Used Git for version control throughout.

**Networking & Systems Fundamentals**
Solid grounding in networking — OSI Layers 1–4, routing/switching, troubleshooting — built through CCNA-aligned coursework and hands-on labs. Working familiarity with Windows Server, Active Directory, and Group Policy from self-study; comfortable navigating both Windows and Linux environments.

---

## 💡 Philosophy & Approach

> ***"Grit (n.) — the drive, stamina, and fortitude to push through any challenge or obstacle until success is achieved."***


---

## 📁 What's In This Repo

**[daily-logs/](daily_logs/)** — My daily study journal. Raw and consistent.

**[personal_notes/](personal_notes/)** — Technical notes organized by domain. AWS, networking, security, Linux.

**[projects/](projects/)** — Hands-on builds. Real infrastructure, documented end to end.

**[tryhackme/](tryhackme/)** — Room completions and write-ups.

**[scripts/](scripts/)** — Automation and utility scripts in Python and Bash.

**[templates/](templates/)** — Reusable formats I use regularly.

---

## 🔗 Find Me

- **Portfolio:** [brandontrigo.com](https://brandontrigo.com)
- **GitHub:** [github.com/Btrigo](https://github.com/Btrigo)
- **LinkedIn:** [linkedin.com/in/brandonjtrigo31](https://linkedin.com/in/brandonjtrigo31)

---

*Last updated: June 2026*
