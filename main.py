import json
import csv
import os
import time
import random

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.03)
    print()

monsters = [
    {"name": "Flowey", "hp": 50, "attack": 10},
    {"name": "Toriel", "hp": 100, "attack": 15},
    {"name": "Sans", "hp": 200, "attack": 20},
]


def choose_monster():
    return random.choice(monsters)


def start_battle(playername):
    print(f"Вы встречаете монстра! Бой начинается!")
    monster = choose_monster()
    print(f"{monster['name']} появляется перед вами.")

    while monster["hp"] > 0:
        print(f"{monster['name']} (HP: {monster['hp']})")
        action = input("Выберите действие (атаковать/убежать): ").lower()

        if action == "атаковать":
            player_attack = random.randint(5, 20)
            monster["hp"] -= player_attack
            print(f"Вы атакуете {monster['name']} и наносите {player_attack} урона!")
            if monster["hp"] <= 0:
                print(f"{monster['name']} погиб!")
                break

            monster_attack = random.randint(5, 15)
            print(f"{monster['name']} атакует вас и наносит {monster_attack} урона!")
        elif action == "убежать":
            print(f"Вы пытаетесь убежать от {monster['name']}!")
            if random.random() < 0.5:
                print("Вы убежали успешно!")
                break
            else:
                print(f"{monster['name']} не позволил вам убежать!")
                monster_attack = random.randint(5, 15)
                print(f"{monster['name']} атакует вас и наносит {monster_attack} урона!")
        else:
            print("Неверное действие. Попробуйте еще раз.")

def save_game(playername):
    game_data = {
        "playername": playername,
        "monsters": monsters
    }
    with open('game_data.json', 'w') as json_file:
        json.dump(game_data, json_file)

def load_game():
    if not os.path.isfile('game_data.json'):
        return None
    with open('game_data.json') as json_file:
        data = json.load(json_file)
    return data

def delete_save():
    if os.path.isfile('game_data.json'):
        os.remove('game_data.json')

def update_csv(playername):
    fieldnames = ['playername', 'monsters']
    data_dict = {
        "playername": playername,
        "monsters": monsters
    }

    if not os.path.isfile('game_data.csv'):
        with open('game_data.csv', mode='w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data_dict)
    else:
        with open('game_data.csv', mode='a') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(data_dict)


def main():
    player_name = input("Введите имя вашего персонажа: ")
    saved_game = load_game()
    if saved_game is not None and saved_game['playername'] == player_name:
        print(f"Добро пожаловать обратно, {player_name}!")
    else:
        print(f"Добро пожаловать, {player_name}!")

    while True:
        action = input("Что вы хотите сделать (начать бой/выйти из игры/сохранить игру/загрузить игру/удалить сохранение): ").lower()
        if action == "начать бой":
            start_battle(player_name)
            update_csv(player_name)
        elif action == "выйти из игры":
            print("Спасибо за игру!")
            break
        elif action == "сохранить игру":
            save_game(player_name)
            print("Игра сохранена!")
        elif action == "загрузить игру":
            saved_game = load_game()
            if saved_game is not None:
                player_name = saved_game['playername']
                print(f"Игра загружена! Добро пожаловать обратно, {player_name}!")
            else:
                print("Нет сохраненных игр.")
        elif action == "удалить сохранение":
            delete_save()
            print("Сохраненная игра удалена!")
        else:
            print("Неверная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()
