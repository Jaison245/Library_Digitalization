# DO NOT MODIFY THIS FILE

# primes in descending order
prime_sizes = [29]

def set_primes(list_of_primes):
    global prime_sizes
    prime_sizes = list_of_primes
    
def get_next_size():
    return prime_sizes.pop()
        
# Whenever you need to rehash, call get_next_size() to get the new table size
















# from prime_generator import get_next_size

# class HashTable:
#     def __init__(self, collision_type, params):
#         '''
#         Possible collision_type:
#             "Chain"     : Use hashing with chaining
#             "Linear"    : Use hashing with linear probing
#             "Double"    : Use double hashing
#         '''
#         self.collision_type = collision_type
#         self.count = 0  # number of items in the hashtable (for load factor calculations)

#         if collision_type in ["Chain", "Linear"]:
#             self.z = params[0]
#             self.table_size = params[1]
#         else:  # Double hashing
#             self.z1 = params[0]
#             self.z2 = params[1]
#             self.c2 = params[2]
#             self.table_size = params[3]

#         # Initialize table based on collision type
#         if collision_type == "Chain":
#             self.table = [[] for _ in range(self.table_size)]
#         else:
#             self.table = [None] * self.table_size
    
#     def char_to_value(self, char):
#         """ Map each character to its corresponding value. """
#         if 'a' <= char <= 'z':
#             return ord(char) - ord('a')  # p(a) : 0, p(b) : 1, ..., p(z) : 25
#         elif 'A' <= char <= 'Z':
#             return ord(char) - ord('A') + 26  # p(A) : 26, p(B) : 27, ..., p(Z) : 51
#         return -1  # Non-alphabetic characters are not valid for hashing

#     def hash_function(self, key):
#         if isinstance(key, str):
#             hash_val = 0
#             for i, char in enumerate(key):
#                 value = self.char_to_value(char)
#                 if value == -1:
#                     continue  # Ignore non-alphabetic characters
#                 hash_val = (hash_val + value * (self.z ** i)) % self.table_size
#             return hash_val
#         return key % self.table_size
    
#     def second_hash(self, key):
#         if isinstance(key, str):
#             hash_val = 0
#             for i, char in enumerate(key):
#                 value = self.char_to_value(char)
#                 if value == -1:
#                     continue  # Ignore non-alphabetic characters
#                 hash_val = (hash_val + value * (self.z2 ** i)) % self.c2
#             return hash_val
#         return key % self.c2
    
#     def get_slot(self, key):
#         initial_hash = self.hash_function(key)
        
#         if self.collision_type == "Chain":
#             return initial_hash
#         elif self.collision_type == "Linear":
#             i = 0
#             while i < self.table_size:
#                 slot = (initial_hash + i) % self.table_size
#                 if self.table[slot] is None or self.table[slot] == key:
#                     return slot
#                 i += 1
#         else:  # Double hashing
#             step = self.second_hash(key)
#             i = 0
#             while i < self.table_size:
#                 slot = (initial_hash + i * step) % self.table_size
#                 if self.table[slot] is None or self.table[slot] == key:
#                     return slot
#                 i += 1
#         return None
    
#     def get_load(self):
#         return self.count / self.table_size
    
#     def __str__(self):
#         return str(self.table)

# class HashSet(HashTable):
#     def __init__(self, collision_type, params):
#         super().__init__(collision_type, params)
    
#     def insert(self, key):
#         if self.collision_type == "Chain":
#             slot = self.get_slot(key)
#             if key not in self.table[slot]:
#                 self.table[slot].append(key)
#                 self.count += 1
#         else:
#             slot = self.get_slot(key)
#             if slot is not None and self.table[slot] is None:
#                 self.table[slot] = key
#                 self.count += 1
    
#     def find(self, key):
#         if self.collision_type == "Chain":
#             slot = self.get_slot(key)
#             return key in self.table[slot]
#         else:
#             slot = self.get_slot(key)
#             return slot is not None and self.table[slot] == key
    
#     def get_slot(self, key):
#         return super().get_slot(key)
    
#     def get_load(self):
#         return super().get_load()
    
#     def __str__(self):
#         return super().__str__()

# class HashMap(HashTable):
#     def __init__(self, collision_type, params):
#         super().__ 