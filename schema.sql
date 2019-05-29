drop table if exists passengers;
  create table passengers (
    id integer primary key autoincrement,
    name text,
    age integer,
    sex text,
    pclass integer,
    fare integer,
    survived integer
);




