create table notes(
    id integer primary key autoincrement,
    done boolean not null default 0,
    note text not null
);