from django.shortcuts import render
from django.http import JsonResponse
from .models import EmotionModel
from django.conf import settings
import joblib
import os
import soundfile
import numpy as np
import librosa

def extract_feature(file_name, mfcc=True, chroma=True, mel=True):
    with open(file_name, 'rb') as file:
        y, sr = librosa.load(file_name, sr=None)
        
        features = []
        if mfcc:
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Extract 13 MFCC coefficients
            features.extend(np.mean(mfccs, axis=1))
        if chroma:
            chromagram = librosa.feature.chroma_stft(y=y, sr=sr)  # Extract 12 chroma features
            features.extend(np.mean(chromagram, axis=1))
        if mel:
            mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)  # Extract 1 mel feature
            features.extend(np.mean(mel_spectrogram, axis=1))
        
        # Fill the remaining features with zeros to reach 180 features
        remaining_features = 180 - len(features)
        features.extend([0] * remaining_features)
        
        return np.array(features)

def predict_emotion(file_path):
    # Load the model from the .pkl file
    model_path = os.path.join(settings.MODEL_ROOT, 'Emotion_Voice_Detection_Model.pkl')
    model = joblib.load(model_path)

    # Extract features from the audio file
    features = extract_feature(file_path)

    # Perform prediction using the loaded model
    prediction = model.predict(features.reshape(1, -1))

    # Return the predicted emotion
    return prediction[0]



def index(request):
    if request.method == 'POST' and request.FILES['audio_file']:
        audio_file = request.FILES['audio_file']

        # Save the uploaded audio file to a temporary location
        file_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        with open(file_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # Use the predict_emotion function to get the predicted emotion
        predicted_emotion = predict_emotion(file_path)

        # Return the predicted emotion as a JSON response
        return JsonResponse({'predicted_emotion': predicted_emotion})

    return render(request, 'index.html')