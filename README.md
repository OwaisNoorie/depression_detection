# depression_detection
Depression Detection System using facial and voice emotion analysis. This AI-powered tool processes user videos to extract facial expressions and vocal cues, classifying the user's mental state as Depressed, Not Depressed, or Undetermined using pretrained models and smart decision logic.

Depression Detection System using Facial & Voice Emotion Analysis

This project is a multimodal Depression Detection System that uses facial expressions and voice emotion analysis to classify individuals as:
- Depressed
- Not Depressed
- or Undetermined

>  Built using TensorFlow, OpenCV, Scikit-learn, and pre-trained models, this system is designed to offer early insights into depressive symptoms using audio-visual data.

---

Project Structure

```plaintext
 depression_detection
├── datasets/
│   ├── AffectNet/
│   ├── rafdb/
│   ├── ravdess/
│   ├── tess/
│   └── cremad/
│
├── models/
│   ├── audio_emotion_model.keras
│   └── mobilenet_affectnet.keras
│
├── facial/
│
├── preprocessed_data/
│   └── frames/
│
├── videos/
│   └── videoplayback.mp4
│
├── results/
│   ├── emotion_predictions.csv
│   ├── cremad_features.csv
│   ├── tess_features.csv
│   ├── ravdess_features.csv
│   ├── train_labels.csv
│   └── val_labels.csv
│
├── notebooks/
│   ├── integ.ipynb
│   ├── facial.ipynb
│   └── voice.ipynb



Datasets used(Taken from Kaggle)
CremaD -- for voice anlysis
AffectNet -- for facial emotion analysis
