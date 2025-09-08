# Complaint Application in Python

# Define a class for complaints
class Complaint:
    def __init__(self, complainant, issue, details):
        self.complainant = complainant
        self.issue = issue
        self.details = details
        self.status = "Open" # Initial status

    def __str__(self):
        return f"Complainant: {self.complainant}\nIssue: {self.issue}\nDetails: {self.details}\nStatus: {self.status}"

# Function to add a new complaint
def add_complaint():
    complainant = input("Enter your name: ")
    issue = input("Enter the issue: ")
    details = input("Enter the details: ")
    complaint = Complaint(complainant, issue, details)
    complaints.append(complaint)
    print("Complaint added successfully!")

# Function to view all complaints
def view_complaints():
    if not complaints:
        print("No complaints to display.")
        return
    for i, complaint in enumerate(complaints):
        print(f"\nComplaint #{i+1}:\n{complaint}")

# Function to mark a complaint as resolved
def resolve_complaint():
    view_complaints()
    if not complaints:
        return
    try:
        index = int(input("Enter the number of the complaint to resolve: ")) - 1
        if 0 <= index < len(complaints):
            complaints[index].status = "Resolved"
            print("Complaint marked as resolved.")
        else:
            print("Invalid complaint number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Main program loop
complaints = [] # List to store complaints

while True:
    print("\nComplaint Application Menu:")
    print("1. Add Complaint")
    print("2. View Complaints")
    print("3. Resolve Complaint")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_complaint()
    elif choice == '2':
        view_complaints()
    elif choice == '3':
        resolve_complaint()
    elif choice == '4':
        print("Exiting application. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
