create table genre_movie_relation (
    genre_id int,
    movie_id int,
    primary key (genre_id, movie_id),
    foreign key (genre_id) references genres(genre_id) on delete cascade,
    foreign key (movie_id) references movies(movie_id) on delete cascade
);