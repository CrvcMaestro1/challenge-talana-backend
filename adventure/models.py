from datetime import date

from django.db import models


# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        import math
        passenger_per_row = 2
        row_numbers = math.ceil(self.vehicle_type.max_capacity / passenger_per_row)
        result = []
        boarded_passengers = 0
        for rn in range(row_numbers):
            current_row = [False, False]
            for passenger in range(passenger_per_row):
                current_row[passenger] = boarded_passengers < self.passengers
                boarded_passengers += 1
            result.append(current_row)
        return result


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self) -> bool:
        return self.end is not None


def validate_number_plate(number_plate: str) -> bool:
    plate = number_plate.split("-")
    if not len(plate) == 3:
        return False
    return plate[0].isalpha() and plate[1].isnumeric() and plate[2].isnumeric()
