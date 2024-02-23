import os

## Import .env var
from dotenv import load_dotenv
import googleapiclient.discovery
from video import Video
import random


# Set up the API client
api_service_name = "youtube"
api_version = "v3"
api_key = os.getenv("YOUTUBE_API_KEY")


def printVideos(videos):
    for i in range(len(videos)):
        print("(" + str(i + 1) + ")")
        video = videos[i]
        print("Video : ", end="")
        print(video.title)
        print("Author :", video.channelTitle)
        print(
            "Views :",
            str(round(int(video.viewCount) / 1000) * 1000),
            "| Likes :",
            str(video.likes),
        )
        print("-" * 100)


# Create the API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key
)


def alreadyDone(videoId):
    with open("ContentCreation/alreadyDone.txt", "r") as file:
        for line in file:
            if videoId in line:
                return False


def addToAlreadyDone(videoId):
    with open("alreadyDone.txt", "a") as file:
        file.write(videoId + "\n")


def getVideo(nb, search):
    # Call the search.list method to retrieve videos matching the search query
    print("We search for videos")
    search_response = (
        youtube.search()
        .list(q=search, type="video", part="id,snippet", maxResults=nb)
        .execute()
    )
    print("Videos aquired")
    for i in range(len(search_response["items"])):
        result = search_response["items"][i]
        videoId = result["id"]["videoId"]
        if not (alreadyDone(videoId)):
            video = Video(videoId)
            return video


def downloadVid():
    """
    Download a video and return the path to the file
    """
    frenchYoutubers = ["Squeezie"]
    youtuber = frenchYoutubers[random.randint(0, len(frenchYoutubers) - 1)]
    vid = getVideo(50, search=youtuber)
    ## get file path :
    path = os.path.dirname(os.path.realpath(__file__))
    outputPath = path + "/videoDownloads/" + vid.title + ".mp4"
    vid.download(outputPath=outputPath)
    return outputPath


if __name__ == "__main__":
    path = downloadVid()
