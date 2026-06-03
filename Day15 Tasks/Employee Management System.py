# Employee Management System

# 1. Create Employee class
class Employee:
    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary

    def display(self):
        return f"ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}"


# 2. Store employees in a dictionary
employees = {}

# Taking input
while True:
    choice = input("Add employee? (yes/no): ").lower()
    
    if choice == "no":
        break
    
    emp_id = input("Enter Employee ID: ")
    name = input("Enter Name: ")
    
    # 4. Exception handling for invalid salary
    try:
        salary = float(input("Enter Salary: "))
    except ValueError:
        print("Invalid salary! Please enter a number.")
        continue
    
    # Create object and store in dictionary
    emp = Employee(emp_id, name, salary)
    employees[emp_id] = emp


# 3. Save data to a file
try:
    with open("employees.txt", "w") as file:
        for emp in employees.values():
            file.write(emp.display() + "\n")
    print("Employee data saved to 'employees.txt'")
except Exception as e:
    print("Error saving file:", e)


# 5. Use loop to display all employees
print("\nEmployee List:")
for emp in employees.values():
    print(emp.display())