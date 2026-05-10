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

        # Prepare text lines
        lines = [race_text, emotion_text, gender_text, age_text]
        
        for i, text in enumerate(lines):
            # Compute text position
            text_x = x
            text_y = y - 10 - i * line_height
        
            # Estimate background box size for text
            (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.3, 1)
            box_x1, box_y1 = text_x, text_y - text_h - baseline
            box_x2, box_y2 = text_x + text_w, text_y + baseline
        
            # Clip coordinates to image bounds
            box_x1 = max(box_x1, 0)
            box_y1 = max(box_y1, 0)
            box_x2 = min(box_x2, img.shape[1])
            box_y2 = min(box_y2, img.shape[0])
        
            # Extract ROI and apply Gaussian blur
            roi = img[box_y1:box_y2, box_x1:box_x2]
            if roi.size > 0:
                blurred_roi = cv2.GaussianBlur(roi, (9, 9), 0)
                img[box_y1:box_y2, box_x1:box_x2] = blurred_roi
        
            # Draw text on top of blurred background
            cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
    # Convert image to bytes
    _, buffer = cv2.imencode('.jpg', img)
    return send_file(BytesIO(buffer), mimetype='image/jpeg')