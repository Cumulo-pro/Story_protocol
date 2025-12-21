# Story Metrics and Grafana Dashboard

![PortadaGithub (3)](https://github.com/user-attachments/assets/57b006a4-1d59-4b90-8447-0ccbca335ae1)

This repository provides a complete **observability stack for Story nodes**, focused on validator operations, consensus health, and network performance.

It includes Prometheus metrics, production-ready Grafana dashboards, and alerting tools designed to help node operators monitor synchronization, consensus behavior, validator participation, transaction throughput, and system-level performance in real time.

The dashboards and documentation are built from real operational experience running Story infrastructure in both **mainnet** and **testnet (Aeneid)** environments.

---

## What this dashboard covers

The Story Grafana dashboards provide visibility into:

- 🧱 Block production and block interval stability (avg / p95)
- 🤝 Consensus health (round duration, voting power participation, quorum behavior)
- 🧑‍⚖️ Validator performance (missed blocks, last signed height, proposal activity)
- 📦 Transaction throughput and gas usage
- 🔁 Mempool pressure and backlog
- 🌐 P2P traffic and peer behavior
- 🧠 Runtime, memory, and garbage collection metrics

---

## First steps

Enable Prometheus metrics in your Story node configuration.

Modify the `config.toml` file located at:

```bash
$HOME/.story/story/config/config.toml
```

Set:

```toml
prometheus = true
prometheus_listen_addr = ":26660"
```

Restart the node:

```bash
sudo systemctl restart story
sudo journalctl -u story -f
```

Verify Prometheus metrics are exposed:

```bash
curl http://localhost:26660/metrics
```

Or from a browser:

```
http://<your-node-ip>:26660/metrics
```

---

## Configure Prometheus

On your Prometheus server, edit:

```bash
/etc/prometheus/prometheus.yml
```

Add the Story node job:

```yaml
- job_name: story
  static_configs:
    - targets: ['<your-node-ip>:26660']
```

Restart Prometheus:

```bash
sudo systemctl restart prometheus
sudo journalctl -u prometheus -f --no-hostname -o cat
```

---

## Story Metrics

Story metrics expose detailed information about consensus behavior, validator performance, transactions, and system health.

For a full description of all metrics and PromQL examples:

[![Metrics](https://img.shields.io/badge/Metrics-View%20Metrics-blue?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring/story_metrics.md)

---

## Grafana Dashboard

The Grafana dashboard provides **real-time, operator-focused visualizations** of consensus behavior, validator performance, transaction activity, and node resource usage. It is designed to support both day-to-day monitoring and incident analysis.

Download the dashboard JSON:

[![Grafana Dashboard](https://img.shields.io/badge/Grafana%20Dashboard-Download-blue?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring/Story%20Dashboard%20by%20Cumulo%20v3-1766318499782.json)

Official Grafana dashboard:

[![Official Grafana Dashboard](https://img.shields.io/badge/Grafana%20Dashboard-Official-blue?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com/grafana/dashboards/22059-story-dashboard-by-cumulo/)

---

## Grafana Dashboard demo (public)

A public, read-only demo of the Story dashboard is available:

[![Grafana Dashboard Demo](https://img.shields.io/badge/Grafana%20Dashboard-Demo-blue?style=for-the-badge&logo=grafana&logoColor=white)](http://74.208.16.201:3000/public-dashboards/17c6d645404a400f8aa7c3c532fd4a61?orgId=1&refresh=5s)

---

## 🧪 Story Aeneid (Testnet) Monitoring

Full monitoring support is also available for the **Story Aeneid testnet**, including Prometheus metrics and a dedicated Grafana dashboard.

Metrics documentation:

[![Story Aeneid Node Metrics FAQ](https://img.shields.io/badge/Story%20Aeneid%20Metrics-View-blue?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring/story_aeneid_metrics.md)

Aeneid dashboard:

[![Story Aeneid Dashboard](https://img.shields.io/badge/Grafana%20Dashboard-Aeneid-blue?style=for-the-badge&logo=grafana&logoColor=white)](https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring/Story%20Dashboard%20Aeneid%20by%20Cumulo-1749224644414.json)

---

## 🤖 Story Node Alert Bot

Stay informed in real time with the **Story Node Alert Bot**, a Telegram-based alerting system powered by Prometheus and Alertmanager.

The bot notifies you about:

- ⛓️ Sync status
- 🧠 Peer count and validator power
- 🟢 Node heartbeat (block height and availability)
- 🔴 Downtime or connectivity issues

Full setup and configuration guide:

[![Story Alert Bot Guide](https://img.shields.io/badge/Story%20Alert%20Bot-View%20Guide-blue?style=for-the-badge&logo=telegram)](https://github.com/Cumulo-pro/Story_protocol/blob/main/monitoring/README_story_node_bot.md)

---

## Intended audience

This repository is intended for:

- Story validators and node operators
- Infrastructure and SRE teams
- Protocol engineers debugging consensus or performance issues
- Community members interested in deep network observability
