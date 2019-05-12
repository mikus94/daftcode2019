# coding: utf-8
"""
Zadanie rekrutacyjne Daftcode, Notif.AI.
Zadanie 2.
Autor: Mikolaj Gagatek
email: mikolaj.gagatek@gmail.com
"""
import logging
import random
import string
from numbers import Number


class EnvironmentalError(Exception):
    """
    Environmental Error used when Diesel Car is being filled with fuel.
    """
    pass


def _check_type(value, field, ctype):
    """
    Method checking if value is given type. It rises error if the field is not.

    Args:
        value: Value of checked variable.
        field (str): Name of variable.
        ctype: Given type to check.

    Returns:
        int: Value of int.
    """
    # check if not None
    if isinstance(value, ctype):
        return value
    else:
        raise TypeError(
            'Mismatch type in declaration of {} as {}.'.format(field, value)
        )


class Car:
    """
    Class representing a car.

    Attributes:
        brand (str): Name of a cars' brand.
        tank_capacity (int): Liters of maximum capacity of cars' tank.
        tanked_fuel (int): Current liters of fuel in tank.
    """

    def __init__(self, brand, tank_capacity, tanked_fuel):
        """
        Constructor of a car object.

        Args:
            brand (str): Name of the car brand.
            tank_capacity (int): Maximum capacity (in liters) of the car's tank.
            tanked_fuel (int): Actual capacity (liters) of fuel in the tank.
        """
        # assign instance variables
        self.brand = _check_type(brand, 'brand', str)
        self.tank_capacity = _check_type(tank_capacity, 'tank_capacity', Number)
        self.tanked_fuel = _check_type(tanked_fuel, 'tanked_fuel', Number)
        # check if tank capacity is not exceeded
        if tanked_fuel > tank_capacity:
            raise ValueError('Tanked fuel exceeds tank capacity!')
        # capacity should be > 0
        if tank_capacity <= 0:
            raise ValueError('Tank capacity should be positive integer!')
        # tanked fuel should be >= 0
        if tanked_fuel < 0:
            raise ValueError('Tanked fuel should be positive integer!')
        # get the percentage of full tank
        tank_prc = (tanked_fuel/tank_capacity) * 100
        logging.info(
            "New car of brand {}, with tank full in {:3.1f}%."
               .format(brand, tank_prc)
        )

    def fill_tank(self, **kwargs):
        """
        Car's fuel the tank to desired capacity.

        Keyword Args:
            limit (int): Limit of fuel to be fueled.
                Specified by percent of tank capacity <0;1>.
            liters (int): Number of liters to fuel the tank.

        Returns:
            int: Returns number of liters that were fueled.
        """
        # check if it is default behaviour
        if not kwargs:
            fueled = self.tank_capacity - self.tanked_fuel
            self.tanked_fuel = self.tank_capacity
            return fueled
        # get possible args
        liters = kwargs.get('liters', None)
        limit = kwargs.get('limit', None)
        if len(kwargs) > 1:
            raise TypeError(
                   'You can only declare liters or limit argument!'
            )

        if liters is not None:
            # check if it is int
            _check_type(liters, 'liters', Number)
            # check if we can fill it with that much liters of fuel
            fueled = self.tanked_fuel + liters
            if fueled > self.tank_capacity:
                raise ValueError(
                    'You cannot fill tank with {} liters! '
                    'It gets filled too much!'.format(liters)
                )
            self.tanked_fuel = fueled
            return liters

        if limit is not None:
            # check limit type and if it is range <0;1>
            _check_type(limit, 'limit', Number)
            if limit < 0 or limit > 1:
                raise ValueError(
                    'Limit value should be in range <0;1>, is {}!'
                    .format(limit)
                )
            desired_fuel = limit * self.tank_capacity
            # if desired fuel capacity is lower than current capacity
            # then fill with 0 fuel
            if desired_fuel <= self.tanked_fuel:
                return 0
            # fuel to desired level
            fueled = desired_fuel - self.tanked_fuel
            self.tanked_fuel = desired_fuel
            return fueled
        # unknown arg
        raise ValueError('Unknown keyword argument.')

    @classmethod
    def get_carpool(cls, number):
        """
        Generate %number of random Cars.

        Args:
            number (int): Number of Cars to generate.

        Returns:
            set: Set of Cars.
        """

        def random_string(length=10):
            """
            Generate random string of fixed length.

            Args:
                length (int): Length of string (default 10).

            Returns:
                str: Returns random string.
            """
            letters = string.ascii_letters
            return ''.join(random.choice(letters) for _ in range(length))

        # dictionary of cars
        carpool = dict()
        # create %number Cars in loop.
        for i in range(number):
            # create unique name
            name = random_string()
            while carpool.get(name, None):
                name = random_string()
            # create tank and fuel it
            tank_cap = random.randint(1, 100)
            fuel = random.randint(0, tank_cap)
            # create car and add it to set
            carpool[name] = cls(name, tank_cap, fuel)
        # return set instead of dict
        return set(carpool.values())

    def __repr__(self):
        """
        Representation of the object.

        Returns:
            str: Representation of object.
        """
        prc_fuel = (self.tanked_fuel / self.tank_capacity) * 100
        new_repr = (
            "<Car at {} of brand {}, with tank full in {:3.1f}%>"
            .format(hex(id(self)), self.brand, prc_fuel)
        )
        return new_repr


class DieselCar(Car):
    """
    Class representing Diesel Car.
    """

    def fill_tank(self, **kwargs):
        """
        Filling tank of diesel car.
        """
        raise EnvironmentalError(
            'Diesel fuel not available due to environmental reasons.'
        )
