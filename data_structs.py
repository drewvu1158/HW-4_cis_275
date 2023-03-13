class AbstractCollection:

	def __init__(self, source_collection=None):
		""" Sets the initial state of self, which includes the contents of source_collection """

		self._size = 0
		if source_collection:
			for item in source_collection:
				self.add(item)

	def __len__(self):
		""" Return the number of items in this collection """
		return self._size

	def is_empty(self):
		""" Returns True if the collection is empty and False otherwise """
		return len(self) == 0

	def __add__(self, other):
		""" Overloads the + operator. A new collection is created with everything from self and other. """
		result = type(self)(self)
		for item in other:
			result.add(item)
		return result



class Array:

    def __init__(self, capacity, fill_value=None):
        """ Capacity is the static size of the array
            Each index in the array is filled with fill_value """
        self._items = []
        for count in range(capacity):
            self._items.append(fill_value)

    def __len__(self):
        """ Returns the length of this array """
        return len(self._items)

    def __str__(self):
        """ Returns a string representation of this array """
        return str(self._items)

    def __iter__(self):
        """ Supports iteration with a for loop """
        return iter(self._items)

    def __getitem__(self, index):
        """ Retrieves the item at 'index' """
        return self._items[index]

    def __setitem__(self, index, new_item):
        """ Sets the internal list's index to 'new_item' """
        self._items[index] = new_item






class MinHeap(AbstractCollection):
    DEFAULT_CAPACITY = 100
    def __init__(self):
        self._heap = Array(MinHeap.DEFAULT_CAPACITY)
        AbstractCollection.__init__(self)

    def add(self, item):
        """ From Class - adds item to minheap in the correct location"""
        self._heap[self._size] = item
        cur_index = self._size  # book likes len(self)
        while cur_index > 0:
            parent_index = (cur_index - 1) // 2
            parent_item = self._heap[parent_index]
            if parent_item <= item:
                break
            else:
                self._heap[cur_index] = parent_item
                self._heap[parent_index] = item
                cur_index = parent_index

        self._size += 1

    def peek(self):
        if self.is_empty():
            raise IndexError("Heap is empty")

        return self._heap[0]

    def pop(self):
        if self.is_empty():
            raise IndexError("Heap is empty")
        top_item = self._heap[0]
        bottom_item = self._heap[self._size-1]
        self._heap[0] = bottom_item
        last_valid_index = self._size - 2  # why 2?

        cur_index = 0  # start trickling in a loop down to correct location
        while True:
            left_child_index = 2 * cur_index + 1
            right_child_index = 2 * cur_index + 2
            if left_child_index > last_valid_index:
                # there are no children
                break
            if right_child_index > last_valid_index:
                # left child is the winner
                min_child_index = left_child_index
            else:
                if self._heap[left_child_index] < self._heap[right_child_index]:
                    min_child_index = left_child_index
                else:
                    min_child_index = right_child_index
            min_child = self._heap[min_child_index]
            if bottom_item <= min_child:
                #  item being moved goes here because it's less than both children.
                break
            # item being moved is larger than its min child. swap and continue
            self._heap[cur_index] = min_child
            self._heap[min_child_index] = bottom_item
            cur_index = min_child_index

        self._size -= 1
        return top_item

    def print_heap(self):
        for i in range(self._size):
            print(self._heap[i], end = ' ')
        print()


class ArrayQueue(AbstractCollection):
    def __init__(self, source_collection=None):
        self._front = 0
        self._rear = 0
        self._items = Array(10)
        AbstractCollection.__init__(self, source_collection)

    def ensure_capacity(self):
        new = Array(len(self._items) * 2)
        for i in range(len(self)):
            new[i] = self._items[self._front]
            self._front = (self._front + 1) % len(self._items)
        
        self._rear = len(self)
        self._items = new
        self._front = 0
    

    def add(self, item):
        if self._size == len(self._items):
            self.ensure_capacity()
        
        
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % len(self._items)
        self._size += 1

    def clear(self):
        self._size = 0
        self._front = 0
        self._rear = 0
        for i in range(len(self._items)):
            self._items[i] = None

    def peek(self):
        if self.is_empty():
            raise KeyError("The queue is empty")
        else:
            return self._items[self._front]

    def pop(self):
        if not self.is_empty():
            result = self._items[self._front]
            self._size -= 1
            self._front = (1 + self._front) % len(self._items)
            return result
        raise ValueError("Queue is empty")
    
    def print_queue(self):
        print(self._items)



