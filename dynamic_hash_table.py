from prime_generator import get_next_size
from hash_table import HashSet, HashMap

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        # Get a new size for the hash table, ideally a prime larger than the current size
        nextTableSize = get_next_size()
        # Copy current table contents to an auxiliary list
        oldTable = self.table.copy()
        
        # Reinitialize the hash table with the new size and reset word count
        self.table = [None] * nextTableSize
        self.table_size = nextTableSize
        self.word_count = 0 

        # Reinsert all elements from old table into the new table, respecting collision handling method
        if self.collision_type in ["Linear", "Double"]:
            for item in oldTable:
                if item is not None:
                    # Use the parent's insert method to handle reinsertion based on collision strategy
                    super().insert(item)
        elif self.collision_type == "Chain":
            for slot in oldTable:
                if slot is not None:
                    # For chaining, each slot is a list of items, so iterate through and reinsert each
                    for item in slot:
                        super().insert(item)
            
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()

    def __str__(self):
        return super().__str__()


class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        super().rehash()
    
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        # hi all
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()

    def __str__(self):
        return super().__str__()
