kv = '''
ScreenManager:
    LoginScreen:
    DashboardScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        Label:
            text: "Financial Planning App"
            font_size: 32
        TextInput:
            id: username
            hint_text: "Username"
            multiline: False
        TextInput:
            id: password
            hint_text: "Password"
            multiline: False
            password: True
        Button:
            text: "Login"
            on_release: root.login(username.text, password.text)

<DashboardScreen>:
    name: 'dashboard'
    BoxLayout:
        orientation: 'vertical'
        TabbedPanel:
            do_default_tab: False
            TabbedPanelItem:
                text: "Budgeting"
                BudgetScreen:
            TabbedPanelItem:
                text: "Stock Analysis"
                StockScreen:
            TabbedPanelItem:
                text: "Mortgage Tracking"
                MortgageScreen:

<BudgetScreen@BoxLayout>:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    Label:
        text: "Budgeting Module"
        font_size: 24
    TextInput:
        id: income
        hint_text: "Enter your monthly income"
        input_filter: 'float'
    TextInput:
        id: expenses
        hint_text: "Enter your monthly expenses"
        input_filter: 'float'
    TextInput:
        id: savings_goal
        hint_text: "Enter your savings goal"
        input_filter: 'float'
    Button:
        text: "Calculate Budget"
        on_release: root.calculate_budget(income.text, expenses.text, savings_goal.text)
    Label:
        id: budget_result
        text: ""

<StockScreen@BoxLayout>:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    Label:
        text: "Stock Analysis Module"
        font_size: 24
    Label:
        text: """Dummy Stock Data:\nAAPL: $150.00\nGOOG: $2800.00\nAMZN: $3400.00"
<MortgageScreen@BoxLayout>:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    Label:
        text: "Mortgage Tracking Module"
        font_size: 24
    TextInput:
        id: principal
        hint_text: "Enter mortgage principal"
        input_filter: 'float'
    TextInput:
        id: interest
        hint_text: "Enter annual interest rate (%)"
        input_filter: 'float'
    TextInput:
        id: years
        hint_text: "Enter number of years"
        input_filter: 'int'
    Button:
        text: "Calculate Monthly Payment"
        on_release: root.calculate_mortgage(principal.text, interest.text, years.text)
    Label:
        id: mortgage_result
        text: ""
'''

# --- Python Code Section ---
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Define our Login Screen
class LoginScreen(Screen):
    def login(self, username, password):
        # For simplicity, any username/password works. In a real app, add secure authentication.
        self.manager.current = 'dashboard'

# Define our Dashboard Screen that contains the tabbed panel
class DashboardScreen(Screen):
    pass

# Define the Budgeting module logic
class BudgetScreen(BoxLayout):
    def calculate_budget(self, income, expenses, savings_goal):
        try:
            income_val = float(income)
            expenses_val = float(expenses)
            savings_val = float(savings_goal)
            disposable = income_val - expenses_val
            result_text = f"Disposable Income: ${disposable:.2f}\n"
            if disposable >= savings_val:
                result_text += "You are on track to meet your savings goal."
            else:
                result_text += "You may need to cut back on expenses."
            self.ids.budget_result.text = result_text
        except ValueError:
            self.ids.budget_result.text = "Please enter valid numbers."

# Define the Stock Analysis module (dummy data for now)
class StockScreen(BoxLayout):
    pass

# Define the Mortgage Tracking module logic
class MortgageScreen(BoxLayout):
    def calculate_mortgage(self, principal, interest, years):
        try:
            P = float(principal)
            annual_interest_rate = float(interest)
            n_years = int(years)
            r = annual_interest_rate / 100 / 12  # monthly interest rate
            n = n_years * 12  # total number of payments
            if r == 0:
                monthly_payment = P / n
            else:
                monthly_payment = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
            self.ids.mortgage_result.text = f"Monthly Payment: ${monthly_payment:.2f}"
        except ValueError:
            self.ids.mortgage_result.text = "Please enter valid numbers."

# The main app class builds the UI from our KV string.
class FinancialPlanningApp(App):
    def build(self):
        return Builder.load_string(kv)

# Run the app
if __name__ == '__main__':
    FinancialPlanningApp().run()