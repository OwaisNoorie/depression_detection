import os
import cv2
import numpy as np
import librosa
import tensorflow as tf
from moviepy.editor import VideoFileClip

# Load models
audio_model = tf.keras.models.load_model("../models/audio_emotion_model.keras")
facial_model = tf.keras.models.load_model("../models/mobilenet_affectnet.keras")

# Emotion Mapping
label_map = {0: "negative", 1: "positive"}

def extract_audio_features(video_path):
    try:
        clip = VideoFileClip(video_path)
        audio_path = video_path.replace(".mp4", ".wav")
        clip.audio.write_audiofile(audio_path, verbose=False, logger=None)

        y, sr = librosa.load(audio_path)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)
        os.remove(audio_path)

        return mfcc_processed.reshape(1, -1)
    except Exception as e:
        print("Audio extraction failed:", e)
        return None

def extract_first_face_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    if success:
        resized = cv2.resize(frame, (224, 224))
        normalized = resized / 255.0
        cap.release()
        return np.expand_dims(normalized, axis=0)
    cap.release()
    return None

def analyze_emotion(video_path):
    result = {}

    # Facial
    face_frame = extract_first_face_frame(video_path)
    if face_frame is not None:
        facial_pred = facial_model.predict(face_frame, verbose=0)
        facial_result = np.argmax(facial_pred)
        result["facial_expression"] = label_map[facial_result]
    else:
        result["facial_expression"] = "unknown"

    # Audio
    audio_features = extract_audio_features(video_path)
    if audio_features is not None:
        audio_pred = audio_model.predict(audio_features, verbose=0)
        audio_result = np.argmax(audio_pred)
        result["voice_emotion"] = label_map[audio_result]
    else:
        result["voice_emotion"] = "unknown"

    # Final depression logic
    f = result["facial_expression"]
    v = result["voice_emotion"]

    if f == "negative" and v == "negative":
        result["final_result"] = "Depressed"
    elif f == "positive" and v == "positive":
        result["final_result"] = "Not Depressed"
    else:
        result["final_result"] = "Cannot be determined"

    return result
