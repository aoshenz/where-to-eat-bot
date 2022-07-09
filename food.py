import pandas as pd
import random
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


q1 = "What meal is this for?"
q1_options = ["Breakfast 🥐", "Lunch 🍗", "Dinner 🍱", "Dessert 🍨"]
q1_dict = {
    "Breakfast 🥐": "is_for_breakfast",
    "Lunch 🍗": "is_for_lunch",
    "Dinner 🍱": "is_for_dinner",
    "Dessert 🍨": "is_for_dessert",
}

q2 = "What is the price range?"
q2_options = ["Low 💵", "Med 💰", "High 💸"]
q2_col = "price_range"
q2_dict = {
    "Low 💵": 1,
    "Med 💰": 2,
    "High 💸": 3,
}

q3 = "What type of weather?"
q3_options = ["Hot", "Cold", "Either"]
q3_col = "ideal_weather"
q3_dict = {
    "Hot": "hot",
    "Cold": "cold",
    "Either": "any",
}


class Food:
    def __init__(self, data=pd.read_csv("./data/food.csv")):
        self.data = data

    def filter(self, dict, option, column=None, single_col=True):

        data = self.data.copy()

        if single_col:
            ans = dict[option]

            # don't filter if chosen option is any
            data = data[(data[column] == ans) | (data[column] == "any")]

            self.data = data
        else:
            col = dict[option]
            data = data[data[col] == 1]
            self.data = data

    def choose_food(self):

        remaining_rows = len(self.data)

        if remaining_rows > 0:
            random_row = random.randint(0, remaining_rows - 1)

            self.chosen_restaurant = self.data["restaurant"].iloc[random_row]
            self.chosen_location = self.data["location"].iloc[random_row]

            logger.info("Chose row %s from %s: %s, %s", random_row + 1, remaining_rows, self.chosen_restaurant, self.chosen_location)
        else:

            self.chosen_restaurant = "No restaurants with your choices"
            self.chosen_location = "try again"



def save_answer(list, answer):

    chosen_selection_without_q = answer[3:]

    logger.info(chosen_selection_without_q)
    list.append(chosen_selection_without_q)

    return chosen_selection_without_q
