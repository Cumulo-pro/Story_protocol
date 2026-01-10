# TECHNICAL CONTRIBUTIONS — Story Networks

📌 **Networks:** Story mainnet & Aeneid testnet

This repository documents the technical contributions provided by **Cumulo** to the Story ecosystem, focused on infrastructure, observability, connectivity, transparency, and technical education.

---

## Index

- [Endpoint Scan (RPC Monitoring)](#endpoint-scan-rpc-monitoring)
- [Decentralized Peer Monitor (PeerScan)](#decentralized-peer-monitor-peerscan)
- [Validator Resources Directory](#validator-resources-directory)
- [Story Snapshots](#story-snapshots)
- [Validator Documentation (Guides)](#validator-documentation-guides)
- [Story Grafana Metrics & Monitoring (v3)](#story-grafana-metrics-monitoring-v3)
- [Story Activity Tracker](#story-activity-tracker)
- [Public Endpoints](#public-endpoints)
- [Validator Alerts Bot](#validator-alerts-bot)
- [Story External Watcher Bot](#story-external-watcher-bot)
- [Technical Content & Education (Medium)](#technical-content-education-medium)
- [Story Validator Uptime Proof](#story-validator-uptime-proof)



![LINEA](https://github.com/user-attachments/assets/6cbf6840-7d91-482b-9f97-bdbaf8187e9f)

## 🔍 Endpoint Scan (RPC Monitoring)

**Resource:** check_d — Decentralized Endpoint Monitoring Tool  
**Live dashboards:**  
- Mainnet: https://cumulo.pro/services/story/rpcscan  
- Testnet: https://cumulo.pro/services/story-aeneid/rpcscan  

**Docs:**  
https://github.com/Cumulo-pro/Cumulo-Front-Chain/blob/main/check_End-Points/README.md

**Description:**  
Decentralized, multi-region monitoring system that evaluates the real performance and availability of public Story RPC endpoints using actual JSON-RPC calls (not ping/TCP checks). Provides objective metrics such as latency, sync status, block height, uptime, and node metadata.  

**Value for Story:**  
Improves transparency and reliability of public RPC infrastructure, helps detect degraded or unreliable endpoints early, and enables developers, indexers, and delegators to identify high-quality access points across regions.  

---

## 🌐 Decentralized Peer Monitor (PeerScan)

**Live dashboards:**  
- Mainnet: https://cumulo.pro/services/story/peerscan  
- Testnet: https://cumulo.pro/services/story-aeneid/peerscan
- 
**Docs:**  
https://github.com/Cumulo-pro/Cumulo-Front-Chain/tree/main/check_peers

**Description:**  
Distributed monitoring system that analyzes P2P peers in the Story Protocol network, aggregating latency, uptime, geolocation, and historical availability to produce ranked peer views.

**Value for Story:**  
Improves peer selection and network stability by helping validators and operators identify low-latency, high-availability peers across regions, strengthening the gossip and connectivity layer.

---

## 🧭 Validator Resources Directory

**Resources:**  
- Mainnet: https://cumulo.pro/services/story/resources  
- Testnet: https://cumulo.pro/services/story-aeneid/resources

**Description:**  
Continuously updated directory that aggregates validator-provided infrastructure and tooling for the Story Protocol ecosystem. Resources are indexed and filterable by category to enable fast discovery.

**Value for Story:**  
Improves accessibility and usability of the ecosystem by making public RPCs, gRPCs, APIs, EVM RPCs, explorers, snapshots, tools, and technical content easy to locate for developers, validators, delegators, and infrastructure operators.

Key Features:  
•	Indexed by resource type (RPC, gRPC, API, EVM, Snapshots, Tools, Content, Explorers)  
•	Covers contributions from multiple Story validators  
•	Supports both mainnet and testnet environments  
•	Regularly updated to reflect active infrastructure  

---

## 📦 Story Snapshots

**Resources:**  
- Mainnet: https://cumulo.pro/services/story/snapshot
- Testnet: https://cumulo.pro/services/story-aeneid/snapshot

**Description:**  
High-performance consensus and execution (Geth) snapshots for Story mainnet, optimized for fast and reliable node recovery using parallel downloads with aria2c.

**Value for Story:**  
Reduces node sync time and operational overhead for validators and node operators, improves network resilience during restarts or migrations, and enables faster recovery after incidents or maintenance.  

Key Features:  
•	Separate snapshots for consensus layer and Geth  
•	Optimized for multi-connection downloads (aria2c)  
•	Clear, reproducible restore procedure  
•	Designed to minimize downtime and sync-related issues  


---

## 📘 Validator Documentation (Guides)

**Resources:**  
- Story Node Installation Guide: https://cumulo.pro/services/story/install  
- Story Node CLI Command Reference: https://github.com/Cumulo-pro/Story_protocol/blob/main/story-mainnet-node-cli-commands.md

**Description:**  
Concise technical documentation for Story validators covering node installation and operational CLI commands, publicly maintained and versioned on GitHub.

---

## 📊 Story Grafana Metrics & Monitoring (v3)

**Resource:**  
- https://cumulo.pro/services/story/monitoring

**Docs:**  
https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring/README.md

**Description:**  
Production-grade Grafana monitoring dashboard (v3) for Story validators, providing clear separation between network health and validator performance, with renewed and unified technical documentation.

**Value for Story:**  
Improves operational visibility, helps validators detect consensus or performance issues early, and raises the overall quality and observability of Story’s validator infrastructure.

---

## 🧾 Story Activity Tracker

**Resource:**  
- https://cumulo.pro/services/story/activity?chain=Story

**Description:**  
Public, timestamped activity and incident log documenting all relevant operational events affecting our Story Protocol infrastructure, including incidents, upgrades, configuration changes, and maintenance actions.

**Value for Story:**  
Improves transparency and accountability for delegators, teams, and validators by providing clear visibility into infrastructure events, how they are handled, and the measures taken to prevent future issues.

---

## 🔌 Public Endpoints

**Resources:**  
- Mainnet: https://cumulo.pro/services/story/conect.php#public-endpoints  
- Testnet: https://cumulo.pro/services/story-aeneid/conect.php#public-endpoints

**Description:**  
Publicly available RPC, API, gRPC, JSON-RPC and WebSocket endpoints operated and maintained for the Story Protocol network.

---

## 🚨 Validator Alerts Bot

**Resource:**  
- https://cumulo.pro/services/story/monitoring#bot
  
**Docs:**  
- https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring_bot/story_validator_alerts.md

**Description:**  
Automated alerting system for Story Protocol validators, designed to notify operators of critical events affecting node health and performance.  

**Value for Story:**  
Enables faster incident detection and response, reducing downtime and improving overall reliability of validator operations across the network.  

---

## 🛰️ Story External Watcher Bot

**Resource:**  
- https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring_bot/story-external-watcher.py
  
**Docs:**  
- https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring_bot/README_story_external_watcher.md

**Description:**  
Internal monitoring bot that performs external checks against Story Protocol infrastructure and endpoints, with configurable rules and thresholds documented in GitHub.  

**Value for Story:**  
Adds an additional monitoring layer from an external perspective, improving early detection of connectivity or availability issues and complementing on-node alerting systems.  

---

## ✍️ Technical Content & Education (Medium)

**Resources:**  
- English: https://cumulo.pro/story/content  
- Spanish: https://cumulo.pro/story/content_es

**Description:**  
Ongoing publication of technical and educational content about Story Protocol on Medium, covering validator operations, infrastructure, ecosystem tooling, and network updates, published in both English and Spanish.  

**Value for Story:**  
Expands Story’s technical reach and understanding across a broader audience, including Spanish-speaking operators and builders, and provides long-form, reusable documentation beyond official channels  

**Audience:**  
- ~3.8K monthly presentations (Dec 2025)  
- 700+ lifetime followers  
- Growing base of email subscribers

---

## ✅ Story Validator Uptime Proof

**Resource:** Validator Uptime Proof (on-chain, reproducible)  
**Repository:**  
https://github.com/Cumulo-pro/Story_protocol/tree/main/validator-uptime-proof

**Description:**  
Reproducible and **on-chain verifiable method** to calculate **Story Mainnet validator consensus uptime**, based exclusively on **block commit signatures** queried from an **archive RPC**.

This tool measures **actual consensus participation** (whether a validator signs block commits when required), not server uptime, process uptime, or RPC availability.

**Value for Story:**  
Provides an auditable and reproducible **uptime proof** suitable for **delegation programs and validator evaluations**, based on the metric that truly matters for network security: **on-chain consensus participation**.

**Key Properties:**  
- Fully on-chain and explorer-independent  
- Reproducible by any third party  
- Does not rely on local node state  
- Aligned with Cosmos-based validator evaluation standards  

---

*Maintained by Cumulo Pro.*
