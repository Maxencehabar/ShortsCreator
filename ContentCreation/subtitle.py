from youtube_transcript_api import YouTubeTranscriptApi
from typing import Iterator, TextIO


def write_srt(subtitles, output_file):
    with open(output_file, 'w') as f:
        count = 1
        for subtitle in subtitles:
            start_time = subtitle['start']
            end_time = start_time + subtitle['duration']
            start_time_str = '{:02d}:{:02d}:{:02.3f}'.format(int(start_time // 3600), int((start_time % 3600) // 60), start_time % 60)
            end_time_str = '{:02d}:{:02d}:{:02.3f}'.format(int(end_time // 3600), int((end_time % 3600) // 60), end_time % 60)

            f.write(str(count) + '\n')
            f.write(start_time_str + ' --> ' + end_time_str + '\n')
            f.write(subtitle['text'] + '\n')
            f.write('\n')

            count += 1

def getTranscript(video_id):
    try:
        res = YouTubeTranscriptApi.get_transcript(video_id, languages=["fr"])
        
        
    except Exception as e:
        print("Error : ", e)
        return None

    write_srt(res, "subtitles.srt")


if __name__ == "__main__":
    getTranscript("7ASjZ6NfuA4")
