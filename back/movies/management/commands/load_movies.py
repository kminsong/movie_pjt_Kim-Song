import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre

class Command(BaseCommand):
    help = "Load movies from TMDB API"

    def handle(self, *args, **kwargs):
        api_url = "https://api.themoviedb.org/3/movie/popular"
        api_key = "afdb577878bc5af42e6d066494d623d3"  # TMDB API 키를 여기에 입력하세요.
        params = {"api_key": api_key, "language": "ko-KR", "page": 1}

        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            movies = data.get("results", [])
            for movie_data in movies:
                # 장르 처리
                genres = movie_data.get("genre_ids", [])
                genre_objs = Genre.objects.filter(id__in=genres)
                
                # Movie 객체 생성 또는 업데이트
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=movie_data["id"],
                    defaults={
                        "title": movie_data["title"],
                        "overview": movie_data["overview"],
                        "release_date": movie_data["release_date"],
                        "poster_path": movie_data["poster_path"],
                        "popularity": movie_data["popularity"],
                        "adult": movie_data["adult"],
                    },
                )
                # Many-to-Many 관계 설정
                movie.genres.set(genre_objs)
                movie.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(movies)} movies."))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch movies: {response.status_code}"))
