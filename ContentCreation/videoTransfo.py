import ffmpeg

def putVideoInTopHalf(input_video, output_video):
    """
    Transform a horizontal video to fit in the upper half of a vertical format using ffmpeg-python.

    Parameters:
    input_video (str): Path to the input video file.
    output_video (str): Path to the output video file.
    """

    