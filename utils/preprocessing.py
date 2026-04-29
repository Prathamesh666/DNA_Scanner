import cv2
import numpy as np

def preprocess_face(file):
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    face = cv2.resize(img, (64, 64)) / 255.0
    return np.expand_dims(face, axis=0)

def predict_all(face, models):
    age_model, gender_model, emotion_model = models
    age = int(age_model.predict(face)[0][0])
    gender = 'Male' if gender_model.predict(face)[0][0] > 0.5 else 'Female'
    emotion = ['Happy', 'Sad', 'Angry', 'Neutral'][np.argmax(emotion_model.predict(face))]
    return age, gender, emotion