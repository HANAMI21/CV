import logging
import sys
from random import sample

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


class Game:
    #  Перша цифра у ключі відповідає за горизонталь, а друга за вертикаль
    cells = {"0:0": ["wh"], "1:0": ["wh"], "1:1": ["wh"], "2:1": ["wh"], "2:2": ["key"], "3:1": ["wh"],
             "3:0": ["wh"], "4:0": ["wh"], "5:0": ["wh"], "5:1": ["wh"], "6:1": ["heart"], "5:2": ["wh"],
             "4:3": ["heart"], "5:3": ["wh"], "6:3": ["wh"], "7:3": ["finish"]}

    commands = ["Праворуч", "Ліворуч", "Вгору", "Вниз", "Бити мечем", "Підняти ключ", "Лікуватися самостійно"]
    heroes_list = []

    def __init__(self):
        self.count_heroes = 0
        self.nicknames = []

    def greeting(self):
        logging.info("Вітаю, вкажіть кількість гравців!")
        while True:
            self.count_heroes = input()
            if self.count_heroes.isdigit() is False:
                logging.info("Потрібно ввести ціле число! Спробуйте ще раз!")
                continue
            else:
                break
        self.entering_names(int(self.count_heroes), self.heroes_list)
        self.start_game(self.heroes_list)

    @classmethod
    def entering_names(cls, count_heroes, heroes_list):
        for i in range(1, count_heroes + 1):
            hero = Hero()
            logging.info(f"Введіть ім'я {i}-го героя!")
            hero.nickname = input()
            heroes_list.append(hero)

        print("Для того щоб грати користуйся цими командами:\n", *Game.commands, sep=" || ")
        print("-" * 95)

    @classmethod
    def spawn_fires(cls, cells):
        temp_list = [addr for addr, value in cells.items() if "wh" in value]
        random_fires = sample(temp_list, k=4)
        logging.info("Вогні знаходяться на клітинах з координатами: ")
        print(*random_fires, sep=" || ")
        print("-" * 95)
        for i in random_fires:
            cells[i].append("fire")

    @classmethod
    def clear_fires(cls, cells):
        for addr, value in cells.items():
            if "fire" in value:
                cells[addr].remove("fire")

    @classmethod
    def start_game(cls, heroes_list):
        flag = True
        cls.spawn_fires(Game.cells)
        while True:
            for player in heroes_list:
                logging.info("Зараз хід гравця " + getattr(player, "nickname"))
                player.moving()
                if player.is_alive() is False:
                    logging.info("Герой " + getattr(player, "nickname") + " програв!")
                    heroes_list.remove(player)
                    print("-" * 95)
                if len(heroes_list) == 0:
                    flag = False
                    break
            if flag is False:
                break
            cls.clear_fires(Game.cells)
            cls.spawn_fires(Game.cells)


class Hero:
    def __init__(self, prev_x=0, prev_y=0, nickname="", health=5, x=0, y=0, charges=3, presence_key=False,
                 permission_take_key=False):
        self.nickname = nickname
        self.health = health
        self.x = x
        self.y = y
        self.prev_x = prev_x
        self.prev_y = prev_y
        self.charges = charges
        self.presence_key = presence_key
        self.permission_take_key = permission_take_key

    # def __str__(self):
    #     return f"Name: {self.nickname}  Age: {self.health}"

    def moving(self):
        while True:
            move = input()
            if move == "Праворуч":
                if f"{self.x + 1}:{self.y}" in Game.cells.keys():
                    self.del_from_cells()
                    print("-" * 95)
                    logging.info("Така клітина є")
                    print("-" * 95)
                    self.prev_x = self.x
                    self.prev_y = self.y
                    self.x += 1
                    self.checking_heart(move)
                    self.checking_key()
                    self.record_in_cells()
                    self.checking_hero()
                    if self.finishing():
                        Game.heroes_list.clear()
                        break
                    self.check_fire()
                    break
                else:
                    self.health -= 1
                    logging.info(f"Здається, ви вдарился в стіну!) Залишилось {self.health} ❤")
                    print("-" * 95)
                    break

            elif move == "Ліворуч":
                if f"{self.x - 1}:{self.y}" in Game.cells.keys():
                    self.del_from_cells()
                    print("-" * 95)
                    logging.info("Така клітина є")
                    print("-" * 95)
                    self.x -= 1
                    if self.check_prev_move() is False:
                        break
                    self.checking_heart(move)
                    self.checking_key()
                    self.record_in_cells()
                    self.checking_hero()
                    self.check_fire()
                    break
                else:
                    self.health -= 1
                    logging.info(f"Здається, ви вдарился в стіну!) Залишилось {self.health} ❤")
                    print("-" * 95)
                    break
            elif move == "Вгору":
                if f"{self.x}:{self.y + 1}" in Game.cells.keys():
                    self.del_from_cells()
                    print("-" * 95)
                    logging.info("Така клітина є")
                    print("-" * 95)
                    self.prev_y = self.y
                    self.prev_x = self.x
                    self.y += 1
                    self.checking_key()
                    self.record_in_cells()
                    self.checking_hero()
                    self.check_fire()
                    break
                else:
                    self.health -= 1
                    logging.info(f"Здається, ви вдарился в стіну!) Залишилось {self.health} ❤")
                    print("-" * 95)
                    break
            elif move == "Вниз":
                if f"{self.x}:{self.y - 1}" in Game.cells.keys():
                    self.del_from_cells()
                    print("-" * 95)
                    logging.info("Така клітина є")
                    print("-" * 95)
                    self.y -= 1
                    if self.check_prev_move() is False:
                        break
                    self.checking_key()
                    self.record_in_cells()
                    self.checking_hero()
                    self.check_fire()
                    break
                else:
                    self.health -= 1
                    logging.info(f"Здається, ви вдарился в стіну!) Залишилось {self.health} ❤")
                    print("-" * 95)
                    break
            elif move == "Бити мечем":
                self.hit_hero()
                break
            elif move == "Підняти ключ":
                self.pick_up_key()
                break
            elif move == "Лікуватися самостійно":
                if self.charges != 0:
                    self.health += 1
                    self.charges -= 1
                    logging.info("Вітаю, тепер у вас на 1 життя більше!")
                    print("-" * 95)
                    break
                else:
                    logging.info("На жаль, ви не можете більше себе лікувати(")
                    print("-" * 95)
                    break
            else:
                print("Такого ходу не існує, спробуйте ще раз!")
                print("-" * 95)
                continue

    def checking_heart(self, move):
        if "heart" in Game.cells[f"{self.x}:{self.y}"]:
            logging.info("Вітаю, ви знайшли ліки! Ваше здоров'я відновлено!)")
            print("-" * 95)
            self.health = 5
            if move == "Праворуч":
                self.x -= 1
            elif move == "Ліворуч":
                self.x += 1

    def checking_key(self):
        if f"{self.x}:{self.y}" == "2:2" and "key" in Game.cells["2:2"]:
            self.permission_take_key = True
            logging.info("Вітаю, в цій клітині є ключ!)")
            print("-" * 95)
            self.y -= 1
        elif "key" in Game.cells[f"{self.x}:{self.y}"]:
            self.permission_take_key = True
            logging.info("Вітаю, в цій клітині є ключ!)")
            print("-" * 95)

    def pick_up_key(self):
        if self.permission_take_key is True:
            self.presence_key = True
            logging.info("Ви підібрали ключ!)")
            print("-" * 95)
            self.permission_take_key = False
            if f"{self.x}:{self.y}" == "2:1":
                Game.cells["2:2"].remove("key")
            else:
                Game.cells[f"{self.x}:{self.y}"].remove("key")

    def is_alive(self):
        if self.health == 0 and self.presence_key is True:
            Game.cells[f"{self.x}:{self.y}"].append("key")
            return False
        elif self.health == 0:
            return False

    def record_in_cells(self):
        Game.cells[f"{self.x}:{self.y}"].append(self.nickname)

    def del_from_cells(self):
        if self.nickname in Game.cells[f"{self.x}:{self.y}"]:
            Game.cells[f"{self.x}:{self.y}"].remove(self.nickname)

    def checking_hero(self):
        for el in Game.heroes_list:
            if getattr(el, "nickname") in Game.cells[f"{self.x}:{self.y}"] and getattr(el, "nickname") != self.nickname:
                logging.info("Увага! В цій клітині є інші герої!")
                print("-" * 95)
                break

    def hit_hero(self):
        for el in Game.heroes_list:
            if getattr(el, "nickname") in Game.cells[f"{self.x}:{self.y}"] and getattr(el, "nickname") != self.nickname:
                setattr(el, "health", getattr(el, "health") - 1)

    def finishing(self):
        if "finish" in Game.cells[f"{self.x}:{self.y}"]:
            if self.presence_key is True:
                logging.info(f"Ураааа! {self.nickname} дійшов до фінішу та переміг!")
                print("-" * 95)
                return True
            else:
                logging.info("Ви дійшли до фінішу, але вас вбив голем, оскільки ви не мали ключа(((")
                print("-" * 95)
                self.health = 0

    def check_fire(self):
        if "fire" in Game.cells[f"{self.x}:{self.y}"]:
            logging.info(f"Ви отримали шкоду від вогню та втрачаєте 1 життя! Залишилось {self.health} ❤")
            print("-" * 95)
            self.health -= 1

    def check_prev_move(self):
        if "key" not in Game.cells[f"{self.prev_x}:{self.prev_y}"]:
            if self.x == self.prev_x or self.prev_y == self.x:
                logging.info(f"Герой {self.nickname} злякався і втік. Герой виводиться із гри!")
                print("-" * 95)
                self.health = 0
                return False


game = Game()
game.greeting()
