import json
import os

class FinanceTracker:
    def __init__(self, filename='finance_data.json'):
        self.filename = filename
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {"users": {}, "current_user": None}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def register(self, username, password):
        if username in self.data['users']:
            return "Username already exists."
        self.data['users'][username] = {
            'password': password,
            'expenses': [],
            'income': [],
            'budget': 0
        }
        self.save_data()
        return "Registration successful."

    def login(self, username, password):
        user = self.data['users'].get(username)
        if user and user['password'] == password:
            self.data['current_user'] = username
            return "Login successful."
        return "Invalid username or password."

    def logout(self):
        self.data['current_user'] = None
        self.save_data()
        return "Logged out successfully."

    def add_expense(self, category, amount):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "You need to login first."
        user['expenses'].append({'category': category, 'amount': amount})
        self.save_data()
        return f"Added expense: {category} - ${amount}"

    def add_income(self, source, amount):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "You need to login first."
        user['income'].append({'source': source, 'amount': amount})
        self.save_data()
        return f"Added income: {source} - ${amount}"

    def set_budget(self, amount):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "You need to login first."
        user['budget'] = amount
        self.save_data()
        return f"Budget set to ${amount}"

    def view_report(self):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "You need to login first."
        total_income = sum(item['amount'] for item in user['income'])
        total_expenses = sum(item['amount'] for item in user['expenses'])
        budget = user['budget']
        return {
            "Total Income": total_income,
            "Total Expenses": total_expenses,
            "Budget": budget,
            "Remaining": budget - total_expenses
        }

def main():
    tracker = FinanceTracker()

    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. Add Expense")
        print("5. Add Income")
        print("6. Set Budget")
        print("7. View Report")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(tracker.register(username, password))
        
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(tracker.login(username, password))
        
        elif choice == '3':
            print(tracker.logout())

        elif choice == '4':
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            print(tracker.add_expense(category, amount))
        
        elif choice == '5':
            source = input("Enter income source: ")
            amount = float(input("Enter income amount: "))
            print(tracker.add_income(source, amount))
        
        elif choice == '6':
            amount = float(input("Enter budget amount: "))
            print(tracker.set_budget(amount))
        
        elif choice == '7':
            report = tracker.view_report()
            print("\n--- Financial Report ---")
            for key, value in report.items():
                print(f"{key}: ${value:.2f}")

        elif choice == '8':
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()