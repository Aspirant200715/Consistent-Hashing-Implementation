# Hashing Algorithms Comparison Report

## 1. Introduction
In distributed systems (like caching clusters or sharded databases), mapping data keys to specific nodes is critical. This report compares two approaches: **Modulo Hashing** and **Consistent Hashing**, implemented in this repository.

## 2. Modulo Hashing
**File:** `modulo_hashing.py`

### Mechanism
The node for a given key is determined by the formula:
`index = hash(key) % number_of_nodes`

### Observations
- **Simplicity**: Very easy to implement.
- **Distribution**: Uniform distribution depends entirely on the hash function quality.
- **Scalability Issue**: When the number of nodes (`N`) changes (e.g., adding a node), the divisor changes. This alters the result for almost every key.
- **Simulation Result**: In the provided script, adding `Node-D` (going from 3 to 4 nodes) typically causes ~75% of keys to move. Theoretically, `(N-1)/N` keys are remapped.

## 3. Consistent Hashing
**File:** `consistent_hashing.py`

### Mechanism
- **Hash Ring**: Both nodes and keys are hashed onto a circular space (e.g., 0 to $2^{128}-1$).
- **Placement**: A key is assigned to the first node found moving clockwise on the ring.
- **Virtual Nodes**: To ensure uniform distribution and handle heterogeneity, each physical node is mapped to multiple points on the ring ("virtual nodes").

### Observations
- **Minimal Movement**: When a node is added, it only takes keys from its immediate neighbor on the ring. Existing keys mapped to other nodes remain untouched.
- **Weighted Distribution**: `Node-B` was assigned `weight=2`, resulting in it owning a larger portion of the ring and receiving more traffic, which is useful for heterogeneous hardware.
- **Replication**: The implementation supports `get_replicas`, allowing data to be stored on the primary node and the next $k$ distinct nodes on the ring.
- **Simulation Result**: Adding `Node-D` resulted in only a small fraction of keys moving (approx `1/(N+1)`), drastically reducing network overhead during scaling.

## 4. Time Complexity Analysis

### Modulo Hashing
- **Lookup (`get_node`)**: $O(1)$ — Direct calculation using hash and modulo.
- **Add/Remove Node**: $O(N)$ — Simple list manipulation (checking for existence and appending).

### Consistent Hashing
- **Lookup (`get_node`)**: $O(\log V)$ — Requires a binary search on the ring, where $V$ is the total number of virtual nodes.
- **Add/Remove Node**: $O(K \cdot V)$ — Adding a node involves inserting $K$ virtual nodes into the sorted ring structure (where insertion is linear in $V$).

*Note: $N = \text{Physical Nodes}$, $K = \text{Virtual Nodes per Node}$, $V = \text{Total Virtual Nodes}$.*

## 5. Comparison Summary

| Feature | Modulo Hashing | Consistent Hashing |
| :--- | :--- | :--- |
| **Mapping** | `hash % N` | Ring topology + Binary Search |
| **Scalability** | Poor (Massive reshuffling) | Excellent (Minimal reshuffling) |
| **Load Balancing** | Depends on Hash | Tunable via Virtual Nodes |
| **Complexity** | Low | Moderate |
| **Heterogeneity** | Hard to handle | Native support via Weights |
| **Lookup Time** | $O(1)$ | $O(\log V)$ |

## 6. Conclusion
While Modulo Hashing is sufficient for static sets of nodes, **Consistent Hashing** is the superior choice for dynamic distributed systems. It minimizes the cost of rebalancing and supports advanced features like weighted distribution and replication, as demonstrated in `consistent_hashing.py`.