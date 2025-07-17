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
                if self.m > 8 and self.n / self.m < self.load_factor_threshold / 3:
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

if __name__ == "__main__":
    import random
    random.seed(0)  # make hash parameters deterministic for testing
    
    # 1. Basic insert & search
    ht = HashTableChaining(initial_capacity=4, load_factor_threshold=0.75)
    ht.insert("apple", 10)
    assert ht.search("apple") == 10, "ERROR: insert or search failed"
    
    # 2. Update existing key
    ht.insert("apple", 20)
    assert ht.search("apple") == 20, "ERROR: update failed"
    
    # 3. Delete key
    assert ht.delete("apple") is True, "ERROR: delete returned False"
    assert ht.search("apple") is None, "ERROR: deleted key still found"
    
    # 4. Collision handling (force collisions in small table)
    ht = HashTableChaining(initial_capacity=2, load_factor_threshold=1.0)
    ht.insert(0, "zero")
    ht.insert(2, "two")  # both 0 and 2 should hash to same bucket mod 2
    assert ht.search(0) == "zero", "ERROR: collision search failed for 0"
    assert ht.search(2) == "two",  "ERROR: collision search failed for 2"
    ht.delete(0)
    assert ht.search(0) is None and ht.search(2) == "two", "ERROR: delete in chain broke other entries"
    
    # 5. Resize-up test
    ht = HashTableChaining(initial_capacity=4, load_factor_threshold=0.5)
    ht.insert("a", 1)
    ht.insert("b", 2)
    # inserting third should trigger resize to 8
    ht.insert("c", 3)
    assert ht.m == 8, f"ERROR: expected resize-up to 8, got {ht.m}"
    for k, v in [("a",1),("b",2),("c",3)]:
        assert ht.search(k) == v, f"ERROR: after resize missing {k}"
    
    print("All basic tests passed!")
