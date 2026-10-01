"""A simple interactive stack program implemented with a Python list."""


class Stack:
    """Last-in, first-out (LIFO) stack."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def display(self):
        return list(reversed(self._items))


def main():
    stack = Stack()

    while True:
        print("\n--- Stack Menu ---")
        print("1. Push")
        print("2. Pop")
        print("3. Peek")
        print("4. Display")
        print("5. Size")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            stack.push(input("Enter a value: "))
            print("Value pushed.")
        elif choice == "2":
            try:
                print(f"Popped: {stack.pop()}")
            except IndexError as error:
                print(error)
        elif choice == "3":
            try:
                print(f"Top value: {stack.peek()}")
            except IndexError as error:
                print(error)
        elif choice == "4":
            values = stack.display()
            print("Top -> Bottom:", values if values else "Stack is empty.")
        elif choice == "5":
            print(f"Stack size: {stack.size()}")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
