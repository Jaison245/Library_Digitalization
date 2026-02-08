from hash_table import HashSet,HashMap 

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):

        #All the book Titles are stored 
        self.book_titles =[]

        #The text in each book is stored
        self.texts = []

        #stores tuples containing each book's index and title sorts the list of books by titles which is required while binary search.
        booksList = []

        for book_title in book_titles: #Each book title is added
            self.book_titles.append(book_title)

        for text in texts: #Each book text is added
            self.texts.append(text)

        length = len(book_titles) #total number of books

        #Generation of `booksList` with tuples of the form (index, title) for each book.
        for i in range(length):
            tup = [i, book_titles[i]]
            booksList.append(tup)
        # Sort `booksList` by titles using a custom merge sort, storing the result.
        # This is useful for binary searching books by title.    
        self.booksList = self.BooksMergeSort(booksList) 

        # Sort the words in each book’s text for efficient keyword searching later.
        # `texts` now holds a sorted list of words for each book. 
        length2 = len(texts)
        for j in range(length2):
            # For each word in the book’s text, a list of tuples is created,each containing the word and an empty string placeholder.
            lis1 = [[word, ''] for word in self.texts[j]]  
            # Sort the list of words in each text and keep only the words themselves.
            self.texts[j] = [tup[0] for tup in self.merge_sort(lis1)]  

    def BooksMerge(self, leftBooks, rightBooks):
        #An empty list is initialized to hold the merged and sorted books.
        soretedList = []

        #pointers for left and right sublists
        i = j = 0 #i is the left pointer
                  #j is the right pointer

        # Traverse both lists until one of them is exhausted.
        while i< len(leftBooks) and j < len(rightBooks):
            # The titles are extracted from the current elements in left and right lists.
            leftTitle= leftBooks[i][1]
            rightTitle = rightBooks[j][1]
            # If the title in the left list is lexicographically smaller, add it to the sorted list.
            if leftTitle < rightTitle:
                # Check if `soretedList` is empty or does not already have this title at the end.
                if not soretedList or soretedList[-1][1] != leftTitle:
                    soretedList.append(leftBooks[i])
                i+= 1 #traversal in the left list
            # If the title in the right list is lexicographically smaller, add it to the sorted list.    
            elif leftTitle > rightTitle:
                # Check if `soretedList` is empty or does not already have this title at the end.
                if not soretedList or soretedList[-1][1] != rightTitle:
                    soretedList.append(rightBooks[j])
                j += 1 #traversal in the right list
                # If titles are the same, add the book from the left list to avoid duplicates.
            else:  
                # Ensure `soretedList` does not already have this title at the end
                if not soretedList or soretedList[-1][1] != leftTitle:
                    soretedList.append(leftBooks[i])
                #traverse in both the lists to avoid duplicates    
                i+= 1
                j += 1
        # Append any remaining elements from the left list, ensuring no duplicates.        
        while i< len(leftBooks):
            if not soretedList or soretedList[-1][1] != leftBooks[i][1]:
                soretedList.append(leftBooks[i])
            i+= 1
        # Append any remaining elements from the right list, ensuring no duplicates.    
        while j < len(rightBooks):
            if not soretedList or soretedList[-1][1] != rightBooks[j][1]:
                soretedList.append(rightBooks[j])
            j += 1
        return soretedList

    def BooksMergeSort(self, arr):

        length= len(arr)
        #Base condition: if the array has one or no elements, it's already sorted
        if length <= 1:
            return arr
        #calculate the midpoint to divide the array into two parts(left and right)
        mid = (length//2)

        # Recursively apply merge sort to both the left and right parts.
        leftArr = self.BooksMergeSort(arr[:mid])
        rightArr = self.BooksMergeSort(arr[mid:])
        # Merge the two sorted halves.
        return self.BooksMerge(leftArr, rightArr)

    def merge(self, left, right):
        #An empty list is initialized to store the merged result
        mergedList = []

        i= j = 0 # Initialize pointers for left and right lists

        # Loop through both lists until one of them is exhausted
        while i < len(left) and j < len(right):
            # If elements in both lists are equal
            if left[i] == right[j]:
                # Add the element if mergedList is empty or doesn't contain this element at the end
                if not mergedList or mergedList[-1] != left[i]:
                    mergedList.append(left[i])
                # Move both pointers forward    
                i += 1
                j += 1
                # If the element in the left list is greater
            elif left[i] > right[j]:
                if not mergedList or mergedList[-1] != right[j]: # Append the smaller one to mergedList if it's not a duplicate of the last element
                    mergedList.append(right[j])
                j += 1
                # If the element in the left list is smaller
            elif left[i] < right[j]:
                if not mergedList or mergedList[-1] != left[i]: # Append the smaller one to mergedList if it's not a duplicate of the last element
                    mergedList.append(left[i])
                i += 1
        # Append any remaining elements in the left list, avoiding duplicates
        while i < len(left):
            if not mergedList or mergedList[-1] != left[i]:
                mergedList.append(left[i])
            i += 1
        # Append any remaining elements in the right list, avoiding duplicates
        while j < len(right):
            if not mergedList or mergedList[-1] != right[j]:
                mergedList.append(right[j])
            j += 1 
        return mergedList

    def merge_sort(self, arr):
        length= len(arr)
        # Base condition: If the array has 1 or 0 elements, it is already sorted
        if length <= 1:
            return arr
        #Calculate mid point to divide the array into two parts 
        mid = (length//2)
        #Apply merge sort recursively to both the left and right parts
        leftArr = self.merge_sort(arr[:mid])
        rightArr = self.merge_sort(arr[mid:])
        return self.merge(leftArr, rightArr)

    def binarySearchHelper(self,arr, x):
        # Initialize low (l) and high (h) indices for the search range
        l = 0
        h = len(arr)-1
        # Define a helper function to perform binary search recursively
        def helper(l, h):
            if h >= l:  # Base condition: search range is valid
                mid = ((h + l)//2)
                if arr[mid] == x: # Check if the middle element is the target element x
                    return mid
                elif arr[mid] < x: #If the middle element is less than x, search the right half
                    return helper(mid + 1, h)
                else:              # If the middle element is greater than x, search the left half
                    return helper(l, mid - 1)
            else:
                return -1       #if not present 
        return helper(l, h)
    
    def distinct_words(self, book_title):
        # Iterate through each tuple in the sorted list of books (booksList)
        for tup in self.booksList:
            # Check if the current book's title matches the specified book_title
            if tup[1] == book_title: #Match Found 
                ind = tup[0] #retrieve the index of the book
                return self.texts[ind]
        pass
    
    def count_distinct_words(self, book_title):
        # Iterate through each tuple in the sorted list of books (booksList)
        for tup in self.booksList:
            # Check if the current book's title matches the specified book_title
            if tup[1] == book_title: #match found
                ind = tup[0] #retrieve the index of the book
                return len(self.texts[ind])
        pass
    
    def search_keyword(self, keyword):
        # Initialize an empty list to store book titles containing the keyword
        booksWithKeyword = []
        length= len(self.booksList) # Get the total number of books in booksList
        # Loop through each book's information in booksList
        for ind in range(length):  
            index=self.booksList[ind][0]
            res = self.binarySearchHelper(self.texts[index], keyword) # Use binary search to check if the keyword exists in the list of distinct words for the current book
            if res != -1: # If binary search returns a non-negative result, the keyword was found in this book
                booksWithKeyword.append(self.booksList[ind][1]) # Append the title of the book containing the keyword to the result list
        return booksWithKeyword
      
    def print_books(self):
        for book in self.booksList: # Loop through each book in booksList to retrieve the title and index
            ind, book_title = book  # Unpack the index and title for the current book
            text = self.texts[ind]  # Retrieve the list of distinct words (text) associated with the book's index 
            output= f"{book_title}: " + " | ".join(x.strip() for x in text)
            print(output)
        pass

class JGBLibrary(DigitalLibrary):
    def __init__(self, name, params):
        self.name = name
        self.params = params
        # Check the name and set the collision type and hashmap accordingly
        if name == "Jobs":
            self.collision_type = "Chain"
            self.hashmap = HashMap(self.collision_type, params)
        elif name == "Gates":
            self.collision_type = "Linear"
            self.hashmap = HashMap(self.collision_type, params)
        elif name == "Bezos":
            self.collision_type = "Double"
            self.hashmap = HashMap(self.collision_type, params)
    
    def add_book(self, book_title, text):
        # Initialize a hash set based on the collision type for the specific name
        if self.name == "Jobs":
            self.collision_type = "Chain"
            self.hashset = HashSet(self.collision_type, self.params)
        elif self.name == "Gates":
            self.collision_type = "Linear"
            self.hashset = HashSet(self.collision_type, self.params)
        elif self.name == "Bezos":
            self.collision_type = "Double"
            self.hashset = HashSet(self.collision_type, self.params)
        for word in text: # Iterate over each word in the provided text
            self.hashset.insert(word) # Insert each word into the hash set
        tuple = [book_title, self.hashset]  # Create a tuple containing the book title and the associated hash set
        self.hashmap.insert(tuple) #the tuple is inserted into the hashmap

    def distinct_words(self, book_title):
        # We find the hash set associated with the given book title from the hashmap
        wordsInBook = self.hashmap.find(book_title)
        words = [] # Initialize an empty list to store distinct words
        # Check the collision resolution type for the hashmap
        if self.collision_type == "Linear" or self.collision_type == "Double":
            for item in wordsInBook.table:
                if item is None: # Skip any empty (None) entries in the hash table
                    continue
                words.append(item) # Append the non-empty item to the words list
        elif self.collision_type == "Chain":
            for lis in wordsInBook.table:
                if lis is None:
                    continue
                for j in lis:
                    words.append(j)
        return words # Return the list of distinct words found in the specified book

    def count_distinct_words(self, book_title):
        hashset = self.hashmap.find(book_title) # Retrieve the hash set associated with the given book title from the hashmap
        if hashset is None:
            return 0
        
        count = 0 # Initialize a counter for distinct words
        # Check the collision resolution type for the hashmap
        if self.collision_type == "Linear" or self.collision_type == "Double":
            for item in hashset.table:
                if item is not None: # Count non-empty entries in the table
                    count += 1
        
        elif self.collision_type == "Chain":
            for lis in hashset.table:
                if lis is None: #ignore the empty parts
                    continue
                count += len(lis) # Add the length of the linked list to the count (number of distinct words)
        return count

    def search_keyword(self, keyword):
        books_keywords = [] # Initialize an empty list to store book titles that contain the specified keyword
        # Check the collision resolution type for the hashmap
        if self.collision_type == "Linear" or self.collision_type == "Double":
            for tup in self.hashmap.table: # Iterate through the hash table
                if tup is None:  # TO remove 'NoneType' object as it is not iterable
                    continue
                book_title, hashset = tup # Unpack the tuple into book_title and hashset

                if hashset.find(keyword): # If found, add the book title to the list
                    books_keywords.append(book_title) 

        elif self.collision_type == "Chain":
            for slot in self.hashmap.table: # Iterate through each slot (bucket) in the hash table
                if slot is None:    # TO remove 'NoneType' object as it is not iterable
                    continue
                # Iterate through each book_title and hashset in the current slot
                for book_title, hashset in slot:
                    # Check if the keyword exists in the hashset
                    if hashset.find(keyword):
                        books_keywords.append(book_title)
        return sorted(books_keywords)

    def print_books(self):
        # Iterate through each entry in the hash table to print book titles and their contents
        # Handle each collision type with a unique format
        for tup in self.hashmap.table:
            if tup is None:
                continue

            # For "Chain" collision type
            if self.collision_type == "Chain" and isinstance(tup, list):
                for entry in tup: # Iterate through each entry (book_title and hashset) in the chain
                    book_title, book_words = entry # Unpack the tuple into book title and hashset

                    # Initialize a list to collect word outputs
                    output = []
                    # Iterate through the hashset's table to gather words
                    for word in book_words.table:
                        if word is None:
                            output.append("<EMPTY>")
                        elif isinstance(word, list):
                            output.append(" ; ".join([w for w in word if w]))
                        else:
                            output.append(word)
                    print(f"{book_title}: {' | '.join(output)}")

            # For "Linear" and "Double" collision types
            elif self.collision_type in ["Linear", "Double"]:
                book_title, book_words = tup
                # Initialize a list to collect word outputs
                output = [] 
                # Iterate through the hashset's table to gather words
                for word in book_words.table:
                    if word is None:
                        output.append("<EMPTY>")
                    elif isinstance(word, list):
                        output.append(" ; ".join([w for w in word if w]))
                    else:
                        output.append(word)
                print(f"{book_title}: {' | '.join(output)}")
                    




