class CarInterface:

    def get_speed(self):
        pass

    def get_weight(self):
        pass


class SportCar(CarInterface):

    def get_speed(self):
        return 150

    def get_weight(self):
        return 100


class FamilyCar(CarInterface):

    def get_speed(self):
        return 100

    def get_weight(self):
        return 500


class Truck(CarInterface):

    def __init__(self, model):
        self.model = model
        self.privet_car = CarInterface

    def get_speed(self):
        return 60

    def get_weight(self):
        return 1000


my_truck = Truck(model="Opel")

print(my_truck.get_speed())
print(my_truck.model)
print(my_truck.privet_car.get_speed)
