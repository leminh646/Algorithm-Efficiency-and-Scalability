import random
import time
import sys
import pandas as pd

# Allow deeper recursion for sorted/reverse inputs
sys.setrecursionlimit(10000)

def randomized_quicksort(arr):
    """
    Randomized QuickSort: picks a random pivot, partitions into <, ==, >,
    and recurses. Returns a new sorted list.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[random.randrange(len(arr))]
    lt = [x for x in arr if x < pivot]
    eq = [x for x in arr if x == pivot]
    gt = [x for x in arr if x > pivot]
    return randomized_quicksort(lt) + eq + randomized_quicksort(gt)

def deterministic_quicksort(arr):
    """
    Deterministic QuickSort: always uses the first element as pivot.
    Returns a new sorted list.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    lt = [x for x in arr if x < pivot]
    eq = [x for x in arr if x == pivot]
    gt = [x for x in arr if x > pivot]
    return deterministic_quicksort(lt) + eq + deterministic_quicksort(gt)

if __name__ == "__main__":
    # Benchmark settings
    sizes = [1000, 2000, 5000]
    repeats = 5
    distributions = {
        'random':   lambda n: [random.randint(0, n) for _ in range(n)],
        'sorted':   lambda n: list(range(n)),
        'reverse':  lambda n: list(range(n, 0, -1)),
        'repeated': lambda n: [random.randint(0, 9) for _ in range(n)]
    }

    results = []
    for n in sizes:
        for name, gen in distributions.items():
            # Avoid deep recursion crash for deterministic on very large sorted inputs
            if name in ('sorted', 'reverse') and n > 2000:
                continue

            # Prepare one input array for randomized tests
            base = gen(n)
            total_rand = 0.0
            for _ in range(repeats):
                arr = base.copy()
                t0 = time.perf_counter()
                randomized_quicksort(arr)
                total_rand += (time.perf_counter() - t0)
            avg_rand = total_rand / repeats

            # Prepare fresh inputs for deterministic tests
            total_det = 0.0
            for _ in range(repeats):
                arr = gen(n)
                t0 = time.perf_counter()
                deterministic_quicksort(arr)
                total_det += (time.perf_counter() - t0)
            avg_det = total_det / repeats

            results.append({
                'n': n,
                'distribution': name,
                'randomized_avg_time_s': avg_rand,
                'deterministic_avg_time_s': avg_det
            })

    # Display results
    df = pd.DataFrame(results)
    print(df)
