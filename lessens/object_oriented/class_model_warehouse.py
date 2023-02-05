# -*- coding: utf-8 -*-

from random import randint
from termcolor import cprint


# Реалезуем модель доставки грузов

# Дорога - хранит растояния между обьектами
# Склад - хранит груз и управляет очередями грузовиков
#
# Базовый класс - Машина,
# имеет
#     кол-во топлива
# может
#     заправляться
#
# Грузовик (производное от Машина)
# имеет
#     емкость кузова, скорость движения, расход топлива за час поездки
# может
#     стоять под погрузкой/разгрузкой
#     ехать со скоростью

# Погрусчик (производный от Машины)
# имеет
#     скорость погрузки, расход топлива в час при работе
# может
#     загружать/разгружать самосвал
#     ждать самосвал

class Road:

    def __init__(self, start, end, distance):
        self.start = start
        self.end = end
        self.distance = distance


class Warehouse:

    def __init__(self, name, content=0):
        pass

    def __str__(self):
        pass

    def set_road_out(self, road):
        pass

    def truck_arrived(self, truck):
        pass

    def get_next_truck(self):
        pass

    def truck_ready(self, truck):
        pass

    def act(self):
        pass


class Vehicle:
    fuel_rate = 0

    def __init__(self, model):
        self.model = model

    def __str__(self):
        pass

    def tack_up(self):
        pass


class Truck(Vehicle):

    def __init__(self, model, body_space=1000):
        pass

    def __str__(self):
        pass

    def ride(self):
        pass

    def go_to(self, road):
        pass

    def act(self):
        pass


class AoutoLoader(Vehicle):

    def __init__(self, model, bucket_capacity=100, warehouse=None, role='loader'):
        pass

    def __str__(self):
        pass

    def act(self):
        pass

    def load(self):
        pass

    def unload(self):
        pass


TOTAL_CARGO = 100000

moscow = Warehouse(name='Moscow', content=TOTAL_CARGO)
piter = Warehouse(name="Piter", content=0)

moscow_piter = Road(start=moscow, end=piter, distance=715)
piter_moscow = Road(start=piter, end=moscow, distance=780)

moscow.set_road_out(moscow_piter)
piter.set_road_out(piter_moscow)

loader_1 = AoutoLoader(model='Bobcat', bucket_capacity=1000, warehouse=moscow, role='loader')
loader_2 = AoutoLoader(model='Lonking', bucket_capacity=500, warehouse=piter, role='unloader')

truck_1 = Truck(model='KAMAZ', body_space=5000)
truck_2 = Truck(model='GAZ', body_space=2000)

moscow.truck_arrived(truck_1)
moscow.truck_arrived(truck_2)

hour = 0

while piter.content < TOTAL_CARGO:
    hour += 1
    cprint('------------- Час {}'.format(hour), color='red')
    truck_1.act()
    truck_2.act()
    loader_1.act()
    loader_2.act()
    moscow.act()
    piter.act()
    cprint(truck_1, color='cyan')
    cprint(truck_2, color='cyan')
    cprint(loader_1, color='cyan')
    cprint(loader_2, color='cyan')
    cprint(moscow, color='cyan')
    cprint(piter, color='cyan')
