import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import subprocess
import ffmpeg
import math

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
            print("Video found : ", video.title)
            res = input("Do you want to download this video ? (y/n)")
            if res == "y":
                addToAlreadyDone(videoId)
                return video


def downloadVid():
    """
    Download a video and return the path to the file
    """
    frenchYoutubers = ["Squeezie anecdote"]
    youtuber = frenchYoutubers[random.randint(0, len(frenchYoutubers) - 1)]
    vid = getVideo(50, search=youtuber)
    ## get file path :
    path = os.path.dirname(os.path.realpath(__file__))
    outputPath = path + "/videoDownloads/" + vid.id + "/"
    filename = vid.title.replace(" ", "_") + ".mp4"
    vid.download(outputPath=outputPath, filename=filename)
    return outputPath + "/" + filename


def get_video_duration(filename):
    probe = ffmpeg.probe(filename)
    duration = float(probe["streams"][0]["duration"])
    return duration


def split_video(inputVideoPath, segment_duration=65):
    ## Create the output path if it doesn't exist
    ## get folder of the video
    output_path = os.path.dirname(inputVideoPath)
    output_path = output_path + "/parts"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    duration = get_video_duration(inputVideoPath)
    segments = math.ceil(duration / segment_duration)

    for i in range(segments):
        start = i * segment_duration
        # Use 'to' as the end time if it's within the video duration, otherwise use the video duration
        end = min((i + 1) * segment_duration, duration)

        output_filename = f"{output_path}/part_{i}.mp4"

        (
            ffmpeg.input(inputVideoPath, ss=start, to=end)
            .output(output_filename, codec="copy")
            .run()
        )


def center_horizontal_video_in_vertical(input_video, output_video):
    """
    Transform a horizontal video to fit in the upper half of a vertical format using ffmpeg-python.

    Parameters:
    input_video (str): Path to the input video file.
    output_video (str): Path to the output video file.
    """

    # Get the width and height of the input video
    probe = ffmpeg.probe(input_video)
    video_info = next(
        stream for stream in probe["streams"] if stream["codec_type"] == "video"
    )
    width = int(video_info["width"])
    height = int(video_info["height"])

    # Calculate the new dimensions for a 9:16 aspect ratio
    new_width = width
    new_height = width * 16 // 9  # Adjusted to maintain 9:16 aspect ratio

    # Calculate padding
    pad_top = 0
    pad_bottom = new_height - height
    pad_left = pad_right = 0

    # Pad the video to fit in the upper half of a vertical format
    stream = ffmpeg.input(input_video).filter(
        "pad", new_width, new_height, pad_left, pad_top, color="black"
    )

    stream.output(output_video).run()


def add_video_to_bottom(input_video1, input_video2, output_video):
    """
    Add a second video to the bottom of the first video, maintaining the aspect ratio.

    Parameters:
    input_video1 (str): Path to the first input video (already transformed to upper half).
    input_video2 (str): Path to the second input video to add to the bottom.
    output_video (str): Path to the output video file.
    """

    # Get the width and height of the first input video
    probe = ffmpeg.probe(input_video1)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    width1 = int(video_info['width'])
    height1 = int(video_info['height'])

    # Resize the second video to match the width of the first video while maintaining its aspect ratio
    input2 = ffmpeg.input(input_video2).filter('scale', width1, -1)

    # Get the new height of the second video after scaling
    probe2 = ffmpeg.probe(input_video2, select_streams='v')
    video_info2 = probe2['streams'][0]
    original_width2 = int(video_info2['width'])
    original_height2 = int(video_info2['height'])
    new_height2 = int(original_height2 * width1 / original_width2)

    # Calculate the position for the second video
    x_pos = 0
    y_pos = height1 - new_height2

    # Overlay videos
    input1 = ffmpeg.input(input_video1)
    overlayed = ffmpeg.overlay(input1, input2, x=x_pos, y=y_pos)

    # Output file
    overlayed.output(output_video).run()


if __name__ == "__main__":
    """path = downloadVid()
    print(path)
    duration = 65
    split_video(inputVideoPath=path, segment_duration=duration)"""
    ##center_horizontal_video_in_vertical("ContentCreation/videoDownloads/Uk7qtMV6HUM/parts/part_1.mp4","ContentCreation/videoDownloads/Uk7qtMV6HUM/parts/part_0_resized.mp4")
    add_video_to_bottom(
        "ContentCreation/videoDownloads/Uk7qtMV6HUM/parts/part_0_resized.mp4",
        "ContentCreation/videoDownloads/Uk7qtMV6HUM/parts/part_3.mp4",
        "ContentCreation/videoDownloads/Uk7qtMV6HUM/parts/part_0_resized2.mp4",
    )
