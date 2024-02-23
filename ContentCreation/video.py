import googleapiclient.discovery
from pytube import YouTube
import json

# Set up the API client
api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyCrMpBRwL88K6LTgn8gwGk2nv4Pyd6oFCU"  # Replace with your own API key
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key
)


def printDict(json_data):
    json_formatted_str = json.dumps(json_data, indent=2)
    print(json_formatted_str)


class Video:
    def __init__(self, id):
        print
        self.id = id
        infos = self.__getVideoInfos()
        #printDict(infos)
        self.title = infos["snippet"]["title"]

        self.description = infos["snippet"]["description"]
        self.viewCount = infos["statistics"]["viewCount"]
        try:
            self.likes = infos["statistics"]["likeCount"]
        except:
            # No like count
            self.likes = None
        self.channelTitle = infos["snippet"]["channelTitle"]
        self.publishDate = infos["snippet"]["publishedAt"]

    def __getVideoInfos(self):
        request = youtube.videos().list(
            part="snippet,statistics", id=self.id, key=api_key
        )
        response = request.execute()
        # print("Nb de videos : ",len(response["items"]))
        # print(response["items"][0]["snippet"]["title"])
        return response["items"][0]

    def download(
        self, outputPath="/home/maxencehabar/Vidéos/Search Downloads/", filename=None
    ):
        # print("Called the download method")
        url = "https://www.youtube.com/watch?v=" + str(self.id)
        # Download(url=url, outputPath=outputpath)
        print("Starting download of " + self.title, end="")
        youtubeObject = YouTube(url)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        try:
            if filename == None:
                youtubeObject.download(output_path=outputPath)
                print("Done")
            else:
                print("Filename is ", filename)
                print("Download : ",end="")
                youtubeObject.download(output_path=outputPath, filename=filename)
                print("Done")
        except:
            print("An error has occurred")
        print("Download is completed successfully")
