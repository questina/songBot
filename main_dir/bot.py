import config
import utils
import telebot
import tb_token

use_inline_markup = True

dict_of_scores = dict()
dict_of_users = utils.views.updating_dictionary()
dict_of_steps = dict()

bot = telebot.TeleBot(tb_token.token)

markups, questions, scores, reactions = utils.generate_points()


@bot.message_handler(func=lambda query: True, commands=['signup'])
def signingup(message):
    if message.from_user.username in dict_of_users and dict_of_users[message.from_user.username]:
        if dict_of_steps[message.from_user.username] < len(scores):
            bot.send_message(message.chat.id, 'Ты уже начал игру, введи /game чтобы продолжить')
        else:
            bot.send_message(message.chat.id, 'Ты уже зарегистрировался. Чтобы начать или продолжить игру напиши /game')
    else:
        utils.views.registration(message)
        dict_of_users.update({message.from_user.username : True})
        dict_of_scores.update({message.from_user.username : 0})
        dict_of_steps.update({message.from_user.username : 0})
        bot.send_message(message.chat.id, 'Ты зарегистрирован. Чтобы начать игру введи /game')
        print(dict_of_users)


@bot.message_handler(func=lambda query: True, commands=['game'])
def game(message):
    if message.from_user.username in dict_of_users.keys() and message.from_user.username in dict_of_steps.keys():
        if dict_of_steps[message.from_user.username] < len(scores):
            bot.send_message(message.chat.id, questions[dict_of_steps[message.from_user.username]], reply_markup=markups[dict_of_steps[message.from_user.username]])
        else:
            bot.send_message(message.chat.id, 'Ты уже прошел тест. Если хочешь пройти заново, зарегистрируйся еще раз.')
    else:
        bot.send_message(message.chat.id, 'Сначала нужно зарегистрироваться')


@bot.message_handler(func=lambda mes: mes.text in config.buttons, content_types=['text'])
def check_answer(message):
    hide_keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, config.buttons[message.text], reply_markup=hide_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        reaction = reactions[dict_of_steps[call.from_user.username]].split(';')
        bot.send_message(call.message.chat.id, reaction[0] if call.data == 'wrong' else reaction[1])
        dict_of_steps[call.from_user.username] += 1
        if dict_of_steps[call.from_user.username] < len(scores):
            score = scores[dict_of_steps[call.from_user.username]]
            dict_of_scores[call.from_user.username] += score if call.data == 'right' else 0
            print(dict_of_scores)
            question = questions[dict_of_steps[call.from_user.username]]
            bot.send_message(call.message.chat.id, question, reply_markup=markups[dict_of_steps[call.from_user.username]])
        else:
            bot.send_message(call.message.chat.id, 'Игра окончена\n{} заработал(а) {} очков'.format(call.from_user.username, dict_of_scores[call.from_user.username]))
            utils.views.update_user_scores(call.from_user.username, dict_of_scores[call.from_user.username])
            dict_of_users[call.from_user.username] = False
    else:
        print('jej 404')


@bot.message_handler(content_types=["text"])
def repeat_mes(message):
    bot.send_message(message.chat.id, config.default_message)


if __name__ == '__main__':
    bot.infinity_polling()