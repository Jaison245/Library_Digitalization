from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
            Initialize the hash table.

            Parameters:
            collision_type: str
            Possible values are "Chain" for chaining, "Linear" for linear probing, 
                and "Double" for double hashing.
            params: tuple
                Contains initial parameters for the hash table.
                params[0] -> z (base for polynomial hashing)
                params[1] -> table_size (should be prime)
                params[2] -> c2 (optional parameter for double hashing)
                params[3] -> z2 (base for secondary polynomial hashing, if needed)
        '''
        # Store the type of collision resolution method to be used
        self.collision_type = collision_type
        # Store the parameters for the hash table initialization
        self.params = params

        #Case-1 Collision type is Linear or chain
        if collision_type == "Chain" or collision_type == "Linear":
            self.z= params[0]
            self.table_size= params[1]
            self.table= [None]*self.table_size
        #Collision type is Linear or Double   
        elif collision_type == "Double":
            self.z1= params[0]
            self.z2= params[1]
            self.c2= params[2]
            self.table_size= params[3]
            self.table= [None]*self.table_size
        self.word_count=0
        pass
        
    def char_to_number(self, char):
        ''' Maps Latin letters to numbers as specified. '''
        #lower case
        if 'a' <= char <= 'z':
            return ord(char) - ord('a')
        #Upper case
        elif 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 26
        else:
            raise ValueError("Unsupported character for hashing")

# Check**
    def polynomial_hash(self, key, base, mod):
        ''' Computes polynomial hash of a string key with base and modulus. '''
        hash_value = 0
        # Iterate over each character in the key along with its index
        for i, char in enumerate(key):
            # Update hash_value using the character's numeric value and the current base raised to the index
            hash_value += self.char_to_number(char) * (base ** i)
        return hash_value % mod

    def get_slot(self, key):
        '''
        Returns the slot and step size for a given key using polynomial accumulation hashing.
        
        Parameters:
        key: str
            The key for which the slot is calculated.
        
        Returns:
        Tuple[int, int]: primary hash (slot) and secondary hash (step size if needed).
        '''
        # Primary hash for the slot
        if(self.collision_type=="Chain" or self.collision_type =="Linear"):
            # Compute primary hash using the first polynomial hash parameters
            primary_hash = self.polynomial_hash(key, self.z, self.table_size)
        elif self.collision_type=="Double":
            # Compute primary hash using the first polynomial hash parameters
            primary_hash= self.polynomial_hash(key, self.z1, self.table_size)        
        # Secondary hash for double hashing (if needed)
        secondary_hash = None # Initialize secondary hash to None; it will be computed if double hashing is used
        if self.collision_type == "Double" and self.z2 is not None and self.c2 is not None:
            # Compute secondary hash based on the second polynomial hash and step size
            secondary_hash = self.c2 - (self.polynomial_hash(key, self.z2, self.c2) % self.c2)

        # return primary_hash
        return primary_hash
    

    def insert(self, x):
        keySlot = self.get_slot(x) # Determine the primary slot for the key using the hashing function
        # CASE 1: Collision resolution using Chaining
        if self.collision_type == "Chain":
            if self.table[keySlot] is None: # Initialize a new list at the given slot as it is empty
                self.table[keySlot] = []
            # Only insert if the item is not already in the list at the slot
            if x not in self.table[keySlot]:
                self.word_count += 1
                self.table[keySlot].append(x)

        # CASE 2 Collision resolution using Linear Probing
        elif self.collision_type == "Linear":
            i = 0 # Initialize probe count
            current_slot = keySlot # Start at the calculated primary slot
            # Check for duplicates while probing
            while self.table[current_slot] is not None:
                if self.table[current_slot] == x:  # Found duplicate
                    return # Exit if duplicate found
                # Calculate the next slot using linear probing
                current_slot = (keySlot + i) % self.table_size
                i += 1
                if current_slot == keySlot: 
                    break
                    
            slot = keySlot
            i = 0
            while self.table[slot] is not None and i<self.table_size:
                slot = (keySlot + i) % self.table_size
                i += 1
            if self.table[slot] is None:
                self.word_count += 1
                self.table[slot] = x
        # CASE 3 Collision resolution using Double Hashing
        elif self.collision_type == "Double":
            i = 1 # Initialize probe count for double hashing
            current_slot = keySlot # Start at the calculated primary slot
            # Calculate step size for double hashing
            step_size = self.c2 - (self.polynomial_hash(x, self.z2, self.c2))
            # Check for duplicates while probing
            while self.table[current_slot] is not None and i<self.table_size:
                if self.table[current_slot] == x: 
                    return
                # Calculate the next slot using double hashing
                current_slot = (keySlot + i * step_size) % self.table_size
                i += 1
                if current_slot == keySlot: 
                    break
                    
            slot = keySlot
            i = 0
            while self.table[slot] is not None and i<self.table_size:
                slot = (keySlot + i * step_size) % self.table_size
                i += 1
             # If an empty slot is found, insert the item    
            if self.table[slot] is None:
                self.table[slot] = x
                self.word_count += 1

    def find(self, key):
        # Calculate the initial slot for the key using the hashing function
        slot = self.get_slot(key) 
        # CASE 1: Searching with Chaining
        if self.collision_type == "Chain":
            # Retrieve the list at the calculated slot
            list = self.table[slot]
            if list is None:
                return False
            for entry in list:
                if entry == key:
                    return True
            return False
        # CASE 2: Searching with Linear Probing
        elif self.collision_type == "Linear":
            # Search for the key using linear probing
            i = 0
            while self.table[(slot + i) % self.table_size] is not None: # Continue until an empty slot is found
                if self.table[(slot + i) % self.table_size] == key:
                    return True
                i += 1
            return False
        # CASE 3: Searching with Double Hashing
        elif self.collision_type == "Double":
            # Calculate the step size for probing
            step_size = self.c2 - (self.polynomial_hash(key, self.z2, self.c2))
            i=0
            original_slot= slot # Store the original slot for loop control
            while i<self.table_size and self.table[slot] is not None:
                if self.table[slot] == key: #Found key
                    return True
                # Calculate the next slot to check using the step size
                slot = (original_slot + i*step_size)%self.table_size
                i+=1
            return False

    def get_load(self):
        # Calculate the load factor of the hash table
        return self.word_count / self.table_size

    def __str__(self):
        sentence = [] # Initialize an empty list to store string representations of each slot in the hash table
        # Iterate through each slot (tup) in the hash table
        for tup in self.table:
            if tup is None: # If slot in table is empty
                sentence.append("<EMPTY>")
            elif isinstance(tup, list): # If the slot contains a list (for chaining)
                # Initialize a list to hold the string representations of the entries
                outputList = []
                for entry in tup: # Iterate through each entry in the list
                    if isinstance(entry, tuple):  # Check if the entry is a tuple
                        outputList.append(f"({entry[0]}, {entry[1]})") # Format the tuple as a string
                    else:
                        outputList.append(str(entry))
                sentence.append(" ; ".join(outputList))
            elif isinstance(tup, tuple): # If the slot contains a single tuple
                sentence.append(f"({tup[0]}, {tup[1]})")
            else: # If the slot contains a single value (not a tuple or list)
                sentence.append(str(tup))
        # Final output
        return " | ".join(sentence)

    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        # Determine the next size for the hash table using a helper function
        nextTableSize = get_next_size(self.table_size)
        # Create a copy of the current table to rehash the elements
        oldTable = [i for i in self.table]
        
        # Updating the values here
        self.table = [None] * nextTableSize #updating the table, table_size and word count
        self.table_size = nextTableSize # Update the table size to the new size
        self.word_count = 0  # Reset the word count to 0 as we will reinsert the elements
        # Handle rehashing based on the collision resolution strategy
        if self.collision_type in ["Linear", "Double"]:
            for tup in oldTable:
                if tup is None: # Handling NoneType
                    continue
                self.insert(tup) # Reinsert the entry into the new table using the insert method
            
        elif self.collision_type == "Chain":
            for slot in oldTable:
                if slot is None: # Handling NoneType
                    continue
                # For each entry in the linked list at this slot, reinsert it into the new table
                for tup in slot:
                    self.insert(tup) # Reinsert the entry into the new table

class HashSet(HashTable):
    def __init__(self, collision_type, params):
        # Initialize the hash set using the HashTable constructor
        super().__init__(collision_type, params)

    def insert(self, key):
        # Insert a key into the hash set
        super().insert(key)

    def find(self, key):
        # Find a key in the hash set
        return super().find(key)

    def get_slot(self, key):
        # Get the initial slot for the key
        return super().get_slot(key)

    def get_load(self):
        # Get the load factor of the hash set
        return super().get_load()

    def __str__(self):
        # String representation of the hash set
        return super().__str__()

class HashMap(HashTable):
    def _init_(self, collision_type, params):
        # Initialize the hash map using the HashTable constructor
        super().__init__(collision_type, params)

    def insert(self, key):
        key1=key[0] # Extract the key for hashing (assuming key[0] holds the unique identifier)
        # Get the slot using the primary hashing function
        slot = self.get_slot(key1)
        # Case 1: Chaining for collision resolution
        if self.collision_type == "Chain":
            # Check if the key already exists in the hash table
            if self.find(key1) == None or self.find(key1) == False:
                if self.table[slot] is None: #Initializing the list at this slot with [key]
                    self.table[slot] = [key]
                else:
                    self.table[slot].append(key) #Appending the key to the already existing list
            self.word_count += 1
        # Case 2: Linear probing for collision resolution
        elif self.collision_type == "Linear":
            c=0
            # Continue probing until an empty slot is found or we find the key1 already in the table
            while c< self.table_size and self.table[slot] is not None and self.table[slot][0] != key1: # Keep checking the next slots until we find a free one or we find the key1
                slot = (slot + 1) % self.table_size
                c +=1
            #Incremented word count only if the slot was free
            if self.table[slot] is None:
                self.word_count += 1
            #Updating or filling the slot with new value key
            self.table[slot] = key
        # Case 3: Double hashing for collision resolution
        elif self.collision_type == "Double":
            step_size = self.c2 - (self.polynomial_hash(key1, self.z2, self.c2))
            ind = 0
            curr_slot= slot
            # Continue probing until an empty slot is found or we find the key1 already in the table
            while ind < self.table_size and self.table[curr_slot] is not None and self.table[curr_slot][0] != key1:
                curr_slot = (curr_slot + ind * step_size) % self.table_size
                ind += 1
            #Incremented word count only if the curr_slot was free
            if self.table[curr_slot] is None:
                self.word_count += 1
            #Updating or filling the curr_slot with new value key
            self.table[curr_slot] = key

    def find(self, key):
        '''
        Find a value by key in the hash map.
        Parameters:
        key: int
            The key to be found.
        Returns:
        The value associated with the key if found, otherwise None.
        '''
        # Get the initial slot for the key using the hash function
        slot = self.get_slot(key)
        # Case 1: If using chaining for collision handling
        if self.collision_type == "Chain":
            # Retrieve the list at the computed slot
            list = self.table[slot]
            if list is None:
                return None
            # Iterate over the entries in the list to find the key
            for tup in list:
                # Check if the first element of each tuple (assumed to be the key) matches the search key
                if tup[0] == key:
                    return tup[1]
            return None
        # Case 2: If using linear probing for collision handling
        elif self.collision_type == "Linear":
            i = 0 # Initialize the probing index
            # Loop until an empty slot is encountered, meaning the key is not in the table
            while self.table[(slot + i) % self.table_size] is not None:
                # Check if the first element of the tuple matches the search key
                if self.table[(slot + i) % self.table_size][0] == key:
                    # Return the associated value if the key is found
                    return self.table[(slot + i) % self.table_size][1]  # Return the associated value
                i += 1
            return None  # Return None if not found
        # Case 3: If using double hashing for collision handling
        elif self.collision_type == "Double":
            # Calculate the step size for double hashing
            step_size = self.c2 - (self.polynomial_hash(key, self.z2, self.c2))
            i = 0 # Initialize the probing index
            # Loop until an empty slot is encountered, meaning the key is not in the table
            while self.table[slot] is not None:
                # Check if the first element of the tuple matches the search key
                if self.table[slot][0] == key:
                    return self.table[slot][1]
                # Move to the next slot based on the step size in double hashing
                slot = (slot + i * step_size) % self.table_size
                i += 1
            return None
        
    def get_slot(self, key):   
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        return super().__str__()
    
