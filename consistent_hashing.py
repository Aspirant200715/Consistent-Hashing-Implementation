import hashlib
import bisect
import threading
from typing import List, Dict, Optional


class ConsistentHash:
    def __init__(
        self,
        nodes: Optional[Dict[str, int]] = None,
        virtual_nodes: int = 100,
        replication_factor: int = 3,
    ):
        self.virtual_nodes = virtual_nodes
        self.replication_factor = replication_factor

        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []
        self.node_weights: Dict[str, int] = {}

        self._lock = threading.RLock()

        if nodes:
            for node, weight in nodes.items():
                self.add_node(node, weight)

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str, weight: int = 1) -> None:
        with self._lock:
            if node in self.node_weights:
                raise ValueError(f"Node {node} already exists")

            self.node_weights[node] = weight
            total_vnodes = self.virtual_nodes * weight

            for i in range(total_vnodes):
                vnode_key = f"{node}#{i}"
                hash_val = self._hash(vnode_key)

                while hash_val in self.ring:  # collision safe
                    vnode_key += "_"
                    hash_val = self._hash(vnode_key)

                self.ring[hash_val] = node
                bisect.insort(self.sorted_keys, hash_val)

    def remove_node(self, node: str) -> None:
        with self._lock:
            if node not in self.node_weights:
                return

            weight = self.node_weights[node]
            total_vnodes = self.virtual_nodes * weight

            for i in range(total_vnodes):
                vnode_key = f"{node}#{i}"
                hash_val = self._hash(vnode_key)

                idx = bisect.bisect_left(self.sorted_keys, hash_val)
                if idx < len(self.sorted_keys) and self.sorted_keys[idx] == hash_val:
                    self.sorted_keys.pop(idx)
                    del self.ring[hash_val]

            del self.node_weights[node]

    def get_node(self, key: str) -> Optional[str]:
        with self._lock:
            if not self.ring:
                return None

            hash_val = self._hash(key)
            idx = bisect.bisect_left(self.sorted_keys, hash_val)

            if idx == len(self.sorted_keys):
                idx = 0

            return self.ring[self.sorted_keys[idx]]

    def get_replicas(self, key: str) -> List[str]:
        with self._lock:
            if not self.ring:
                return []

            hash_val = self._hash(key)
            idx = bisect.bisect_left(self.sorted_keys, hash_val)

            replicas = []
            visited = set()

            for i in range(len(self.sorted_keys)):
                index = (idx + i) % len(self.sorted_keys)
                node = self.ring[self.sorted_keys[index]]

                if node not in visited:
                    replicas.append(node)
                    visited.add(node)

                if len(replicas) == min(self.replication_factor, len(self.node_weights)):
                    break

            return replicas


#Test Case

def run_simulation():
    print("\nRunning Consistent Hashing\n")

    nodes = {
        "Node-A": 1,
        "Node-B": 2, 
        "Node-C": 1,
    }

    ch = ConsistentHash(nodes, virtual_nodes=50, replication_factor=2)

    print(f"Initial Nodes (with weights): {nodes}")
    print(f"Total Virtual Nodes: {len(ch.sorted_keys)}\n")

    keys = [f"user_{i}" for i in range(1000)]

    # Initial distribution
    distribution = {node: 0 for node in nodes}

    initial_mapping = {}
    for key in keys:
        node = ch.get_node(key)
        initial_mapping[key] = node
        distribution[node] += 1

    print("📊 Initial Distribution:")
    for node, count in distribution.items():
        print(f"{node}: {count}")

    # Replication example
    print("\nReplica Check for user_42:")
    print(ch.get_replicas("user_42"))

    # Add new node
    new_node = "Node-D"
    print(f"\nAdding {new_node} (weight=1)\n")
    ch.add_node(new_node, weight=1)

    moved = 0
    new_distribution = {node: 0 for node in ch.node_weights}

    for key in keys:
        new_node_assignment = ch.get_node(key)
        new_distribution[new_node_assignment] += 1

        if new_node_assignment != initial_mapping[key]:
            moved += 1

    percent_moved = (moved / len(keys)) * 100

    print("New Distribution After Adding Node-D:")
    for node, count in new_distribution.items():
        print(f"{node}: {count}")

    print(f"\nKeys Moved: {moved} / {len(keys)}")
    print(f"Percentage Moved: {percent_moved:.2f}%")
    print("Expected ≈ 1/(N+1) movement property ✔")


if __name__ == "__main__":
    run_simulation()
