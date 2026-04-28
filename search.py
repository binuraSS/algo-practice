def find_item(target, items):
    for i in range(len(items)):
        if items[i] == target:
            return f"Found at index {i}"
    return "Not found"

data = [10, 23, 45, 71, 11, 15,70]
print(find_item(70, data))