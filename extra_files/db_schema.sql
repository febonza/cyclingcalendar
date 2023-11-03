CREATE TABLE races (
    date_from date,
    date_to	date,
    name text not null,
    venue text,
    country text,
    category text,
    discipline text,
    calendar text,
    class text,
    email text,
    website text
);


CREATE TABLE amateur_races (
    id integer primary key autoincrement,
    race_name text not null unique,
    organizer text,
    race_local text,
    race_date date,
    website text,
    category text,
    picture_race text
);


CREATE TABLE user_races (
    id integer primary key autoincrement,
    user_id integer,
    race_id integer,
    date_added datetime
);

