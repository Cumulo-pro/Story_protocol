# TECHNICAL CONTRIBUTIONS — Story Networks

**Networks:** Story mainnet & Aeneid testnet

This repository documents the technical contributions provided by **Cumulo** to the Story ecosystem, focused on infrastructure, observability, connectivity, transparency, and technical education.

---

## Index

- [Endpoint Scan (RPC Monitoring)](#endpoint-scan-rpc-monitoring)
- [Decentralized Peer Monitor (PeerScan)](#decentralized-peer-monitor-peerscan)
- [Validator Resources Directory](#validator-resources-directory)
- [Story Snapshots](#story-snapshots)
- [Validator Documentation (Guides)](#validator-documentation-guides)
- [Story Grafana Metrics & Monitoring (v3)](#story-grafana-metrics--monitoring-v3)
- [Story Activity Tracker](#story-activity-tracker)
- [Public Endpoints](#public-endpoints)
- [Validator Alerts Bot](#validator-alerts-bot)
- [Story External Watcher Bot](#story-external-watcher-bot)
- [Technical Content & Education (Medium)](#technical-content--education-medium)


![LINEA](https://github.com/user-attachments/assets/6cbf6840-7d91-482b-9f97-bdbaf8187e9f)

## Endpoint Scan (RPC Monitoring)

**Resource:** check_d — Decentralized Endpoint Monitoring Tool  
**Live dashboards:**  
- Mainnet: https://cumulo.pro/services/story/rpcscan  
- Testnet: https://cumulo.pro/services/story-aeneid/rpcscan  
**Docs:**  
https://github.com/Cumulo-pro/Cumulo-Front-Chain/blob/main/check_End-Points/README.md

**Description:**  
Decentralized, multi-region monitoring system that evaluates the real performance and availability of public Story RPC endpoints using actual JSON-RPC calls (not ping or TCP checks).

**Value for Story:**  
Improves transparency and reliability of public RPC infrastructure and helps identify degraded or unreliable endpoints early.

---

## Decentralized Peer Monitor (PeerScan)

**Live dashboards:**  
- Mainnet: https://cumulo.pro/services/story/peerscan  
- Testnet: https://cumulo.pro/services/story-aeneid/peerscan  
**Docs:**  
- https://github.com/Cumulo-pro/Cumulo-Front-Chain/tree/main/check_peers

**Description:**  
Distributed monitoring system that analyzes P2P peers, aggregating latency, uptime, geolocation, and historical availability to produce ranked peer views.

**Value for Story:**  
Improves peer selection and network stability by helping operators identify low-latency, high-availability peers across regions.

---

## Validator Resources Directory

**Resources:**  
- Mainnet: https://cumulo.pro/services/story/resources  
- Testnet: https://cumulo.pro/services/story-aeneid/resources

**Description:**  
Continuously updated directory aggregating validator-provided infrastructure and tooling, indexed and filterable by category.

**Value for Story:**  
Improves accessibility and usability of RPCs, APIs, explorers, snapshots, tools, and technical content for the ecosystem.

---

## Story Snapshots

**Resources:**  
- Mainnet: https://cumulo.pro/services/story/snapshot
- Testnet: https://cumulo.pro/services/story-aeneid/snapshot

**Description:**  
High-performance consensus and execution (Geth) snapshots optimized for fast and reliable node recovery using parallel downloads.

**Value for Story:**  
Reduces node sync time and operational overhead, improving network resilience and recovery speed.

---

## Validator Documentation (Guides)

**Resources:**  
- Story Node Installation Guide: https://cumulo.pro/services/story/install  
- Story Node CLI Command Reference: https://github.com/Cumulo-pro/Story_protocol/blob/main/story-mainnet-node-cli-commands.md

**Description:**  
Concise technical documentation for validators, publicly maintained and versioned on GitHub.

---

## Story Grafana Metrics & Monitoring (v3)

**Resource:**  
- https://cumulo.pro/services/story/monitoring

**Description:**  
Production-grade Grafana dashboard providing clear separation between network health and validator performance, with unified documentation.

**Value for Story:**  
Improves operational visibility and early detection of consensus or performance issues.

---

## Story Activity Tracker

**Resource:**  
- https://cumulo.pro/services/story/activity?chain=Story

**Description:**  
Public, timestamped activity and incident log documenting infrastructure events, upgrades, and maintenance actions.

**Value for Story:**  
Improves transparency and accountability for delegators, teams, and validators.

---

## Public Endpoints

**Resources:**  
- Mainnet: https://cumulo.pro/services/story/conect.php#public-endpoints  
- Testnet: https://cumulo.pro/services/story-aeneid/conect.php#public-endpoints

**Description:**  
Public RPC, API, gRPC, JSON-RPC, and WebSocket endpoints operated and maintained for Story.

---

## Validator Alerts Bot

**Resource:**  
- https://cumulo.pro/services/story/monitoring#bot  
**Docs:**  
- https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring_bot/story_validator_alerts.md

**Description:**  
Automated alerting system notifying operators of critical events affecting node health and performance.

**Value for Story:**  
Enables faster incident detection and response, reducing downtime.

---

## Story External Watcher Bot

**Resource:**  
- https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring_bot/story-external-watcher.py  
**Docs:**  
- https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring_bot/README_story_external_watcher.md

**Description:**  
Internal monitoring bot performing external checks against infrastructure and endpoints with configurable rules.

**Value for Story:**  
Adds an additional external monitoring layer, complementing on-node alerting systems.

---

## Technical Content & Education (Medium)

**Resources:**  
- English: https://cumulo.pro/story/content  
- Spanish: https://cumulo.pro/story/content_es

**Description:**  
Ongoing publication of technical and educational content covering validator operations, infrastructure, and ecosystem tooling, published in English and Spanish.

**Audience:**  
- ~3.8K monthly presentations (Dec 2025)  
- 700+ lifetime followers  
- Growing base of email subscribers

---

*Maintained by Cumulo Pro.*
