import models
import datetime


def create_tables():
    with models.database as db:
        db.create_tables([models.User, models.Point])


def insert_Points_into_DB():
    point_1 = models.Point(score=5, question='Из какого мультфильма строчки песни: Взгляни вокруг, оглянись назад, духи с тобой связаться хотят',
                           wrong_answer='Скуби-Ду;Гравити Фолз;Рик и Морти',
                           right_answer='Шаман Кинг', reaction='Неверно, это начало опенинга к аниме Шаман Кинг;Верно, а у тебя хорошее детство было :Р')
    point_2 = models.Point(score=5, question='Из какого фильма строчка песни: Со мною вот что происходит, ко мне мой лучший друг не ходит',
                           wrong_answer='Двенадцать стульев;Полосатый рейс;Кавказская пленница',
                           right_answer='Ирония судьбы', reaction='Неверно, это начальная песня советского фильма Ирония Судьбы;Верно!')
    point_3 = models.Point(score=10, question='Из какого мультфильма строчка песни: But the meteor men beg to differ',
                           wrong_answer='Холодное сердце;Ледниковый период;Би муви',
                           right_answer='Шрек', reaction='Неверно, это же All stars из Шрека;Верно, да ты фанат Шрека!!!')
    point_4 = models.Point(score=10, question='Из какого фильма строчка песни: And the last known survivor stalks his prey in the night',
                           wrong_answer='Телохранитель;Бойцовский клуб;Терминатор',
                           right_answer='Рокки', reaction='Неверно, это Eye of the tiger, знаменитая песня из Рокки;Верно!')
    point_1.save()
    point_2.save()
    point_3.save()
    point_4.save()


def registration(message):
    if not(message.from_user.username in dict_of_users):
        user = models.User(username=message.from_user.username, join_date=datetime.date.today(), score = 0)
        user.save()
        dict_of_users.update({message.from_user.username: True})


def get_points():
    list_of_points = list()
    for points in models.Point.select():
        list_of_points.append(points)
    return list_of_points


def update_user_scores(username, score):
    user = models.User.get(models.User.username == username)
    user.score = score
    user.save()


def updating_dictionary():
    dict_of_users = dict()
    for user in models.User.select():
        dict_of_users.update({user.username:False})
    return dict_of_users


dict_of_users = updating_dictionary()