class Stack:
    def __init__(self):
        self.size = 0
        self.head = None

    def empty(self):
        return self.size == 0

    def size(self):
        return self.size

    def clear(self):
        self.head = None
        self.size = 0

    def push(self, folder):
        folder.next = self.head
        self.head = folder
        self.size += 1

    def pop(self):
        if self.size == 0:
            return None

        item = self.head
        self.head = self.head.next
        self.size -= 1
        return item

    def peek(self):
        return self.head


