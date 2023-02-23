from src.repositories.dto.movie import CastDto
from src.repositories.dto.movie import GenreDto
from src.repositories.dto.movie import MovieInfoDto
from src.repositories.dto.movie import WatchProviderDto


class MoviesRepository:
    def __init__(self) -> None:
        pass

    async def get_movie_info(self, movie_id: int, locale: str) -> MovieInfoDto:
        return MovieInfoDto(
            id=161,
            title="Одиннадцать друзей Оушена",
            original_title="Ocean's Eleven",
            poster="/zEuI9yi0mOHjBzIubMMsxHxtKz1.jpg",
            release_date="2001-12-07",
            genre=[
                GenreDto(
                    id=53,
                    name="триллер"
                ),
                GenreDto(
                    id=80,
                    name="криминал"
                ),
            ],
            length=116,
            adult=False,
            providers=[
                WatchProviderDto(
                    logo="/o9ExgOSLF3OTwR6T3DJOuwOKJgq.jpg",
                    provider_name="Ivi",
                )
            ],
            overview="После выхода из тюрьмы вора Дэнни Оушена не проходит и 24 часов, а он уже планирует организовать самое сложное ограбление казино в истории. Он хочет украсть 150 млн. американских долларов из трех самых преуспевающих казино Лас-Вегаса. Все эти казино принадлежат элегантному и в то же время жестокому дельцу-Терри Бенедикту. Всего за одну ночь, Дэнни подбирает команду из одиннадцати «специалистов», способных совершить эту дерзкую кражу.",
            cast=[
                CastDto(
                    profile="/4s3wI0bqOP7K3hhcmKqV6m3GYiQ.jpg",
                    name="George Clooney",
                    character="Danny Ocean",
                ),
                CastDto(
                    profile="/4s3wI0bqOP7K3hhcmKqV6m3GYiQ.jpg",
                    name="George Clooney",
                    character="Danny Ocean",
                ),
                CastDto(
                    profile="/4s3wI0bqOP7K3hhcmKqV6m3GYiQ.jpg",
                    name="George Clooney",
                    character="Danny Ocean",
                ),
                CastDto(
                    profile="/4s3wI0bqOP7K3hhcmKqV6m3GYiQ.jpg",
                    name="George Clooney",
                    character="Danny Ocean",
                ),
                CastDto(
                    profile="/4s3wI0bqOP7K3hhcmKqV6m3GYiQ.jpg",
                    name="George Clooney",
                    character="Danny Ocean",
                ),
                CastDto(
                    profile="/4s3wI0bqOP7K3hhcmKqV6m3GYiQ.jpg",
                    name="George Clooney",
                    character="Danny Ocean",
                ),
            ],
        )
