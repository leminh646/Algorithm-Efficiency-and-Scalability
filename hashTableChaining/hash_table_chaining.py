import random

class HashTableChaining:
    def __init__(self, initial_capacity=8, load_factor_threshold=0.75):
        self.m = initial_capacity
        self.table = [[] for _ in range(self.m)]
        self.n = 0
        self.load_factor_threshold = load_factor_threshold
        
        # Universal hash params
        self.p = 2**61 - 1
        self.a = random.randrange(1, self.p)
        self.b = random.randrange(0, self.p)
    
    def _hash(self, key):
        h0 = hash(key)
        h0 = h0 if h0 >= 0 else -h0
        return ((self.a * h0 + self.b) % self.p) % self.m
    
    def insert(self, key, value):
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.n += 1
        if self.n / self.m > self.load_factor_threshold:
            self._resize(self.m * 2)
    
    def search(self, key):
        idx = self._hash(key)
        for (k, v) in self.table[idx]:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.n -= 1
                # shrink if very sparse
                if self.m > 8 and self.n / self.m < self.load_factor_threshold / 4:
                    self._resize(self.m // 2)
                return True
        return False
    
    def _resize(self, new_capacity):
        old_items = [pair for bucket in self.table for pair in bucket]
        self.m = new_capacity
        self.table = [[] for _ in range(self.m)]
        self.n = 0
        self.a = random.randrange(1, self.p)
        self.b = random.randrange(0, self.p)
        for (k, v) in old_items:
            self.insert(k, v)
