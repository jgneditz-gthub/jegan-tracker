from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import datetime


class ExpenseApp(App):

    def build(self):
        self.expenses = []
        self.current_day = datetime.date.today()

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.amount_input = TextInput(
            hint_text="Enter amount",
            multiline=False,
            input_filter='float'
        )
        layout.add_widget(self.amount_input)

        self.category = Spinner(
            text="Food",
            values=("Food", "Travel", "Shopping", "Other")
        )
        layout.add_widget(self.category)

        btn = Button(text="Add Expense")
        btn.bind(on_press=self.add_expense)
        layout.add_widget(btn)

        self.total_label = Label(text="Total: 0.00")
        layout.add_widget(self.total_label)

        self.dashboard = Label(text="No data yet")
        layout.add_widget(self.dashboard)

        return layout

    def add_expense(self, instance):
        today = datetime.date.today()

        if today != self.current_day:
            self.expenses = []
            self.current_day = today

        try:
            amt = float(self.amount_input.text)
            if amt <= 0:
                self.total_label.text = "Amount must be positive"
                return
            cat = self.category.text
            self.expenses.append((amt, cat))
            self.amount_input.text = ""
            self.update_ui()
        except ValueError:
            self.total_label.text = "Invalid input"

    def update_ui(self):
        total = sum(x[0] for x in self.expenses)

        cat_total = {}
        for amt, cat in self.expenses:
            cat_total[cat] = cat_total.get(cat, 0) + amt

        breakdown = "\n".join([f"{k}: {v:.2f}" for k, v in cat_total.items()])

        self.total_label.text = f"Total: {total:.2f}"
        self.dashboard.text = f"Breakdown:\n{breakdown}"


if __name__ == "__main__":
    ExpenseApp().run()
