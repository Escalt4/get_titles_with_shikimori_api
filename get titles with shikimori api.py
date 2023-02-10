import json
import time
import os

from shikimori_api import Shikimori

session = Shikimori()
api = session.get_api()
user_id = 506974

i = 0
while True:
    if not os.path.exists("my_anime_titles_" + str(i).zfill(3) + ".txt"):
        break
    i += 1

file_result = open("my_anime_titles_" + str(i).zfill(3) + ".txt", "w+", encoding="utf-8", errors="surrogateescape")

franchise_count = 0

# получаем аниме отмеченные просмотренными
user_anime_list = []
for i in api.users(user_id).anime_rates.GET(limit=9999, status='completed'):
    user_anime_list.append([i['anime']['id'], i['anime']['russian']])


# функция получения всех тайтлов в франшизе
def get_franchise(anime_id):
    franchise = []
    try:
        for i in api.animes(anime_id).franchise.GET()['nodes']:
            franchise.append([i['id'], i['name']])
    except Exception as ex:
        # print(ex)
        time.sleep(3)
        get_franchise(anime_id)

    return franchise


# разбиваем полученный список по франшизам
while len(user_anime_list) > 0:
    anime_id = user_anime_list[0][0]

    franchise = get_franchise(anime_id)

    # если аниме одно во франшизе то на сайте может быть пусто
    if len(franchise) == 0:
        franchise.append(user_anime_list[0])

    # ищем в списке просмотреного аниме одной франшизы
    for j in range(len(franchise)):
        if user_anime_list.count(franchise[j]) > 0:
            print(franchise[j][1])
            file_result.write(franchise[j][1] + "\n")

            user_anime_list.remove(franchise[j])

    print("")
    file_result.write("\n")

    franchise_count += 1

    time.sleep(0.5)

print("\nКоличество тайтлов: " + str(franchise_count))
file_result.write("\nКоличество тайтлов: " + str(franchise_count) + "\n")

file_result.close()

input()
