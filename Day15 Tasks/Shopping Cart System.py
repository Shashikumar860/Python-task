"""3. Shopping Cart System
Scenario: A user adds items to a shopping cart.
Task:
● Store items in a list
● Convert to set to remove duplicates
● Use loop + condition to calculate total cost
● Handle invalid input using try-except"""

# Price list of items
price_list = {
    "apple": 90,
    "banana": 700,
    "orange": 150,
    "grapes": 140
}
print("\nItems in cart:", price_list)
# 1. Store items in a list
cart = []

print("Enter items (type 'done' to finish):")

while True:
    try:
        item = input("Enter item: ").lower()
        
        if item == "done":
            break
        
        # 4. Handle invalid input using try-except
        if item not in price_list:
            raise ValueError("Invalid item")
        
        cart.append(item)
    
    except ValueError as e:
        print("Error:", e)

# 2. Convert list to set (remove duplicates)
unique_items = set(cart)
print("Unique items:", unique_items)

# 3. Calculate total cost using loop + condition
total_cost = 0
for item in unique_items:
    if item in price_list:
        total_cost += price_list[item]
print("Total cost:", total_cost)