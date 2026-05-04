import cv2
import numpy as np
from flask import Blueprint, request, send_file
from deepface import DeepFace
from io import BytesIO

detect_route = Blueprint('detect_route', __name__)

@detect_route.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Analyze faces (now includes race)
    results = DeepFace.analyze(
        img,
        actions=['age', 'gender', 'emotion', 'race'],
        enforce_detection=False,
        detector_backend='mtcnn'
    )

    # Draw bounding boxes
    for face in results:
        x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Prepare individual lines
        age_text = f"Age: {face['age']}"
        gender = face.get('gender', 'Unknown')
        confidence = face.get('gender_confidence', None)

        if confidence is not None:        
            gender_text = f"Gender: {gender} ({confidence:.2f}%)"
        else:
            gender_text = f"Gender: {gender}"
        
        # If DeepFace returns gender as dict, handle predicted gender
        if isinstance(gender, dict):
            predicted_gender = max(gender, key=gender.get)
            confidence = gender[predicted_gender]
            gender_text = f"Gender: {predicted_gender} ({confidence:.2f}%)"
        
        emotion_text = f"Emotion: {face['dominant_emotion']}"

        # Handle race output (DeepFace returns dict of race probabilities)
        race = face.get('race', {})
        if isinstance(race, dict) and race:
            predicted_race = max(race, key=race.get)
            race_confidence = race[predicted_race]
            race_text = f"Race: {predicted_race} ({race_confidence:.2f}%)"
        else:
            race_text = "Race: Unknown"

        # Define line spacing
        line_height = 12

        # Draw each line above the rectangle
        cv2.putText(img, race_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
        cv2.putText(img, emotion_text, (x, y - 10 - line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
        cv2.putText(img, gender_text, (x, y - 10 - 2 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
        cv2.putText(img, age_text, (x, y - 10 - 3 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

    # Convert image to bytes
    _, buffer = cv2.imencode('.jpg', img)
    return send_file(BytesIO(buffer), mimetype='image/jpeg')