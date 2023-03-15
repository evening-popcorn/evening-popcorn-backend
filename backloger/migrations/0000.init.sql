CREATE TABLE users_backlog(
    user_id uuid,
    movie_id int,
    note text,
    added_at timestamp,
    constraint users_backlog_pk
        primary key (user_id, movie_id)
)