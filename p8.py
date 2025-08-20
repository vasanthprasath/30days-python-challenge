
students = []

# Input number of students
n = int(input())

# Read name and score for each student
for _ in range(n):
    name = input()
    score = float(input())
    students.append([name, score])

# Get unique scores and sort them
scores = sorted(set([s[1] for s in students]))

# Get second lowest score
second_lowest = scores[1]

# Get all students with second lowest score
result = sorted([s[0] for s in students if s[1] == second_lowest])

# Print each name
for name in result:
    print(name)
