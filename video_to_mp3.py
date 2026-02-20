#Converting the videos to mp3
# Converting the videos to numbered mp3 files

import os
import subprocess
video_folder = "Videos"
audio_folder = "audios"
# Create audios folder if not present
os.makedirs(audio_folder, exist_ok=True)
# Get only mp4 files
files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
# 🔹 Sort numerically (very important for vid1 → vid15 order)
files = sorted(files, key=lambda x: int(x.replace("vid", "").replace(".mp4", "")))
for index, file in enumerate(files, start=1):
    file_name = file.replace(".mp4", "")
    number = str(index).zfill(2)   # 01, 02, 03...
    output_name = f"{number}_{file_name}.mp3"
    print("Processing:", output_name)
    subprocess.run([
        "ffmpeg",
        "-i", f"{video_folder}/{file}",
        f"{audio_folder}/{output_name}"
    ])
