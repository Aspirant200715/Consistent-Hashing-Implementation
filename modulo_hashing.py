import hashlib
from typing import List, Dict

class ModuloHash:
    """
    Implements traditional Modulo Hashing: index = hash(key) % N
    """
    def __init__(self, nodes: List[str] = None):
        self.nodes = nodes if nodes else []          

    def add_node(self, node: str) -> None:
        if node not in self.nodes:
            self.nodes.append(node)

    def remove_node(self, node: str) -> None:
        if node in self.nodes:
            self.nodes.remove(node)

    def get_node(self, key: str) -> str:
        """Formula: hash(key) % number_of_nodes"""
        if not self.nodes:
            return None
        #MD5 to ensure the same key always yields the same integer,
        hash_object = hashlib.md5(key.encode('utf-8'))
        hash_int = int(hash_object.hexdigest(), 16)
        node_index = hash_int % len(self.nodes)
        return self.nodes[node_index]

def run_simulation():
    print("Running Modulo Hashing Simulation")

    nodes = ["Node-A", "Node-B", "Node-C"]
    hasher = ModuloHash(list(nodes))                # Pass a copy
    print(f"Initial Nodes ({len(nodes)}): {nodes}")

    keys = [f"user_{i}" for i in range(20)]         #Dummy user ids (hardcoded 20 user ids)

    initial_mapping: Dict[str, str] = {}
    for k in keys:
        initial_mapping[k] = hasher.get_node(k)     
    
    print("\nInitial Distribution")
    for k, v in initial_mapping.items():
        print(f"{k} -> {v}")

    new_node = "Node-D"
    print(f"\n--- Adding {new_node} ---")
    hasher.add_node(new_node)
    print(f"New Node List: {hasher.nodes}")

    #Key remapping
    new_mapping: Dict[str, str] = {}
    moved_keys = 0
    
    print("\nKey Migration")
    for k in keys:
        new_node_assignment = hasher.get_node(k)
        new_mapping[k] = new_node_assignment
        
        previous_node = initial_mapping[k]
        
        if new_node_assignment != previous_node:
            moved_keys += 1
            print(f"Key [{k}] moved from {previous_node} -> {new_node_assignment}")
        else:
            print(f"Key [{k}] stayed on {previous_node}")
            pass

   
#Test case 
    total_keys = len(keys)
    percent_moved = (moved_keys / total_keys) * 100

    print(f"\nMovement Statistics")
    print(f"Total Keys: {total_keys}")
    print(f"Moved Keys: {moved_keys}")
    print(f"Actual Movement: {percent_moved:.2f}%")

    old_n = len(nodes)           # original node count (before scaling)
    new_n = len(hasher.nodes)    # new node count (after scaling)
    expected_movement = (old_n / new_n) * 100
    deviation = abs(percent_moved - expected_movement)
    print(f"\nOld Nodes (N): {old_n}")
    print(f"New Nodes (N+1): {new_n}")
    print(f"Expected Movement (Theoretical): ~{expected_movement:.2f}%")
    print(f"Deviation from Theory: {deviation:.2f}%")


if __name__ == "__main__":
    run_simulation()