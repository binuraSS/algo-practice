import time

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target: return mid
        if arr[mid] > target: high = mid - 1
        else: low = mid + 1
    return -1

# 1. Create 1 million sorted items
data = list(range(1, 1000001))

try:
    # 2. Get User Input
    target = int(input("Enter a number to find (1 to 1,000,000): "))
    
    # 3. Benchmark the Algorithm
    start_time = time.perf_counter()
    result = binary_search(data, target)
    end_time = time.perf_counter()
    
    # 4. Report Results
    if result != -1:
        print(f"✅ Found {target} at index {result}")
    else:
        print("❌ Number not in list.")
        
    print(f"⏱️ Search took: {(end_time - start_time) * 1000:.4f} ms")

except ValueError:
    print("⚠️ Please enter a valid whole number.")