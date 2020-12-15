class DLLNode():
    # if value is none, loop to self
    def __init__(self, value, prev, next) -> None:
        if value is None:
            self.v = 0
            self.p = self
            self.n = self
            return

        self.v = value
        self.p = prev
        prev.n = self
        self.n = next
        next.p = self