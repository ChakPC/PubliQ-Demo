create table movies (
	movie_id int,
    movie varchar(255),
    genre_id int,
    primary key (movie_id),
    foreign key (genre_id) references genres(genre_id)
);