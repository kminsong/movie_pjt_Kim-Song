import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre


class Command(BaseCommand):
    help = "Load top 1000 popular movies from TMDB API"

    def handle(self, *args, **kwargs):
        api_url = "https://api.themoviedb.org/3/movie/popular"
        api_key = "afdb577878bc5af42e6d066494d623d3"  # TMDB API 키
        params = {"api_key": api_key, "language": "ko-KR"}

        total_movies = 0  # 총 저장된 영화 개수
        max_pages = 50  # 50페이지(1000개)를 가져오도록 설정

        for page in range(1, max_pages + 1):
            params["page"] = page
            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                data = response.json()
                movies = data.get("results", [])
                if not movies:
                    break  # 더 이상 데이터가 없으면 종료
                
                for movie_data in movies:
                    # 장르 처리
                    genres = movie_data.get("genre_ids", [])
                    genre_objs = Genre.objects.filter(id__in=genres)

                    # release_date 처리 (빈 값이면 None으로 설정)
                    release_date = movie_data.get("release_date", None)
                    if not release_date:  # release_date가 빈 문자열 또는 None인 경우
                        release_date = None
                    
                    # Movie 객체 생성 또는 업데이트
                    movie, created = Movie.objects.update_or_create(
                        tmdb_id=movie_data["id"],
                        defaults={
                            "title": movie_data["title"],
                            "overview": movie_data["overview"],
                            "release_date": release_date,  # None일 경우 Django가 처리
                            "poster_path": movie_data["poster_path"],
                            "popularity": movie_data["popularity"],
                            "adult": movie_data["adult"],
                        },
                    )
                    # Many-to-Many 관계 설정
                    movie.genres.set(genre_objs)
                    movie.save()

                total_movies += len(movies)
                self.stdout.write(self.style.SUCCESS(f"Page {page}: Loaded {len(movies)} movies."))

            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch movies from page {page}: {response.status_code}"))
                break

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {total_movies} movies."))
