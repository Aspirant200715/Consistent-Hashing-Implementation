# Consistent-Hashing-Implementation

This repository contains implementations of two hashing strategies used in distributed systems: **Modulo Hashing** and **Consistent Hashing**. The project demonstrates the impact of adding or removing nodes on key distribution and migration.

## Files

- `modulo_hashing.py`: Implements the traditional `hash(key) % N` approach.
- `consistent_hashing.py`: Implements Consistent Hashing using a hash ring, virtual nodes, and weighted distribution.
- `report.md`: A detailed comparison and analysis of the two algorithms based on the simulations.

## How to Run

Ensure you have Python 3 installed. No external dependencies are required as the scripts use standard libraries (`hashlib`, `bisect`, `threading`).

### 1. Run Modulo Hashing Simulation
```bash
python modulo_hashing.py
```
Observe how adding a single node causes a large percentage of keys to move.

### 2. Run Consistent Hashing Simulation
```bash
python consistent_hashing.py
```
Observe how adding a node results in minimal key movement, preserving the mapping for most keys.

## Features Implemented

### Consistent Hashing
1.  **Ring Topology**: Maps nodes and keys to a common hash space.
2.  **Virtual Nodes**: Improves load balancing by assigning multiple positions on the ring to a single physical node.
3.  **Weighted Nodes**: Allows nodes with higher capacity to handle more keys (e.g., `Node-B` has weight 2).
4.  **Replication**: Supports finding `N` unique replicas for a given key for fault tolerance.
5.  **Thread Safety**: Uses `threading.RLock` for concurrent access safety.

## Comparison

For a detailed analysis of the results and theoretical differences, please refer to report.md.

## Objectives Met
1. Distributes keys uniformly across nodes.
2. Minimizes key movement during node addition/removal.
3. Supports deterministic lookup.
4. Handles node rebalancing efficiently.
5. Virtual Nodes creation and distribution.
