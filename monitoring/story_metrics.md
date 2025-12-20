# Story Node Metrics FAQ

# Index

1. [Story Node Metrics FAQ](#story-node-metrics-faq)
   - [Sync Status](#sync-status)
   - [Consensus Height](#consensus-height)
   - [Latest Block Height](#latest-block-height)
   - [Block Size](#block-size)
   - [Peers Connected](#peers-connected)
   - [State Block Processing Time](#state-block-processing-time)
   - [Average Block Processing Time](#average-block-processing-time)
   - [Chain Size](#chain-size)
   - [Late Votes](#late-votes)
   - [Proposal Receive Count](#proposal-receive-count)
   - [Begin Blocker Duration](#begin-blocker-duration)
   - [End Blocker Duration](#end-blocker-duration)
   
2. [Token Distribution and Staking](#token-distribution-and-staking)
   - [Staking Delegate](#staking-delegate)
   - [Staking Undelegate](#staking-undelegate)
   - [Staking Redelegate](#staking-redelegate)
   - [Staking Delegate Transactions](#staking-delegate-transactions)
   - [Staking Redelegate Transactions](#staking-redelegate-transactions)
   - [Staking Undelegate Transactions](#staking-undelegate-transactions)
   - [Staking Queue Depth](#staking-queue-depth)
   - [Staking Queue Depth](#staking-queue-depth-1)

3. [Validator Data](#validator-data)
   - [Nº Missing Validators](#n-missing-validators)
   - [Total Power of Missing Validators](#total-power-of-missing-validators)
   - [Validator Set Updates](#validator-set-updates)
   - [Consensus Parameter Updates](#consensus-parameter-updates)
   - [Byzantine Validators Power](#byzantine-validators-power)
   - [Byzantine Validators](#byzantine-validators)
   - [Duplicate Block Part](#duplicate-block-part)
   - [Duplicate Vote](#duplicate-vote)

4. [Transactions & Gas](#transactions--gas)
   - [Number of Transactions](#number-of-transactions)
   - [Total Transactions](#total-transactions)
   - [Successful Transactions](#successful-transactions)
   - [Transaction Count](#transaction-count)
   - [Gas Used](#gas-used)
   - [Gas Wanted](#gas-wanted)

5. [Mempool](#mempool)
   - [Mempool Size](#mempool-size)
   - [Mempool Size in Bytes](#mempool-size-in-bytes)

6. [P2P Metrics](#p2p-metrics)
   - [P2P Message Receive Bytes Total](#p2p-message-receive-bytes-total)
   - [P2P Message Send Bytes Total](#p2p-message-send-bytes-total)

7. [System Metrics](#system-metrics)
   - [Runtime Free Count](#runtime-free-count)
   - [GC Pause Time](#gc-pause-time)
   - [Number of Goroutines](#number-of-goroutines)
   - [System Bytes](#system-bytes)
   - [Process Memory in Use](#process-memory-in-use)


_______________________________________________

## Sync Status  

*cometbft_blocksync_syncing*  

Indicates whether the node is synchronizing blocks.  
Value: Displays 1 if the node is synchronizing and 0 if it is not, helping to diagnose the synchronization status.  
![image](https://github.com/user-attachments/assets/ee4f75ba-2600-4f35-bfda-115d25b7c983)

## Consensus Height  

*cometbft_consensus_height*

Measures the height of the consensus block.  
Value: Number representing the last block reached by the node consensus.  
![image](https://github.com/user-attachments/assets/413fb7ee-6263-416e-8e84-7c3f6e588dd5)

## Latest Block Height

*cometbft_blocksync_latest_block_height*  

This is the number of the highest block processed by the node, indicating whether it is up to date with the network.  
Value: Number representing highest block processed by the node.  
![image](https://github.com/user-attachments/assets/5b472c4d-dfb8-4120-beab-4f164702d099)

## Block Size  

*cometbft_consensus_block_size_bytes*  

This metric provides the size of individual blocks processed by the node. It reflects the amount of data contained in a single block, such as transactions and other relevant information. Monitoring block size is crucial for understanding the network's data throughput and can help in identifying performance issues, especially when block sizes grow too large or remain consistently small.  
Value: size of each block in bytes.  
![image](https://github.com/user-attachments/assets/a4c5f097-4548-4003-b73e-17efc45ba56c)

## Peers Connected

*cometbft_p2p_peers*  

Monitors the number of peers connected to the node in the P2P network. However, monitoring the number of peers is essential to detect if there are too few (which might signal network partition or connectivity issues) or too many (which could lead to resource strain on the node). Maintaining an optimal number of peers ensures efficient block propagation, consensus participation, and overall network performance.  
Value: number of peers that are connected to the node. A higher number of peers can indicate good network connectivity, ensuring a healthy and distributed exchange of information.  
![image](https://github.com/user-attachments/assets/4402c7b4-9a50-4b6c-8b1f-9b066ed71417)


## State Block  Processing Time  

*cometbft_state_block_processing_time_bucket*  

Measures block processing time. Records the time the node takes to process a block, which helps to evaluate its efficiency.
These metrics are fundamental for monitoring and diagnosing the performance and status of the node in the network.  
Value: histogram representing block times  
![image](https://github.com/user-attachments/assets/3d683ee0-9dfa-4d4d-b95f-db394582366a)

## Average Block Processing Time

*cometbft_state_block_processing_time_sum / cometbft_state_block_processing_time_count*  

This metric provides the average time it takes for the node to process a block, calculated by dividing the total block processing time (cometbft_state_block_processing_time_sum) by the total number of blocks processed (cometbft_state_block_processing_time_count). Monitoring the average block processing time is crucial for evaluating the efficiency of block finalization. If the average time increases, it may indicate potential performance bottlenecks or issues with the node's processing power. Keeping the average block processing time within an optimal range helps ensure the smooth functioning of the network and avoids delays in transaction finalization.
Value: average time spent processing each block.  
![image](https://github.com/user-attachments/assets/bd8b0066-2e52-4e0a-9c80-97a8f0d5fb84)


## Chain Size  

*cometbft_consensus_chain_size_bytes*

This metric shows the cumulative size of the blockchain as it grows over time, accounting for all blocks, transactions, and state data. Understanding the chain size helps track data storage requirements and manage resources, especially for nodes with limited storage capacity.  
Value: size of the blockchain in bytes  
![image](https://github.com/user-attachments/assets/39faf527-e104-49cb-8a15-c4a1f67839fc)

## Late Votes   

*cometbft_consensus_late_votes*

This metric captures instances where the node receives votes that are considered "late," meaning they belong to earlier stages of the consensus process. The presence of late votes can indicate network delays, synchronization issues, or potential inefficiencies in message propagation. Monitoring this helps in diagnosing network health and ensuring that nodes are maintaining timely consensus participation.  
Value: number of votes received by the node that correspond to previous heights and rounds than the node’s current state.  
![image](https://github.com/user-attachments/assets/7bf32f7a-9611-4227-b1fa-ca1099e567a7)

## Proposal Receive Count  

*cometbft_consensus_proposal_receive_count*

This metric measures the total count of block proposals that the node has received over time. The proposals are annotated with their status, indicating whether they were accepted or rejected by the consensus process. Monitoring this helps in understanding the node's participation in the consensus mechanism and provides insights into the efficiency and reliability of the proposal process within the network. It is particularly useful for diagnosing any issues with block proposal acceptance rates.  
Value: total number of proposals received by the node since the process started, categorized by status ('accepted' or 'rejected').  
![image](https://github.com/user-attachments/assets/20436329-e905-487e-a8f4-ee7a97571225)

## Begin Blocker Duration

*cosmos_begin_blocker*  

This metric measures the time taken to execute the begin blocker for various modules (e.g., distribution, mint, slashing, staking, upgrade). Begin blockers are executed at the start of each block to update the blockchain state and apply necessary logic before transactions are processed. The metric provides different quantiles (0.5, 0.9, 0.99) to show the distribution of execution times for each module. Monitoring this metric helps assess the performance of each module and identify potential bottlenecks that may impact the speed of block processing.
Value: duration of the begin blocker execution for different modules in the Cosmos SDK.  
![image](https://github.com/user-attachments/assets/94c26b6c-0107-4200-892c-34653c1db2ac)


## End Blocker Duration  

*cosmos_end_blocker*  

This metric measures the time taken to execute the end blocker for different modules (e.g., evmstaking, gov, staking) within the Cosmos SDK. End blockers are critical functions that are run at the end of each block in the blockchain to finalize state changes and apply governance, staking, and other processes. The metric uses different quantiles (0.5, 0.9, 0.99) to show the distribution of execution times, providing insights into the efficiency of the end blockers.   
Value: duration of the end blocker execution for different modules in the Cosmos SDK.  
![image](https://github.com/user-attachments/assets/31c4e8b0-9d7d-4d21-8cf0-6bfbea433fef)

## Token Distribution and Staking
_________________________________

## Staking Delegate  

*cosmos_staking_delegate*

Measures how many times users have delegated tokens to validators, showing staking activity on the network. 

Value: Counts the total number of staking delegations.  
![image](https://github.com/user-attachments/assets/4a250fa0-f90e-4529-ae14-2829bfc0b14c)

## Staking Undelegate  

*cosmos_staking_undelegate*

Displays the total number of undelegate events that have occurred in the network.  
Value: number of times delegations have been withdrawn.  
![image](https://github.com/user-attachments/assets/82c61e25-b06c-493a-8e7a-dc282c939c78)

## Staking Redelegate  

*cosmos_staking_redelegate*

Displays the total number of redelegate events that have occurred in the network.
Value: number of times staking delegations have been reallocated from one validator to another.  
![image](https://github.com/user-attachments/assets/3196a022-41b3-45a6-8e7f-11be513c9923)

## Staking Delegate Transactions  

*cosmos_tx_msg__cosmos_staking_v1beta1_MsgDelegate*

Tracks the number of delegation transactions for the Cosmos staking module. Displays the total amount of tokens delegated in the network .  
Value: number of delegation transactions for the Cosmos staking module.  
![image](https://github.com/user-attachments/assets/f88c8c0b-f9e7-48fc-8054-9d4b36d72a28)

## Staking Redelegate Transactions  

*cosmos_tx_msg__cosmos_staking_v1beta1_MsgBeginRedelegate*

Tracks the number of redelegation transactions initiated in the Cosmos staking module. Displays the total amount of tokens involved in redelegation.  
Value: number of redelegation transactions for the Cosmos staking module.  
![image](https://github.com/user-attachments/assets/e6950839-6274-449a-b979-8697d29ba543)

## Staking Undelegate Transactions   

*cosmos_tx_msg__cosmos_staking_v1beta1_MsgUndelegate*  

Tracks the number of undelegation transactions initiated in the Cosmos staking module. Displays the total amount of tokens undelegated 
Value: number of undelegation transactions for the Cosmos staking module.  
![image](https://github.com/user-attachments/assets/96a77a37-d53b-48da-8e07-346021d89719)

## Staking Queue Depth  

*evmstaking_queue_depth*  

Monitors the depth of the staking queue in an EVM-based staking system. A queue depth of zero means that all staking requests have been processed and there are no outstanding transactions. Monitoring this metric is important for understanding the network's ability to handle staking requests efficiently and identifying any delays or congestion in the staking process. A growing queue depth may signal potential bottlenecks in processing staking transactions.  
Value: number of pending staking or delegation requests waiting to be processed.  
![image](https://github.com/user-attachments/assets/8604c005-f099-43ce-97e6-29d84e813885)

## Staking Queue Depth 

*evmstaking_queue_depth*  

Monitors the depth of the staking queue in an EVM-based staking system. A higher queue depth indicates that there are multiple staking or delegation requests waiting to be executed, which may point to a potential delay or bottleneck in processing. Monitoring this metric helps ensure that staking operations are being handled efficiently and provides insight into the network's ability to process staking requests in a timely manner.
Value: number of pending staking or delegation requests waiting to be processed in the staking queue.  
![image](https://github.com/user-attachments/assets/c877dce3-493c-456a-a0a0-f6e8465f76fd)


## Validator data
_________________________________

## Nº Missing Validators 

*cometbft_consensus_missing_validators*  

This metric shows the voting power (stake) that absent validators represent. A high power of absent validators can have a negative impact on the security and decentralization of the network, as it reduces the available consensus power.
Value: total power of the validators who are absent in the consensus process.  
![image](https://github.com/user-attachments/assets/83e0aa42-1f02-44ab-bba0-e0fe7fbbe281)

## Total Power of Missing Validators   

*cometbft_consensus_missing_validators_power*  

It measures the total voting power (stake) of validators that are absent in the network consensus process with the chain_id=“iliad-0”.This metric indicates the total amount of consensus power (in terms of stake) that has been lost due to the absence of certain validators. It is crucial to assess the impact that the absence of these validators has on the security and stability of the network, as more absent voting power can weaken the consensus of the blockchain.
Value: total voting power (stake) of validators who are absent in the consensus process in the network.   
![image](https://github.com/user-attachments/assets/a98e5ffa-6428-4a15-ba04-3e6e53211659)

## Validator Set Updates 

*cometbft_state_validator_set_updates*  

This metric counts how many times the validator set has been updated by the application. Validator set updates occur when validators join, leave, or their power changes, affecting the composition of the active validators responsible for consensus. Monitoring this metric is crucial for understanding the dynamics of validator participation and network governance. A high number of updates may indicate frequent changes in validator status, which can affect network stability and security.  
Value: number of updates to the validator set since the node process started.  
![image](https://github.com/user-attachments/assets/cd42671b-3d4f-4de0-aa6d-a976d6c921cb)

## Consensus Parameter Updates  

*cometbft_state_consensus_param_updates*  

This metric counts how many times the application has updated the consensus parameters. These parameters define critical settings for the consensus process, such as block size, timeouts, and validator requirements. Monitoring this metric helps identify changes in the rules that govern the network's consensus mechanism. A high number of updates could indicate frequent tuning of network settings, which may affect how the network reaches consensus and how efficiently it operates.  
Value: number of updates to the consensus parameters since the node process started.  
![image](https://github.com/user-attachments/assets/140aa820-9572-444d-9e76-3659d5481f27)

## Byzantine Validators Power  

*cometbft_consensus_byzantine_validators_power*

This metric indicates the total voting power of validators that have attempted to double-sign. It’s important for assessing the potential impact of byzantine activities on network consensus. A higher value could signal a significant threat to the network’s stability.  
Value: total power of byzantine validators.  
![image](https://github.com/user-attachments/assets/ec6d6d71-aebd-45e0-b72e-4e669c113f9c)

## Byzantine Validators 

*cometbft_consensus_byzantine_validators*  

This metric helps identify validators that are engaging in byzantine behavior, such as attempting to create conflicting blocks. Monitoring this is crucial for maintaining the network’s integrity and security, as byzantine validators can potentially disrupt consensus.  
Value: number of validators that attempted to double-sign.  
![image](https://github.com/user-attachments/assets/4c75f1a6-7b88-4f6c-80c3-9e2e03de92ec)

## Duplicate Block Part   

*cometbft_consensus_duplicate_block_part*  

This metric captures instances where a block part has been received multiple times, which could indicate potential inefficiencies or network issues. Monitoring this helps in identifying redundant data transmissions and optimizing network bandwidth.  
Value: number of times a duplicate block part has been received.  
![image](https://github.com/user-attachments/assets/d2d2cc58-9d53-4f91-b4d7-d89823d6c074)

## Duplicate Vote   

*cometbft_consensus_duplicate_vote*  

This metric provides insight into how often duplicate votes are encountered during consensus. It could indicate potential misbehavior or inefficiencies in the voting process. Monitoring duplicate votes helps ensure the consensus protocol runs smoothly and efficiently.  
Value: number of times duplicate votes have been received.  
![image](https://github.com/user-attachments/assets/6689e2d1-230d-4b85-9a5b-df6ee3e9b787)


## Transactions & gas  
_________________________________

## Number of Transactions 

*cometbft_consensus_num_txs*  

Helps to understand the network activity and the load of transactions processed by the node.  
Value: Nº transactions in the most recent block.  
![image](https://github.com/user-attachments/assets/aeb1cf68-4158-428a-97e4-fcfb6db1117d)

## Total Transactions   

*cometbft_consensus_total_txs*  

Indicates the total number of transactions processed in the chain by this node so far.
Value: total number of transactions processed by the node.  
![image](https://github.com/user-attachments/assets/64dd988e-7255-4156-a315-ae07e5981338)

## Successful Transactions

*cosmos_tx_successful*

This metric provides insight into the overall reliability and performance of the blockchain, tracking how many transactions have been completed without errors.  
Value: total number of successfully executed transactions in the network.  
![image](https://github.com/user-attachments/assets/604a6dbd-6dc1-446d-8fd2-7f0a34835936)


## Transaction Count 

*cosmos_tx_count*

Records the total number of transactions performed. Helps to measure overall network activity by counting all transactions processed.  
Value: total number of transactions performed.  
![image](https://github.com/user-attachments/assets/5159a769-9657-4cd1-8c1f-c50244964892)

## Gas Used  

*cosmos_tx_gas_used*  

Indicates the amount of gas used in transactions. Reflects the gas consumed by recent transactions, which can show the efficiency of transactions.  
Value: amount of gas used in transactions.  
![image](https://github.com/user-attachments/assets/e30a8d04-edb8-4ca1-8af5-7371d8c00bef)

## Gas Wanted  

*cosmos_tx_gas_wanted*  

Indicates the amount of gas requested in the transactions. Shows the gas that users estimated would be needed for their transactions.  
Value: amount of gas requested in the transactions.  
![image](https://github.com/user-attachments/assets/cd96ce53-1659-454f-a671-a469b5cb6912)

## Mempool
_________________________________

## Mempool Size

*cometbft_mempool_size*  

Monitors the number of uncommitted transactions in the mempool. The mempool is a temporary holding area for transactions that have been submitted but not yet confirmed. A larger mempool size indicates that there are many transactions waiting to be processed, which may suggest network congestion or delays in block production. Monitoring this helps assess the network's ability to process transactions efficiently and manage load.  
Value:   current number of transactions waiting to be included in a block.  
![image](https://github.com/user-attachments/assets/c4a639cc-f39f-4868-94aa-25dbdede15b7)

## Mempool Size in Bytes 

*cometbft_mempool_size_bytes*  

This metric measures the total memory footprint of the mempool, indicating the combined size of all uncommitted transactions in bytes. It is useful for understanding how much data is being held in the mempool at any given time. Monitoring the size in bytes can provide insights into memory usage and help ensure that the node is not overwhelmed by a large volume of transactions, which could lead to performance issues.  
Value: total size of the mempool in bytes.   
![image](https://github.com/user-attachments/assets/3988cd4a-f731-4f01-b123-2f48ce71a4b0)

## P2P Metrics 

*cometbft_p2p_message_receive_bytes_total*  

This metric records the total amount of data, in bytes, received for different types of messages exchanged in the P2P network of a CometBFT (Tendermint) blockchain. Each message type serves a specific function, such as block requests, votes, proposals, and consensus steps. Monitoring the volume of data received for each message type is important for understanding network traffic and detecting any unusual patterns that may indicate performance issues or potential attacks. A higher number of bytes in certain message types, such as consensus_BlockPart or consensus_Vote, could reflect high activity in the consensus process, while spikes in other message types could signal issues.  
Value: total number of bytes received for each message type in the peer-to-peer (P2P) network.  
![image](https://github.com/user-attachments/assets/97d3c3b6-8ff1-41fa-bcac-83b9f500cc2e)


## P2P Message Send Bytes Total

*cometbft_p2p_message_send_bytes_total*  

This metric records the total volume of data, in bytes, that is being sent by the node for different message types over the P2P network. These message types are crucial for network operations, such as block responses, votes, consensus steps, and peer exchanges. Monitoring the bytes sent for each message type helps assess network bandwidth usage and detect potential bottlenecks or issues in message propagation. A high amount of data sent for messages like consensus_BlockPart or consensus_Vote reflects heavy network activity, especially during consensus processes. Tracking this helps ensure the node is not overwhelmed by sending too much data at once, which could degrade performance.  
Value: total number of bytes sent for each message type in the peer-to-peer (P2P) network.
![image](https://github.com/user-attachments/assets/69ee9a21-bf4e-4df6-a19a-2a76d7191401)

## System Metrics  
_________________________________

## Runtime Free Count 

*cosmos_runtime_free_count*  

Indicates how many memory free operations have been performed by the runtime since the start of the process, helping to understand the efficiency of memory usage.
Value: number of times memory was freed in the system.  
![image](https://github.com/user-attachments/assets/2c471bc5-819c-4bef-bfd1-bbe0824fa7ec)

## GC Pause Time 

*cosmos_runtime_gc_pause_ns*  

Measures how long the rubbish collector (GC) has paused execution. Allows to evaluate the impact of rubbish collection on system performance by showing how long it is paused to free memory.
Value: time that the garbage collector (GC) has paused the execution of a garbage collection operation.  
![image](https://github.com/user-attachments/assets/383baf06-c844-45e3-80ca-237b0b7049aa)

## Number of Goroutines   

*cosmos_runtime_num_goroutines*  

Indicates the number of goroutines running. Reflects the number of concurrent tasks active on the system, providing a view of concurrency.  
Value: number of goroutines in execution.  
![image](https://github.com/user-attachments/assets/a8d33ddf-e504-4fd8-8391-7f39d06e4bd4)

## System Bytes 

*cosmos_runtime_sys_bytes*  

Displays the total amount of memory allocated by the system. Reflects the total memory in use by runtime and other system resources. 
Value: memory allocated by the system.  
![image](https://github.com/user-attachments/assets/697ebac6-6d9b-46af-adaf-2e0db05007d9)

## Process Memory in Use  

*cosmos_runtime_alloc_bytes*  
![image](https://github.com/user-attachments/assets/2ea5b809-71d2-42b3-ab57-fc5952f9401c)  

______________________________________________________________________-

# Consensus & Validator Metrics

This section documents the main **consensus health** and **validator performance** metrics exposed by Story nodes and visualized in Grafana.

---

## Precommits Counted

**Metric name:**  
`cometbft_consensus_precommits_counted`

**Description:**  
Total number of precommit votes processed by the consensus engine.

This metric reflects the volume of precommit messages successfully handled during consensus rounds. It provides a low-level view of consensus activity and message throughput.

**PromQL example:**
```promql
rate(cometbft_consensus_precommits_counted{job="$job"}[5m])
```

---

## Blocks Proposed (24h)

**Metric name:**  
`cometbft_consensus_proposal_create_count`

**Description:**  
Number of blocks proposed by this node during the last 24 hours.

This metric counts how often the node acted as a block proposer within the network.

**PromQL:**
```promql
increase(cometbft_consensus_proposal_create_count{job="$job"}[24h])
```

---


## Consensus Voting Power Participation (%)

**Metric name:**  
`cometbft_consensus_round_voting_power_percent`

**Description:**  
Percentage of total network voting power participating in consensus rounds, measured separately for **prevote** and **precommit** phases.

The metric is reported on a **0–1 scale** and displayed as a percentage.

**PromQL:**
```promql
max by (vote_type) (
  avg_over_time(cometbft_consensus_round_voting_power_percent{job="$job"}[10m])
)
```

---



## Validator Last Signed Height

**Metric name:**  
`cometbft_consensus_validator_last_signed_height`

**Description:**  
Block height of the most recent block signed by the validator.

**PromQL:**
```promql
max(cometbft_consensus_validator_last_signed_height{job="$job"})
```

---

## Missed Blocks (last 24h)

**Metric name:**  
`cometbft_consensus_validator_missed_blocks`

**Description:**  
Number of blocks missed by the validator over a given time window.

**PromQL:**
```promql
increase(
  cometbft_consensus_validator_missed_blocks{job="$job"}[24h]
)
```

---

## Consensus Health (Rounds & Timing)

This group of metrics provides insight into **consensus efficiency, latency, and stability**.

---

### Round Duration (avg / p95)

**Metric name:**  
`cometbft_consensus_round_duration_seconds`

**Description:**  
Measures the time required to complete consensus rounds in CometBFT.

A consensus round includes the proposal, prevote, and precommit phases required to finalize a block.  
The average value represents typical round duration, while the p95 highlights slow or problematic rounds.

Increased round durations usually indicate network latency, delayed validator participation, or multiple round retries.


**PromQL (avg):**
```promql
sum(rate(cometbft_consensus_round_duration_seconds_sum{job="$job"}[5m]))
/
sum(rate(cometbft_consensus_round_duration_seconds_count{job="$job"}[5m]))
```

**PromQL (p95):**
```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(cometbft_consensus_round_duration_seconds_bucket{job="$job"}[5m])
  )
)
```

---

### Block Interval (avg / p95)

**Metric name:**  
`cometbft_consensus_block_interval_seconds`

**Description:**  
Time interval between consecutive blocks.

**PromQL (avg):**
```promql
sum(rate(cometbft_consensus_block_interval_seconds_sum{job="$job"}[5m]))
/
sum(rate(cometbft_consensus_block_interval_seconds_count{job="$job"}[5m]))
```

**PromQL (p95):**
```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(cometbft_consensus_block_interval_seconds_bucket{job="$job"}[5m])
  )
)
```

This metric indicates how many bytes of memory the process is currently using. It is essential for monitoring the node's memory usage, as a significant increase could affect its performance and stability. The metric helps to detect potential problems related to memory management, which can lead to optimisation of system resource usage.  
Value: amount of memory allocated and still in use in the process.  


