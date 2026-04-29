import cv2
import numpy as np
from flask import Blueprint, request, send_file, jsonify
from deepface import DeepFace
from io import BytesIO

detect_route = Blueprint('detect_route', __name__)

@detect_route.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Analyze faces
    results = DeepFace.analyze(img, actions=['age', 'gender', 'emotion'], enforce_detection=False, detector_backend='opencv')

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
        emotion_text = f"Emotion: {face['dominant_emotion']}"
        predicted_gender = max(gender, key=gender.get)
        confidence = gender[predicted_gender]
        gender_text = f"Gender: {predicted_gender} ({confidence:.2f}%)"

        # Define line spacing
        line_height = 15

        # Draw each line above the rectangle
        cv2.putText(img, emotion_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.putText(img, gender_text, (x, y - 10 - line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.putText(img, age_text, (x, y - 10 - 2 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Convert image to bytes
    _, buffer = cv2.imencode('.jpg', img)
    return send_file(BytesIO(buffer), mimetype='image/jpeg')