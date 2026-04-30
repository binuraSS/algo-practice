import os

# 1. THE LOADER
def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

# 2. THE SAVER
def save_tasks(tasks):
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

def show_menu():
    print("\n--- TASKMASTER ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Exit")

# --- MAIN PROGRAM ---
# Load tasks ONCE at the start
tasks = load_tasks()

while True:
    show_menu()
    user_choice = input("Choose an option (1-4): ")

    if user_choice == "1":
        new_task = input("Enter the task: ")
        tasks.append(new_task)
        save_tasks(tasks) # Save immediately
        print("✅ Task added and saved!")

    elif user_choice == "2":
        if not tasks:
            print("\nYour list is empty!")
        else:
            print("\nYour Tasks:")
            for index, task in enumerate(tasks, start=1):
                print(f"{index}. {task}")

    elif user_choice == "3":
        try:
            task_num = int(input("Enter task number to remove: "))
            removed = tasks.pop(task_num - 1)
            save_tasks(tasks) # Update the file after removing
            print(f"🗑️ Removed: {removed}")
        except (ValueError, IndexError):
            print("⚠️ Invalid number!")

    elif user_choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")
        