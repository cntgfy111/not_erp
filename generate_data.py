import datetime as dt
from dataclasses import dataclass
from enum import Enum
from random import randrange, random, choice
from itertools import count
import sys


@dataclass
class Address:
    id_seq = count(start=1)
    addresses = [
            "Большая академическая улица, 44",
            "Прянишникова улица, 19",
            "Прянишникова улица, 17",
            "Тимирязевская улица, 55",
            "Прянишникова улица, 6",
            "Тимирязевская улица, 58",
            "Тимирязевский проезд, 2",
            "Тимирязевская улица, 54",
            "Тимирязевская улица, 48",
            "Тимирязевская улица, 44, стр. 1",
            "Верхняя аллея, 4",
            "Тимирязевская улица, 39",
            "Лиственничная аллея, 3",
            "Лиственничная аллея, 4А",
            "Лиственичная аллея, 5",
            "Прянишникова улица, 12",
    ]

    id: int
    area: int
    windows: int
    phys_address: str
    floor: int
    room: int
    room_index: float

    @staticmethod
    def generate():
        return Address(
                Address.id_seq.__next__(),
                area=randrange(15, 200),
                windows=randrange(1, 10),
                phys_address=choice(Address.addresses),
                floor=randrange(1, 4),
                room=randrange(1, 30),
                room_index=round(random(), 2)
        )

    def generate_insert(self) -> str:
        return f'insert into Address(id, area, windows, phys_address, floor, room, room_idx) values {self.id, self.area, self.windows, self.phys_address, self.floor, self.room, self.room_index};'


@dataclass
class Lightbulb:
    State = Enum("State", "включена, выключена, неисправна")

    serial_number: str
    state: State
    light_temp: int
    price: int
    address_ref: Address

    @staticmethod
    def generate(addres: Address):
        return Lightbulb(
                serial_number=''.join([choice(list(map(chr, range(ord('0'), ord('9'))))) for _ in range(13)]),
                state=list(Lightbulb.State)[randrange(len(Lightbulb.State))],
                light_temp=randrange(2700, 6500),
                price=randrange(10000, 100000),
                address_ref=addres
        )

    def generate_insert(self) -> str:
        return f'insert into LightBulb(serial_number, state, light_temp, price, address) values {self.serial_number, self.state.name, self.light_temp, self.price, self.address_ref.id};'


@dataclass
class Temperature:
    bulb: str
    t: int | None
    time: dt.datetime

    @staticmethod
    def generate(bulb: Lightbulb):
        return Temperature(
                bulb.serial_number,
                (randrange(180, 220) if (chance := random()) > 0.1
                    else None if chance > 0.9
                    else randrange(15, 23)),
                dt.datetime(2023, 2, randrange(1, dt.date.today().day), randrange(0, 24), randrange(0, 60))
        )

    def generate_insert(self) -> str:
        return f'insert into Temperature(bulb, temp, measure_time) values {self.bulb, self.t, self.time.strftime("%Y-%m-%d %H:%M")};'


if __name__ == '__main__':
    bulb_count = int(sys.argv[1])

    rooms = [Address.generate() for _ in range(max(1, int(bulb_count / 50)))]
    for room in rooms:
        print(room.generate_insert())

    bulbs = [Lightbulb.generate(choice(rooms)) for _ in range(bulb_count)]
    for bulb in bulbs:
        print(bulb.generate_insert())

    temps = [Temperature.generate(choice(bulbs)) for _ in range(bulb_count * 10)]
    for temp in temps:
        print(temp.generate_insert())
