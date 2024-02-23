from youtube_transcript_api import YouTubeTranscriptApi
from typing import Iterator, TextIO
import ffmpeg

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

    write_srt(res, "ContentCreation/subtitles/"+video_id+".srt")



def add_subtitle_frame_by_frame(video_path, subtitle_path, output_path, font='Arial', font_size=24, font_color='white'):
    # Open the subtitle file and read each subtitle
    with open(subtitle_path, 'r') as f:
        content = f.read()
    
    subtitles = content.strip().split('\n\n')
    
    frame_rate = get_frame_rate(video_path)
    
    # Iterate through each subtitle and overlay it on the corresponding frame
    i = 0
    for subtitle in subtitles:
        print(subtitle)
        start_time, end_time, text = parse_subtitle(subtitle)
        
        (
            ffmpeg
            .input(video_path, ss=start_time)
            .output("ContentCreation/tmp/tmp"+str(i)+".mp4", ss=start_time, to=end_time, 
                    vf=f"subtitles={subtitle_path}:force_style='FontName={font},FontSize={font_size}'")
            .run()
        )
        i += 1

def add_subtitle_to_video(video_path, subtitle_path, output_path, font='Arial', font_size=24, font_color='white'):
    (
        ffmpeg
        .input(video_path)
        .output(output_path, vf=f'subtitles={subtitle_path}:force_style=\'FontName={font},FontSize={font_size},PrimaryColour={font_color}\'')
        .run()
    )


def get_frame_rate(video_path):
    probe = ffmpeg.probe(video_path)
    return int(probe['streams'][0]['avg_frame_rate'].split('/')[0])

def parse_subtitle(subtitle):
    print(subtitle)
    parts = subtitle.strip().split('\n')
    start_time, end_time = parts[1].split(' --> ')
    text = '\n'.join(parts[2:])
    return start_time, end_time, text



if __name__ == "__main__":
    ##getTranscript("7ASjZ6NfuA4")
    add_subtitle_to_video("ContentCreation/videoDownloads/QUI EST LE MEURTRIER ? #2 (Murder IRL).mp4/QUI EST LE MEURTRIER  2 (Murder IRL).mp4", "ContentCreation/subtitles/7ASjZ6NfuA4.srt", "ContentCreation/videoDownloads/Le meilleur de Squeezie #1 with subtitles.mp4")