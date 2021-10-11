create table if not exists Genre(
	id serial primary key,
	title varchar(40) not null unique
);

create table if not exists Singer(
	id serial primary key,
	pseudonym varchar(40) not null	
);

create table if not exists SingerGenre(
	singer_id integer not null references Singer(id),
	genre_id integer not null references Genre(id),
	constraint singer_genre primary key (singer_id, genre_id)
);

create table if not exists Album(
	id serial primary key,
	title varchar(40) not null,
	year integer not null
);

create table if not exists SingerAlbum(
	singer_id integer not null references Singer(id),
	album_id integer not null references Album(id),
	constraint singer_album primary key (singer_id, album_id)
);

create table if not exists Track(
	id serial primary key,
	title varchar(40) not null,
	duration integer not null,
	album_id integer references Album(id)
);

create table if not exists Collection(
	id serial primary key,
	title varchar(40) not null,
	duration integer not null,
	year integer not null
);

create table if not exists CollectionTrack(
	collection_id integer not null references Collection(id),
	track_id integer not null references track(id),
	constraint collection_track primary key (collection_id, track_id)
);
