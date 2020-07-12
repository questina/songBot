import telebot
import random
import views

def generate_markup(buttons):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    list_items = []
    for item in buttons:
        list_items.append(item)
    random.shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup


def generate_points():
    list_of_points = views.get_points()
    list_of_markups = []
    list_of_questions = []
    list_of_scores = []
    list_of_reactions = []
    for point in list_of_points:
        keyboard = [telebot.types.InlineKeyboardButton(wrong_ans, callback_data='wrong') for wrong_ans in point.wrong_answer.split(';')]
        keyboard.append(telebot.types.InlineKeyboardButton(point.right_answer, callback_data='right'))
        random.shuffle(keyboard)
        markup = telebot.types.InlineKeyboardMarkup()
        for item in keyboard:
            markup.add(item)
        list_of_markups.append(markup)
        list_of_questions.append(point.question)
        list_of_scores.append(point.score)
        list_of_reactions.append(point.reaction)
    return list_of_markups, list_of_questions, list_of_scores, list_of_reactions






