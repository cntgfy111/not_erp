create table if not exists Address(
  id serial primary key,
  area double precision not null,
  windows int not null,
  phys_address text not null,
  floor int not null,
  room int not null,
  room_idx double precision not null
);

CREATE TYPE BulbState AS ENUM ('включена', 'выключена', 'неисправна');

create table if not exists LightBulb(
  serial_number varchar(13) primary key,
  state BulbState not null,
  light_temp int not null,
  price int,
  address int references Address(id)
);

create table if not exists Temperature(
  id bigserial primary key,
  bulb varchar(13) references LightBulb(serial_number),
  temp int,
  measure_time timestamp not null
);


create table if not exists Monitor(
  id int
);
