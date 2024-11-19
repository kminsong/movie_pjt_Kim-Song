from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    adult = models.BooleanField(default=False)  # 성인 콘텐츠 여부
    genres = models.ManyToManyField(Genre, related_name="movies")  # 장르 관계 추가

    def __str__(self):
        return self.title
