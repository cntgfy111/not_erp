import datetime as dt
from dataclasses import dataclass
from enum import Enum
from random import randrange, random, choice
from itertools import count
import sys
from typing import List


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

    @staticmethod
    def generate_inserts(addresses) -> str:
        values = map(lambda a: f"{a.id, a.area, a.windows, a.phys_address, a.floor, a.room, a.room_index}", addresses)
        return f'insert into Address(id, area, windows, phys_address, floor, room, room_idx) values\n\t' + ',\n\t'.join(values) + ";"


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

    @staticmethod
    def generate_inserts(bulbs) -> str:
        values = map(lambda b: f"{b.serial_number, b.state.name, b.light_temp, b.price, b.address_ref.id}", bulbs)
        return f'insert into LightBulb(serial_number, state, light_temp, price, address) values\n\t' + ',\n\t'.join(values) + ";"


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

    @staticmethod
    def generate_inserts(temps):
        values = map(lambda t: f"{t.bulb, t.t, t.time.strftime('%Y-%m-%d %H:%M')}", temps)
        return f'insert into Temperature(bulb, temp, measure_time) values\n\t' + ',\n\t'.join(values) + ";"


if __name__ == '__main__':
    bulb_count = int(sys.argv[1])

    rooms = [Address.generate() for _ in range(max(1, int(bulb_count / 50)))]
    print(Address.generate_inserts(rooms))

    bulbs = [Lightbulb.generate(choice(rooms)) for _ in range(bulb_count)]
    print(Lightbulb.generate_inserts(bulbs))

    temps = [Temperature.generate(choice(bulbs)) for _ in range(bulb_count * 10)]
    print(Temperature.generate_inserts(temps))
