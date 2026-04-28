def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        # Find the middle index
        mid = (low + high) // 2
        guess = arr[mid]

        if guess == target:
            return f"Target {target} found at index {mid}"
        
        if guess > target:
            # Target is in the left half, move the high pointer
            high = mid - 1
        else:
            # Target is in the right half, move the low pointer
            low = mid + 1

    return "Target not found"

# Test data (MUST be sorted)
my_list = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

print(binary_search(my_list, 7))   # Found
print(binary_search(my_list, 10))  # Not found