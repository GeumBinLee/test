from googleapiclient.discovery import build

# API 키 설정
API_KEY = "YOUR_API_KEY"
youtube = build("youtube", "v3", developerKey=API_KEY)

# 검색하기
request = youtube.search().list(part="snippet", maxResults=10, q="검색어")
response = request.execute()

for item in response["items"]:
    print(item["snippet"]["title"])
