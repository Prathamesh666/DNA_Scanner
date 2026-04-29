# DNA Analyzer – Age • Gender • Emotion Detection

## 📖 Overview
**DNA Analyzer** is a web application that uses **AI-powered face recognition** to detect **Age, Gender, and Emotion** in real-time.  
The app combines a futuristic **DNA-inspired UI** with computer vision models, allowing users to upload an image or use their webcam for instant analysis.

---

## ✨ Features
- 🔬 **Face Recognition** – Detects faces in uploaded images or live webcam feed.
- 📊 **Age Estimation** – Predicts approximate age range.
- 🧑 **Gender Classification** – Identifies male/female.
- 😀 **Emotion Detection** – Recognizes emotions such as happy, sad, angry, surprised, neutral.
- 🎨 **Glassmorphism UI** – Stylish frosted glass containers with gradient text.
- 🎥 **Responsive Video Backgrounds** – Triple video layout (side-by-side on desktop, stacked on mobile).

---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS (Flexbox, Glassmorphism, Gradient Text)
- **Backend:** Python (Flask / FastAPI)
- **AI Models:** OpenCV, DeepFace / custom CNN models
- **UI Enhancements:** Orbitron & Poppins fonts, responsive design
- **Deployment:** Vercel / Streamlit / Localhost

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Prathamesh666/DNA-Analyzer
cd dna-analyzer
```
### 2. Install the requirements
```pip install -r requirements.txt
```

### 3. Run the Web App
```python main.py
```

The app will be available at:
http://localhost:5000 (Flask) 

## 📂 Project Structure
```
dna-analyzer/
│── static/              # CSS, JS, videos
│── templates/           # HTML templates
│── models/              # Pre-trained AI models
│── app.py               # Main backend script
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
```

🎬 Usage
1. Upload Image – Select an image file and click Detect.

2. Live Webcam – Start webcam to analyze faces in real-time.

3. Results Panel – Displays detected age, gender, and emotion.

🧑‍💻 Author
Developed by Prathamesh  
For research, learning, and demonstration of AI-powered facial analytics.

## ⚠️ Important Notice on Model Predictions

The predictions provided by **DNA Analyzer** are generated using AI models trained on publicly available datasets.  
Results are **probabilistic estimates**, not absolute truths. Accuracy depends on several factors:

- ✅ **Image Quality** – Clear, well-lit images with unobstructed faces yield better predictions.  
- ✅ **Face Visibility** – Ensure the face is front-facing and not partially hidden.  
- ✅ **Context** – The model is designed for general use; cultural, stylistic, or environmental factors may affect results.  
- ✅ **Webcam Use** – For real-time detection, maintain stable lighting and avoid motion blur.  

### 🔹 Guidelines for Genuine Results
1. Upload high-resolution images with a single, clearly visible face.  
2. Avoid extreme angles, heavy makeup, masks, or accessories that obscure facial features.  
3. Use consistent lighting — natural or soft indoor light works best.  
4. Remember: predictions are **approximations** and should not be used for medical, legal, or critical decision-making.  

---

**Disclaimer:** This application is intended for **educational and demonstration purposes only**.  
It does not replace professional analysis or judgment. Always interpret results responsibly.
