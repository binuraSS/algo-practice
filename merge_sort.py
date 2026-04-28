def merge_sort(arr):
    # Base case: A list of 0 or 1 items is already sorted
    if len(arr) <= 1:
        return arr

    # 1. Split the list in half
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # 2. Merge the sorted halves
    return merge(left_half, right_half)

def merge(left, right):
    result = []
    i = j = 0

    # Compare elements from each half and pick the smaller one
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Test it out
data = [38, 27, 43, 3, 9, 82, 10]
print(f"Original: {data}")
print(f"Sorted:   {merge_sort(data)}")