# Story Protocol — Grafana Dashboard Metrics (Final v3)

Operator-oriented reference for **all panels** included in the Story Grafana dashboard JSON.

- Images removed
- Ordered by dashboard rows
- Includes the **exact PromQL** configured in Grafana

---

## Overview – Network & Consensus

### Untitled

_No panel description in Grafana._

*(Text panel — no PromQL.)*

---

### Sync Status 

Indicates whether the node is currently syncing blocks.
A value of 1 means the node is still catching up; 0 means it is fully synced.
If this stays at 1 for an extended period, the node may be stalled, disconnected from peers, or experiencing disk / network issues.

**PromQL:**

```promql
cometbft_blocksync_syncing{job="$job"}
```

**Metrics used:** `cometbft_blocksync_syncing`

---

### Consensus Height

Current consensus block height observed by the node.
This value should continuously increase at the expected block cadence.
If it stalls while peers remain connected, it usually indicates consensus issues, sync problems, or node instability.

**PromQL:**

```promql
cometbft_consensus_height{job="$job"}
```

**Metrics used:** `cometbft_consensus_height`

---

### Number of Peers

Number of connected peers participating in consensus and block propagation.
A healthy peer count is required for timely vote and block propagation.
Low or fluctuating peer counts often correlate with increased block times, higher round counts, and degraded consensus performance.

**PromQL:**

```promql
cometbft_p2p_peers{job="$job"}
```

**Metrics used:** `cometbft_p2p_peers`

---

### Validator Last Signed Height

Last block height successfully signed by the validator.
This should closely track the current consensus height.
If it lags behind while consensus height continues to advance, the validator may be missing signatures or experiencing signing issues.

**PromQL:**

```promql
max by(validator_address) (cometbft_consensus_validator_last_signed_height{job="$job"})
```

**Metrics used:** `cometbft_consensus_validator_last_signed_height`

---

### Round Duration (avg / p95)

Duration of consensus rounds.
The average shows normal behavior, while p95 highlights tail latency and stalled rounds.
Rising p95 values typically indicate degraded consensus conditions, such as slow vote propagation, insufficient peers, or node performance bottlenecks.

**PromQL:**

```promql
sum by(instance) (rate(cometbft_consensus_round_duration_seconds_sum{job="$job"}[5m])) / (sum by(instance) (rate(cometbft_consensus_round_duration_seconds_count[5m])))
```

```promql
histogram_quantile(0.95, sum by(instance, le) (rate(cometbft_consensus_round_duration_seconds_bucket{job="$job"}[5m])))
```

**Metrics used:** `cometbft_consensus_round_duration_seconds_bucket`, `cometbft_consensus_round_duration_seconds_count`, `cometbft_consensus_round_duration_seconds_sum`

---

### Block Interval (avg / p95)

Time interval between consecutive blocks observed by the node.
The average reflects expected block cadence, while p95 captures irregular delays.
Increases usually point to consensus slowdowns, network instability, or validator participation issues.

**PromQL:**

```promql
sum by(instance) (rate(cometbft_consensus_block_interval_seconds_sum{job="$job"}[5m])) / (sum by(instance) (rate(cometbft_consensus_block_interval_seconds_count[5m])))
```

```promql
histogram_quantile(0.95, sum by(instance, le) (rate(cometbft_consensus_block_interval_seconds_bucket{job="$job"}[5m])))
```

**Metrics used:** `cometbft_consensus_block_interval_seconds_bucket`, `cometbft_consensus_block_interval_seconds_count`, `cometbft_consensus_block_interval_seconds_sum`

---

### Consensus Voting Power Participation (%)

Percentage of total voting power observed in consensus votes (prevote and precommit).
Values close to 1 (or 100%) indicate healthy participation and good vote propagation.
Sustained drops suggest network issues, poor connectivity, or validators failing to participate in consensus.

**PromQL:**

```promql
max by (vote_type) (cometbft_consensus_round_voting_power_percent{job="$job"})
```

**Metrics used:** `cometbft_consensus_round_voting_power_percent`

---



## Validator – Activity & Reliability

### Blocks Proposed (24h)

Number of blocks proposed by this validator over the last 24 hours.
This metric reflects validator activity and participation in block production.
Values depend on validator power and network size; prolonged periods at zero may indicate validator downtime, misconfiguration, or jailing.

**PromQL:**

```promql
increase(cometbft_consensus_proposal_create_count{job="$job"}[24h])
```

**Metrics used:** `cometbft_consensus_proposal_create_count`

---

### Missed Blocks (last 24h)

Number of consensus blocks missed by the validator over the last 24 hours.
Missed blocks directly impact validator reliability and may contribute to slashing or jailing if sustained.
Any non-zero increase should be investigated immediately.

**PromQL:**

```promql
increase(cometbft_consensus_validator_missed_blocks{job="$job"}[24h])
```

**Metrics used:** `cometbft_consensus_validator_missed_blocks`

---

### Validator Last Signed Height

Block height of the most recent block signed by the validator.

**PromQL:**

```promql
max by(validator_address) (cometbft_consensus_validator_last_signed_height{job="$job"})
```

**Metrics used:** `cometbft_consensus_validator_last_signed_height`

---



## Node Internals

### Block Size

Indicates the amount of data contained in the last block, in bytes.

**PromQL:**

```promql
cometbft_consensus_block_size_bytes{job="$job"}
```

**Metrics used:** `cometbft_consensus_block_size_bytes`

---

### Chain Size 

This metric shows the cumulative size of the blockchain as it grows over time, accounting for all blocks, transactions, and state data.

**PromQL:**

```promql
cometbft_consensus_chain_size_bytes{job="$job"}
```

**Metrics used:** `cometbft_consensus_chain_size_bytes`

---

### Validator Power

Reports the voting power of each validator.

**PromQL:**

```promql
cometbft_consensus_validator_power{job="$job"}
```

**Metrics used:** `cometbft_consensus_validator_power`

---

### Nº Missing Validators

This metric shows the voting power (stake) that absent validators represent. A high power of absent validators can have a negative impact on the security and decentralization of the network, as it reduces the available consensus power. Value: total power of the validators who are absent in the consensus process.

**PromQL:**

```promql
cometbft_consensus_missing_validators{job="$job"}
```

**Metrics used:** `cometbft_consensus_missing_validators`

---

### ABCI latency (avg)

Average latency of ABCI calls.
Useful to distinguish systemic application slowness (avg increases) from sporadic slow executions (only p95 increases).

**PromQL:**

```promql
sum(rate(cometbft_abci_connection_method_timing_seconds_sum{job="$job"}[5m]))
/
sum(rate(cometbft_abci_connection_method_timing_seconds_count{job="$job"}[5m]))
```

**Metrics used:** `cometbft_abci_connection_method_timing_seconds_count`, `cometbft_abci_connection_method_timing_seconds_sum`

---

### ABCI Method Latency (p95)

95th percentile latency of ABCI calls (e.g., CheckTx, DeliverTx, Commit).
Rising p95 indicates application-layer bottlenecks (state execution / DB / CPU), which can slow block production even if consensus participation remains healthy.

**PromQL:**

```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(cometbft_abci_connection_method_timing_seconds_bucket{job="$job"}[5m])
  )
)
```

**Metrics used:** `cometbft_abci_connection_method_timing_seconds_bucket`

---

### State Block  Processing Time

Measures block processing time. Records the time the node takes to process a block, which helps to evaluate its efficiency.
These metrics are fundamental for monitoring and diagnosing the performance and status of the node in the network.

**PromQL:**

```promql
cometbft_state_block_processing_time_bucket{job="$job"}
```

**Metrics used:** `cometbft_state_block_processing_time_bucket`

---

### Average Block Processing Time

This metric provides the average time it takes for the node to process a block, calculated by dividing the total block processing time (cometbft_state_block_processing_time_sum) by the total number of blocks processed (cometbft_state_block_processing_time_count). Monitoring the average block processing time is crucial for evaluating the efficiency of block finalization. If the average time increases, it may indicate potential performance bottlenecks or issues with the node's processing power. Keeping the average block processing time within an optimal range helps ensure the smooth functioning of the network and avoids delays in transaction finalization.

**PromQL:**

```promql
cometbft_state_block_processing_time_sum{job="$job"}
```

```promql
cometbft_state_block_processing_time_count{job="$job"}
```

**Metrics used:** `cometbft_state_block_processing_time_count`, `cometbft_state_block_processing_time_sum`

---

### Begin Blocker Duration

This metric measures the time taken to execute the begin blocker for various modules (e.g., distribution, mint, slashing, staking, upgrade). Begin blockers are executed at the start of each block to update the blockchain state and apply necessary logic before transactions are processed. The metric provides different quantiles (0.5, 0.9, 0.99) to show the distribution of execution times for each module. Monitoring this metric helps assess the performance of each module and identify potential bottlenecks that may impact the speed of block processing.

**PromQL:**

```promql
cosmos_begin_blocker{job="$job"}
```

**Metrics used:** `cosmos_begin_blocker`

---

### Proposal Receive Count

This metric measures the total count of block proposals that the node has received over time. The proposals are annotated with their status, indicating whether they were accepted or rejected by the consensus process. Monitoring this helps in understanding the node's participation in the consensus mechanism and provides insights into the efficiency and reliability of the proposal process within the network. It is particularly useful for diagnosing any issues with block proposal acceptance rates.

**PromQL:**

```promql
cometbft_consensus_proposal_receive_count{job="$job"}
```

**Metrics used:** `cometbft_consensus_proposal_receive_count`

---

### Late Votes

This metric captures instances where the node receives votes that are considered "late," meaning they belong to earlier stages of the consensus process. The presence of late votes can indicate network delays, synchronization issues, or potential inefficiencies in message propagation. Monitoring this helps in diagnosing network health and ensuring that nodes are maintaining timely consensus participation.

**PromQL:**

```promql
cometbft_consensus_late_votes{job="$job"}
```

**Metrics used:** `cometbft_consensus_late_votes`

---

### End Blocker Duration

This metric measures the time taken to execute the end blocker for different modules (e.g., evmstaking, gov, staking) within the Cosmos SDK. End blockers are critical functions that are run at the end of each block in the blockchain to finalize state changes and apply governance, staking, and other processes. The metric uses different quantiles (0.5, 0.9, 0.99) to show the distribution of execution times, providing insights into the efficiency of the end blockers.

**PromQL:**

```promql
cosmos_end_blocker
```

**Metrics used:** `cosmos_end_blocker`

---



## Debug (Extras)

### Consensus Parameter Updates

This metric counts how many times the application has updated the consensus parameters. These parameters define critical settings for the consensus process, such as block size, timeouts, and validator requirements. Monitoring this metric helps identify changes in the rules that govern the network's consensus mechanism. A high number of updates could indicate frequent tuning of network settings, which may affect how the network reaches consensus and how efficiently it operates.

**PromQL:**

```promql
cometbft_state_consensus_param_updates{job="$job"}
```

**Metrics used:** `cometbft_state_consensus_param_updates`

---

### Duplicate Block Part 

This metric captures instances where a block part has been received multiple times, which could indicate potential inefficiencies or network issues. Monitoring this helps in identifying redundant data transmissions and optimizing network bandwidth.

**PromQL:**

```promql
cometbft_consensus_duplicate_block_part{job="$job"}
```

**Metrics used:** `cometbft_consensus_duplicate_block_part`

---

### Duplicate Vote

This metric provides insight into how often duplicate votes are encountered during consensus. It could indicate potential misbehavior or inefficiencies in the voting process. Monitoring duplicate votes helps ensure the consensus protocol runs smoothly and efficiently

**PromQL:**

```promql
cometbft_consensus_duplicate_vote{job="$job"}
```

**Metrics used:** `cometbft_consensus_duplicate_vote`

---

### Byzantine Validators Power 

This metric indicates the total voting power of validators that have attempted to double-sign. It’s important for assessing the potential impact of byzantine activities on network consensus. A higher value could signal a significant threat to the network’s stability

**PromQL:**

```promql
cometbft_consensus_byzantine_validators_power{job="$job"}
```

**Metrics used:** `cometbft_consensus_byzantine_validators_power`

---

### Byzantine Validators 

Tracks the number of validators that attempted to double-sign. This metric helps identify validators that are engaging in byzantine behavior, such as attempting to create conflicting blocks. Monitoring this is crucial for maintaining the network’s integrity and security, as byzantine validators can potentially disrupt consensus.

**PromQL:**

```promql
cometbft_consensus_byzantine_validators{job="$job"}
```

**Metrics used:** `cometbft_consensus_byzantine_validators`

---

### Blocks Proposed (24h)

Number of blocks proposed by this node during the last 24 hours.

This metric is derived from the CometBFT consensus counter
cometbft_consensus_proposal_create_count and represents how often the node acted as block proposer in the current network.

A value of 0 over a long period may indicate:

the validator is not being selected as proposer,

the node is not actively participating in consensus,

or a configuration / connectivity issue.

**PromQL:**

```promql
increase(cometbft_consensus_proposal_create_count{job="$job"}[24h])
```

**Metrics used:** `cometbft_consensus_proposal_create_count`

---

### Missed Blocks (last 24h)

Number of blocks missed by the validator over a given time window.

**PromQL:**

```promql
increase(cometbft_consensus_validator_missed_blocks{job="$job"}[24h])
```

**Metrics used:** `cometbft_consensus_validator_missed_blocks`

---



## Consensus Health (Rounds & Timing)

### Consensus Rounds

Average consensus round number over the last 10 minutes. Ideally the network reaches consensus in the first round (near 0/1 depending on how rounds are indexed). If this value trends upward, it usually means blocks often require extra rounds, which can correlate with network instability, delayed votes, low participation, or validator connectivity/performance issues.

**PromQL:**

```promql
avg_over_time(cometbft_consensus_rounds{job="$job"}[10m])
```

**Metrics used:** `cometbft_consensus_rounds`

---

### Precommits Counted

Rate of precommit votes processed by the node.
This reflects how actively the node is receiving and processing consensus votes from the network.
Drops or irregular patterns may indicate peer connectivity issues, slow vote propagation, or local node performance problems.

**PromQL:**

```promql
rate(cometbft_consensus_precommits_counted{job="$job"}[5m])
```

**Metrics used:** `cometbft_consensus_precommits_counted`

---

### Step Duration (p95)

95th percentile duration of consensus steps (propose / prevote / precommit, etc.). This captures tail latency: if p95 increases, some steps are taking unusually long, which often indicates vote propagation delays, peer/network issues, overloaded node resources, or broader chain congestion. Use it as an early warning signal for consensus degradation.

**PromQL:**

```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(cometbft_consensus_step_duration_seconds_bucket{job="$job"}[5m])
  )
)
```

**Metrics used:** `cometbft_consensus_step_duration_seconds_bucket`

---

### ABCI method latency (p95)

95th percentile latency of ABCI calls by method (e.g., CheckTx, DeliverTx, Commit).
This reveals application-layer bottlenecks: rising p95 means the state machine is taking longer to process requests, which can slow block production even if consensus participation looks healthy.

**PromQL:**

```promql
histogram_quantile(
  0.95,
  sum by (le, method) (
    rate(cometbft_abci_connection_method_timing_seconds_bucket{job="$job"}[5m])
  )
)
```

**Metrics used:** `cometbft_abci_connection_method_timing_seconds_bucket`

---



## Token Distribution and Staking

### Nº Missing Validators 

This metric shows the voting power (stake) that absent validators represent. A high power of absent validators can have a negative impact on the security and decentralization of the network, as it reduces the available consensus power.

**PromQL:**

```promql
cometbft_consensus_missing_validators{job="$job"}
```

**Metrics used:** `cometbft_consensus_missing_validators`

---

### Total Power of Missing Validators 

It measures the total voting power (stake) of validators that are absent in the network consensus process with the chain_id=“iliad-0”.This metric indicates the total amount of consensus power (in terms of stake) that has been lost due to the absence of certain validators. It is crucial to assess the impact that the absence of these validators has on the security and stability of the network, as more absent voting power can weaken the consensus of the blockchain.

**PromQL:**

```promql
cometbft_consensus_missing_validators_power{job="$job"}
```

**Metrics used:** `cometbft_consensus_missing_validators_power`

---

### Staking Withdrawal Depth

Indicates the depth of the withdrawal queue in an EVM-based staking system. A queue depth of zero means that all staking withdrawal transactions have been processed and there are no pending transactions.
Value: number of pending staking withdrawal requests waiting to be processed.

**PromQL:**

```promql
evmstaking_withdrawal_queue_depth{job="$job"}
```

**Metrics used:** `evmstaking_withdrawal_queue_depth`

---

### Staking Queue Depth

Indicates the depth of the reward queue in an EVM-based staking system. A queue depth of zero means that all staking reward transactions have been processed and there are no pending transactions.
Value: number of pending staking reward requests waiting to be processed.

**PromQL:**

```promql
evmstaking_reward_queue_depth{job="$job"}
```

**Metrics used:** `evmstaking_reward_queue_depth`

---



## Transactions & gas

### Number of Transactions 

Counts the transactions in the most recent block. Helps to understand the network activity and the load of transactions processed by the node.

**PromQL:**

```promql
cometbft_consensus_num_txs{job="$job"}
```

**Metrics used:** `cometbft_consensus_num_txs`

---

### Total Transactions 

Shows the total number of transactions processed by the node. Indicates the total number of transactions processed in the chain by this node so far.

**PromQL:**

```promql
cometbft_consensus_total_txs{job="$job"}
```

**Metrics used:** `cometbft_consensus_total_txs`

---

### Successful Transactions

Counts the total number of successfully executed transactions in the network. This metric provides insight into the overall reliability and performance of the blockchain, tracking how many transactions have been completed without errors.

**PromQL:**

```promql
cosmos_tx_successful{job="$job"}
```

**Metrics used:** `cosmos_tx_successful`

---

### Transaction Count 

Records the total number of transactions performed. Helps to measure overall network activity by counting all transactions processed.

**PromQL:**

```promql
cosmos_tx_count{job="$job"}
```

**Metrics used:** `cosmos_tx_count`

---

### Gas Used

Indicates the amount of gas used in transactions. Reflects the gas consumed by recent transactions, which can show the efficiency of transactions.

**PromQL:**

```promql
cosmos_tx_gas_used{job="$job"}
```

**Metrics used:** `cosmos_tx_gas_used`

---

### Gas Wanted

Indicates the amount of gas requested in the transactions. Shows the gas that users estimated would be needed for their transactions.

**PromQL:**

```promql
cosmos_tx_gas_wanted{job="$job"}
```

**Metrics used:** `cosmos_tx_gas_wanted`

---



## Mempool & P2P

### P2P Metrics 

Measures the number of bytes received for each message type. Monitors the amount of data received from other nodes for different types of messages, such as blocks or status responses.

**PromQL:**

```promql
cometbft_p2p_message_receive_bytes_total{job="$job"}
```

**Metrics used:** `cometbft_p2p_message_receive_bytes_total`

---

### P2P Message Send Bytes Total 

This metric records the total volume of data, in bytes, that is being sent by the node for different message types over the P2P network. These message types are crucial for network operations, such as block responses, votes, consensus steps, and peer exchanges. Monitoring the bytes sent for each message type helps assess network bandwidth usage and detect potential bottlenecks or issues in message propagation. A high amount of data sent for messages like consensus_BlockPart or consensus_Vote reflects heavy network activity, especially during consensus processes. Tracking this helps ensure the node is not overwhelmed by sending too much data at once, which could degrade performance.

**PromQL:**

```promql
cometbft_p2p_message_send_bytes_total{job="$job"}
```

**Metrics used:** `cometbft_p2p_message_send_bytes_total`

---



## System Metrics

### Runtime Free Count 

Counts the number of times memory was freed in the system. Indicates how many memory free operations have been performed by the runtime since the start of the process, helping to understand the efficiency of memory usage.

**PromQL:**

```promql
cosmos_runtime_free_count{job="$job"}
```

**Metrics used:** `cosmos_runtime_free_count`

---

### GC Pause Time 

Measures how long the rubbish collector (GC) has paused execution. Allows to evaluate the impact of rubbish collection on system performance by showing how long it is paused to free memory.

**PromQL:**

```promql
cosmos_runtime_gc_pause_ns{job="$job"}
```

**Metrics used:** `cosmos_runtime_gc_pause_ns`

---

### Number of Goroutines 

Indicates the number of goroutines running. Reflects the number of concurrent tasks active on the system, providing a view of concurrency.

**PromQL:**

```promql
cosmos_runtime_num_goroutines{job="$job"}
```

**Metrics used:** `cosmos_runtime_num_goroutines`

---

### System Bytes 

Displays the total amount of memory allocated by the system. Reflects the total memory in use by runtime and other system resources.

**PromQL:**

```promql
cosmos_runtime_sys_bytes{job="$job"}
```

**Metrics used:** `cosmos_runtime_sys_bytes`

---

### Process Memory in Use

Measures the amount of memory allocated and still in use in the process. This metric indicates how many bytes of memory the process is currently using. It is essential for monitoring the node's memory usage, as a significant increase could affect its performance and stability. The metric helps to detect potential problems related to memory management, which can lead to optimisation of system resource usage.

**PromQL:**

```promql
cosmos_runtime_alloc_bytes{job="$job"}
```

**Metrics used:** `cosmos_runtime_alloc_bytes`

---


