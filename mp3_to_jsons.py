import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import json
import whisper

# Load model (better for your laptop)
model = whisper.load_model("small", device="cpu")

audio_folder = "audios"
output_folder = "jsons"

os.makedirs(output_folder, exist_ok=True)

# Only these two files
target_files = ["12_vid12.mp3", "13_vid13.mp3"]

for audio in target_files:

    audio_path = os.path.join(audio_folder, audio)

    if not os.path.exists(audio_path):
        print(f"{audio} not found. Skipping...")
        continue

    number = audio.split("_")[0]
    title = audio.split("_")[1][:-4]  # remove .mp3

    print("Processing:", audio)

    result = model.transcribe(
        audio_path,
        language="hi",
        task="translate",
        fp16=False
    )

    chunks = []

    # Merge every 3 consecutive segments into one semantic chunk
    window_size = 3
    segments = result["segments"]
    for i in range(0, len(segments), window_size):
        window = segments[i:i + window_size]
        chunks.append({
            "number": number,
            "title": title,
            "start": round(window[0]["start"], 2),
            "end": round(window[-1]["end"], 2),
            "text": " ".join(seg["text"].strip() for seg in window)
        })

    chunks_with_metadata = {
        "chunks": chunks,
        "full_text": result["text"]
    }

    output_file = os.path.join(output_folder, f"{audio}.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks_with_metadata, f, indent=4, ensure_ascii=False)

    print(f"Saved: {output_file}")
