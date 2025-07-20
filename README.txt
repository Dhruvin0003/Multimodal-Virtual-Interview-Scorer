
# 🧠 Multimodal Interview Scorer

This is an AI-powered multimodal interview scoring system that evaluates candidate responses by analyzing **text**, **audio**, and **facial expressions**. It uses FastAPI as the backend and Streamlit as the frontend.

---

## 🚀 Features

- Upload and analyze interview videos
- Audio scoring using Wav2Vec2 + Librosa (clarity, WPM, pitch, energy, pauses)
- Text scoring using MiniLM embeddings (coherence, sentiment, vocabulary richness)
- Emotion scoring using DeepFace and OpenCV on video frames
- Modular FastAPI backend and Streamlit-based UI

---

## 🗂 Required Directory Structure

Before running the app, create models dir and sample_data dir and make sure the directory structure looks like this:

```
multimodal-interview-scorer/
├── models/
│   ├── wav2vec2/            # Stores Wav2Vec2 model
│   ├── text_similarity/     # Stores MiniLM model
│   └── nltk_data/           # Stores NLTK punkt tokenizer data
├── sample_data/
├──app/
├──frontend/
├──modules/  

---

## 🔻 Model Setup

These models are required and should be **downloaded manually** into the `models/` directory.

### ✅ 1. Wav2Vec2 Model

Download this from Hugging Face and place it in:

```
models/wav2vec2/
```

You can use:

```python
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from huggingface_hub import snapshot_download

snapshot_download("facebook/wav2vec2-base-960h", local_dir="models/wav2vec2")
```

---

### ✅ 2. MiniLM for Text Similarity

This model is used for semantic scoring of transcripts. Place it in:

```
models/text_similarity/
```

Download using:

```python
from huggingface_hub import snapshot_download

snapshot_download("sentence-transformers/all-MiniLM-L6-v2", local_dir="models/text_similarity")
```

---

### ✅ 3. NLTK Tokenizer (Punkt)

Used for sentence splitting in scoring modules. Place the data in:

```
models/nltk_data/tokenizers/punkt/
```

Download using:

```python
import nltk
nltk.download('punkt', download_dir='models/nltk_data')
```

---


## ⚙️ Install & Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run FastAPI backend:
```bash
uvicorn main:app --reload
```

3. Run Streamlit frontend:
```bash
streamlit run app.py
```

---

## 🧠 Tech Stack

- Python, FastAPI, Streamlit
- Transformers, Librosa, NLTK
- Hugging Face, Sentence Transformers
- DeepFace, OpenCV, TensorFlow

---

## 👤 Author

**Dhruvin Dedakiya**  
Generative AI Engineer | NLP + Multimodal AI Developer  
🔗 https://www.linkedin.com/in/dhruvin-dedakiya-4b834a251


