# LIST EXAMPLE

fruits = ["apple", "banana", "cherry"]

print("Original list:", fruits)

# Access by index
print("First fruit:", fruits[0])

# Modify element
fruits[1] = "mango"
print("After modification:", fruits)

# Add element
fruits.append("orange")
print("After adding:", fruits)

# Remove element
fruits.remove("apple")
print("After removing:", fruits)

# TUPLE EXAMPLE

coordinates = (10, 20)

print("Tuple:", coordinates)
print("X value:", coordinates[0])

# Try to modify (this will cause error)
# coordinates[0] = 15

# DICTIONARY EXAMPLE

student = {
    "name": "Claudia",
    "age": 21,
    "course": "Data Science"
}

print("Student dictionary:", student)

# Access using key
print("Student name:", student["name"])

# Modify value
student["age"] = 22
print("After age update:", student)

# Add new key
student["grade"] = "A"
print("After adding grade:", student)