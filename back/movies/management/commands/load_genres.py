import requests
from django.core.management.base import BaseCommand
from movies.models import Genre

class Command(BaseCommand):
    help = "Load genres from TMDB API"

    def handle(self, *args, **kwargs):
        api_url = "https://api.themoviedb.org/3/genre/movie/list"
        api_key = "afdb577878bc5af42e6d066494d623d3"  # TMDB API 키를 여기에 입력하세요.
        params = {"api_key": api_key, "language": "ko-KR"}

        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            genres = data.get("genres", [])
            for genre in genres:
                Genre.objects.update_or_create(id=genre["id"], defaults={"name": genre["name"]})
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(genres)} genres."))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch genres: {response.status_code}"))
