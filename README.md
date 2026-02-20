# 🎓 RAG AI Teaching Assistant (Fully Local)

A fully local, end-to-end Retrieval-Augmented Generation (RAG) pipeline designed as an AI teaching assistant for the Sigma Web Development course.

Students submit natural language questions.  
The system retrieves relevant lecture transcript segments and generates a grounded answer citing:

- 📺 Video number
- ⏱ Timestamp range

Runs 100% offline — no cloud APIs required.

---

## 🧠 Executive Summary

This project demonstrates a practical, modular RAG architecture built for:

- Resource-constrained environments
- Fully offline operation
- Privacy-focused AI systems
- Educational use cases

It integrates:

- Video processing
- Whisper-based speech recognition
- Dense vector retrieval (BGE-M3)
- Cosine similarity search
- Local LLM inference (Llama 3.2 via Ollama)

---

## 🏗 Pipeline Architecture

Videos (.mp4)
      ↓
video_to_mp3.py
      ↓
MP3 audio files
      ↓
mp3_to_jsons.py (Whisper + Semantic Chunking)
      ↓
Chunked JSON transcripts
      ↓
pre_processesed_json.py (BGE-M3 Embeddings)
      ↓
embeddings.joblib (Vector Store)
      ↓
process_incoming.py
      ↓
Top-K Retrieval + Llama 3.2
      ↓
Timestamp-Grounded Answer

---

## 📁 Project Structure

RAG-based-ai/
├── Videos/                  # 15 raw lecture MP4 files  
├── audios/                  # Converted MP3 files  
├── jsons/                   # Whisper-generated transcripts  
├── video_to_mp3.py          # Stage 1: Video → Audio  
├── mp3_to_jsons.py          # Stage 2: Audio → Chunked JSON  
├── pre_processesed_json.py  # Stage 3: JSON → Embeddings  
├── process_incoming.py      # Stage 4: Query → Retrieval → Answer  
├── embeddings.joblib        # Serialized embedding store  
├── embeddings.csv           # CSV export (debug)  
├── prompt.txt               # Last prompt (debug)  
├── response.txt             # Last response (debug)  
├── README.md  
└── .gitignore  

Total lecture footage: ~320 MB  
Currently processed: 2 / 15 videos  

---

## 🔍 Stage Breakdown

### 1️⃣ Video → Audio
File: video_to_mp3.py  
- Converts .mp4 files to .mp3  
- Uses ffmpeg  
- Ensures correct numeric sorting (vid1–vid15)  

---

### 2️⃣ Audio → Transcript + Semantic Chunking
File: mp3_to_jsons.py  

- Whisper model: small (CPU mode)  
- Language: Hindi → Translated to English  
- Timestamp-aware transcription  
- Window-based chunk merging (3 segments per chunk)  

Why chunk merging?

Raw Whisper segments are very short (1–3 seconds).  
The system merges every 3 segments into one semantic chunk.

This improves:
- Semantic coherence  
- Embedding quality  
- Retrieval accuracy  

---

### 3️⃣ Transcript → Embeddings
File: pre_processesed_json.py  

- Embedding model: BGE-M3  
- Served locally via Ollama  
- Stored in Pandas DataFrame  
- Serialized using joblib  

Each row contains:
- Video number  
- Title  
- Start time  
- End time  
- Text  
- Embedding vector  

---

### 4️⃣ Query → Retrieval → Grounded Response
File: process_incoming.py  

Steps:
1. User submits question  
2. Question is embedded  
3. Cosine similarity retrieves top 5 chunks  
4. Structured prompt sent to Llama 3.2  
5. Model generates timestamp-grounded answer  

Example output:

"The exercise is mentioned in video 13 at 481.04 – 482.04 seconds. Please watch that segment."

---

## 🧰 Technology Stack

Video Processing: ffmpeg  
Transcription: Whisper (small)  
Embeddings: BGE-M3  
LLM: Llama 3.2  
Runtime: Ollama (localhost)  
Retrieval: sklearn cosine_similarity  
Storage: Pandas + joblib  
Language: Python 3.x  

---

## 💪 Strengths

- Fully offline & private  
- Modular 4-stage pipeline  
- Smart semantic chunking  
- Timestamp-grounded responses  
- Multilingual support (Hindi → English)  
- Debug-friendly (prompt & response saved)  
- Clean separation of responsibilities  

---

## ⚠️ Current Limitations

- Only 2 / 15 videos processed  
- No Ollama health-check  
- No incremental embedding updates  
- Single-turn Q&A only  
- No relevance threshold filtering  
- No requirements.txt yet  

---

## 🚀 Recommended Improvements

High Priority:
- Process all 15 videos  
- Add requirements.txt  
- Add Ollama connectivity check  

Medium Priority:
- Add similarity threshold filtering  
- Support incremental embedding updates  
- Add simple CLI or Web UI  

Nice to Have:
- Multi-turn conversation support  
- FastAPI or Gradio interface  
- Vector database (FAISS) for scaling  

---

## 📊 Completion Status

Video → MP3          ✅ Complete  
MP3 → JSON           ⚠ Partial (2/15)  
JSON → Embeddings    ⚠ Partial  
Query → Answer       ✅ Functional  

---

## 🎯 What This Project Demonstrates

- Practical RAG implementation  
- Local LLM deployment  
- Applied NLP  
- Embedding-based retrieval  
- System design thinking  
- Privacy-focused AI architecture  
- Resource-aware ML engineering  

---

This project serves as a foundation for building:

- AI Teaching Assistants  
- Private Knowledge Systems  
- Offline AI Applications  
- Educational RAG Systems  
