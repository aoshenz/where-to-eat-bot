import pandas as pd


class Food:
    def __init__(self, data=pd.read_csv("./data/food.csv")):
        self.data = data

    def filter_q1(self, option):

        data = self.data.copy()
        col = q1_dict[option]
        data = data[data[col] == 1]
        self.data = data

        # print(self.data)
    
    def filter_q2(self, option):

        data = self.data.copy()
        ans = q2_dict[option]
        data = data[data[q2_col] == ans]
        self.data = data

        # print(self.data)

    def choose_food(self):
        self.chosen_restaurant = self.data["restaurant"].iloc[0]
        self.chosen_location = self.data["location"].iloc[0]


q1 = "What meal is this for?"
q1_options = ["Breakfast 🥐", "Lunch 🍗", "Dinner 🍱", "Dessert 🍨"]
q1_dict = {
    "Breakfast 🥐": "is_for_breakfast",
    "Lunch 🍗": "is_for_lunch",
    "Dinner 🍱": "is_for_dinner",
    "Dessert 🍨": "is_for_desert",
}

q2 = "What is the price range?"
q2_options = ["Low 💵", "Med 💰", "High 💸"]
q2_col = "price_range"
q2_dict = {
    "Low 💵": 1,
    "Med 💰": 2,
    "High 💸": 3,
}
