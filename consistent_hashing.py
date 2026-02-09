import hashlib
import bisect
from typing import List, Dict

class ConsistentHash:
    def __init__(self, nodes: List[str] = None, virtual_nodes: int = 100):

        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}
        self.vnode_map: Dict[int, str] = {}
        self.sorted_keys: List[int] = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        for i in range(self.virtual_nodes):
            vnode_key = f"{node}#{i}"
            
            hash_val = self._hash(vnode_key)
            
            self.ring[hash_val] = node
            self.vnode_map[hash_val] = vnode_key
            bisect.insort(self.sorted_keys, hash_val)   #binary search algorithm

    def remove_node(self, node: str) -> None:
        for i in range(self.virtual_nodes):
            vnode_key = f"{node}#{i}"
            hash_val = self._hash(vnode_key)
            
            if hash_val in self.ring:
                del self.ring[hash_val]
            if hash_val in self.vnode_map:
                del self.vnode_map[hash_val]
            
            if hash_val in self.sorted_keys:
                self.sorted_keys.remove(hash_val)

    def get_node(self, key: str) -> str:
        """
        Finds the node responsible for a given key using Clockwise logic.
        O(log V) where V is total virtual nodes.
        """
        if not self.ring:
            return None 
        hash_val = self._hash(key)
        idx = bisect.bisect_left(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys):
            idx = 0    
        target_hash = self.sorted_keys[idx]
        
        return self.ring[target_hash]

    def get_node_with_vnode(self, key: str) -> tuple:

        if not self.ring: return None, None
        hash_val = self._hash(key)
        idx = bisect.bisect_left(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys): idx = 0
        target_hash = self.sorted_keys[idx]
        return self.ring[target_hash], self.vnode_map[target_hash]

def run_simulation():
    print("Running Consistent Hashing")
    nodes = ["Node-A", "Node-B", "Node-C"]
    ch = ConsistentHash(nodes, virtual_nodes=10)
    print(f"Initial Nodes: {nodes}")

    keys = [f"user_{i}" for i in range(20)]
    
    initial_mapping: Dict[str, str] = {}
    for k in keys:
        initial_mapping[k] = ch.get_node(k)
        
    print("\nInitial Distribution")
    counts = {n: 0 for n in nodes}
    for k, v in initial_mapping.items():
        counts[v] += 1
        print(f"{k} -> {v}")
    print(f"Distribution counts: {counts}")
    
    print("\nVirtual Nodes (Load Balancing)")
    for k in keys[:5]: # Check first 5 keys
        p_node, v_node = ch.get_node_with_vnode(k)
        print(f"Key [{k}] routed to Physical [{p_node}] via Virtual [{v_node}]")
    
    new_node = "Node-D"
    print(f"\n--- Adding {new_node} ---")
    ch.add_node(new_node)

    moved_keys = 0
    print("\nKey Migrations")
    for k in keys:
        new_node_assignment = ch.get_node(k)
        previous_node = initial_mapping[k]
        
        if new_node_assignment != previous_node:
            moved_keys += 1
            print(f"Key [{k}] moved from {previous_node} -> {new_node_assignment}")
    
    total_keys = len(keys)
    percent_moved = (moved_keys / total_keys) * 100
    print(f"\nTotal Keys: {total_keys}")
    print(f"Moved Keys: {moved_keys}")
    print(f"Percentage Moved: {percent_moved:.2f}%")
    print(f"In Consistent Hashing, we expect ~1/(N+1) keys to move. 1/4 = 25%.")

if __name__ == "__main__":
    run_simulation()