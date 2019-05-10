from zadanie2 import Car, DieselCar, EnvironmentalError
import unittest

print('zadanie2 test')

def info(c, car):
    """
    Produce another info about object.

    Args:
        c (Car): Car object.
        car (tuple): Tuple of car that was created with.

    Returns:
        (str): String info about car.
    """
    loc = hex(id(c))
    brand = car[0]
    cap = car[1]
    fuel = car[2]
    prc = (fuel/cap) * 100
    return (
        "<Car at {} of brand {}, with tank full in {:3.1f}%>"
        .format(loc, brand, prc)
    )


class TestTask2(unittest.TestCase):
    """
    Test for Car and DieselCar module.
    """

    ex1 = [
        ('Merc', 100, 20),
        ('BMW', 77, 23),
        ('Audi', 53, 12),
        ('Lambo', 1000, 1000),
        ('Ferrari', 1234, 0)
    ]

    ex1_full = [
        80,
        54,
        41,
        0,
        1234
    ]

    ex1_bad_liters = [
        [100, 81, 543, 2145],
        [333, 77, 55, 55],
        [42, 42, 43, 44],
        [1, 2, 3, 4, 5],
        [1235, 10000, 10000000]
    ]

    ex1_liters = [
        [1, 2, 3, 4, 5, 6, 10, 20, 22, 66, 80],
        [10, 0, 42, 50, 51, 9],
        [2, 4, 5, 10],
        [0, 0, 0, 0, 0],
        [1, 1, 1234, 1234, 0, 2, 9]
    ]

    ex1_prc = [
        [
            (0.5, 30),
            (0.25, 5),
            (0.1, 0)
        ],
        [
            (0.5, 15),
            (0.25, 0),
            (0.1, 0)
        ],
        [
            (0.5, 14),
            (0.25, 1),
            (0.1, 0)
        ],
        [
            (0.5, 0),
            (0.25, 0),
            (0.1, 0)
        ],
        [
            (0.5, 617),
            (0.25, 308),
            (0.1, 123)
        ]
    ]


    def test_good_creating(self):
        for car in self.ex1:
            c = Car(*car)
            d = DieselCar(*car)
            self.assertEqual(str(c), info(c, car))
            self.assertEqual(str(d), info(d, car))

    def test_bad_creating(self):
        cars = [
            ((1, 1, 1), TypeError),
            (('', 'sto', 1), TypeError),
            (('', 1, 'sto'), TypeError),

            (('', -1, 1), ValueError),
            (('', 1, -1), ValueError),
            (('', 0, 0), ValueError),
            (('', 10, 20), ValueError)
        ]
        for c in cars:
            self.assertRaises(c[1], Car, *c[0])
            self.assertRaises(c[1], DieselCar, *c[0])

    def test_good_full_filling(self):
        """
        Checking filling the tank to maximum with all the methods.
        """
        for car, ans in zip(self.ex1, self.ex1_full):
            c = Car(*car)
            self.assertEqual(c.fill_tank(), ans)
            c = Car(*car)
            self.assertEqual(c.fill_tank(limit=1.), ans)
            c = Car(*car)
            self.assertEqual(c.fill_tank(liters=ans), ans)

    def test_good_empty_filling(self):
        """
        Filling tank with nothing.
        """
        for car in self.ex1:
            c = Car(*car)
            self.assertEqual(c.fill_tank(liters=0), 0)
            c = Car(*car)
            self.assertEqual(c.fill_tank(limit=0.), 0)

    def test_good_limit_filling(self):
        """
        Test filling with limit.
        """
        for limits, car in zip(self.ex1_prc, self.ex1):
            for (prc, ans) in limits:
                c = Car(*car)
                self.assertEqual(c.fill_tank(limit=prc), ans)

    def test_good_liters_filling(self):
        for liters, car in zip(self.ex1_liters, self.ex1):
            for ans in liters:
                c = Car(*car)
                self.assertEqual(c.fill_tank(liters=ans), ans)

    def test_bad_liters(self):
        for liters, car in zip(self.ex1_bad_liters, self.ex1):
            for e in liters:
                c = Car(*car)
                with self.assertRaises(ValueError):
                    c.fill_tank(liters=e)

    def test_bad_input_methods(self):
        for car in self.ex1:
            c = Car(*car)
            with self.assertRaises(TypeError):
                c.fill_tank(liters='sto')
            with self.assertRaises(TypeError):
                c.fill_tank(limit='sto')
            with self.assertRaises(TypeError):
                c.fill_tank(limit=1., liters=100)
            with self.assertRaises(ValueError):
                c.fill_tank(other=10)

    #pools
    def test_good_pool(self):
        pools = [
            0,
            1,
            2,
            3,
            10,
            100
        ]
        for nr in pools:
            cp = Car.get_carpool(nr)
            cps = [c.brand for c in cp]
            self.assertEqual(len(cps), nr)
            dp = DieselCar.get_carpool(nr)
            dps = [d.brand for d in dp]
            self.assertEqual(len(dps), nr)

    def test_method_pool(self):
        for i in [10,20,30]:
            cars = Car.get_carpool(i)
            for c in cars:
                self.assertEqual(c.fill_tank(limit=0.), 0)
                self.assertEqual(c.fill_tank(liters=0), 0)

    def test_bad_pool(self):
        exs = [
            'sto',
            1.1,
            0.5,
            '20',
            [],
            [1,23]
        ]
        for e in exs:
            with self.assertRaises(TypeError):
                Car.get_carpool(e)
            with self.assertRaises(TypeError):
                DieselCar.get_carpool(e)

    def test_diesel_fill(self):
        for car in self.ex1:
            dc = DieselCar(*car)
            with self.assertRaises(EnvironmentalError):
                dc.fill_tank()
            with self.assertRaises(EnvironmentalError):
                dc.fill_tank(limit=0.5)
            with self.assertRaises(EnvironmentalError):
                dc.fill_tank(liters=10)



if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    # m = Car('merc', 70, 1)
    # print(m.fill_tank(liters=1))
    # print(m.fill_tank(limit=0.5))
    # print(m)
    # Car.get_carpool(3)
    # print('asf')
    # Car.get_carpool(0)
    # print('asf')
    # Car.get_carpool(1)
    # dc = DieselCar.get_carpool(1)
    # dc = dc.pop()
    # dc.fill_tank()
    unittest.main()
