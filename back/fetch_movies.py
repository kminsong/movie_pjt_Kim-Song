import requests
import json

# TMDB API 설정
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NmIyYTk4MDI1ZTYzNWI5Y2M3OGNjNTZmNTU3NmIxMyIsIm5iZiI6MTczMTkxNzI5MC41NTYzNiwic3ViIjoiNjczNmQwMmFhYzlmM2JhMDgxNTU4M2U4Iiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.1nt7qRIUrZImHayfM0p8_bClQGi-bNDvGOAs2iGvPqo"  # 자신의 TMDB API 키를 입력하세요
BASE_URL = "https://api.themoviedb.org/3/movie/popular"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 연령 등급 정보 가져오기
def is_r18(movie_id):
    try:
        release_dates_url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates"
        response = requests.get(release_dates_url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            for result in data.get("results", []):
                if result.get("iso_3166_1") == "KR":  # 한국 기준 등급 확인
                    for release in result.get("release_dates", []):
                        if release.get("certification") in ["R", "18"]:  # R-18 등급 확인
                            return True
        return False
    except Exception as e:
        print(f"Error checking R-18 status for movie {movie_id}: {e}")
        return True  # 오류 발생 시 기본적으로 제외


def fetch_movies():
    all_movies = []
    total_pages = 10  # 10페이지 x 20개 = 200개 데이터

    for page in range(1, total_pages + 1):
        try:
            print(f"Fetching page {page}...")
            response = requests.get(BASE_URL, headers=HEADERS, params={
                "language": "ko-KR",
                "page": page,
                "include_adult": False  # 성인 콘텐츠 제외 요청
            })

            if response.status_code == 200:
                data = response.json()
                movies = []
                for movie in data["results"]:
                    if not is_r18(movie["id"]):  # R-18 등급 필터링
                        movies.append({
                            "model": "movies.movie",
                            "pk": movie["id"],  # 고유 TMDB ID를 pk로 사용
                            "fields": {
                                "tmdb_id": movie["id"],
                                "title": movie["title"],
                                "overview": movie.get("overview", ""),
                                "release_date": movie.get("release_date", None),
                                "poster_path": movie.get("poster_path", ""),
                                "popularity": movie.get("popularity", 0),
                                "adult": movie.get("adult", False)
                            }
                        })
                all_movies.extend(movies)
            else:
                print(f"Failed to fetch page {page}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching page {page}: {e}")

    # 데이터를 fixtures/movies.json 파일에 저장
    with open("fixtures/movies.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

    print("Movies data saved to fixtures/movies.json")


if __name__ == "__main__":
    fetch_movies()
