# DNA Analyzer – Age • Gender • Emotion • Race Detection

## 📖 Overview
**DNA Analyzer** is a web application that uses **AI-powered face recognition** to detect **Age, Gender, Emotion & Race** in real-time.  
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

## 🚀 Getting Started with localhost 

### 1. Clone the repository
```bash
git clone https://github.com/Prathamesh666/DNA_Scanner
cd DNA_Scanner
```
### 2. Install the requirements
```bash
pip install -r requirements.txt
```

### 3. Run the Web App
```bash
python main.py
```

The app will be available at:
http://localhost:5000 (Flask) 

**Note:** Webcame feature may not work on localhost. 

**Option 1:** You will need to deploy using an instance having VPS Hosting (I used Ezerhost SM 50 VPS Hosting: Self Managed) or render deploy with 1.8GB+ (2GB) RAM for AI models [often expensive about 25$/month and 1 CPU which might work slower].

**Option 2:** Remove the <Video> line in Live web-came section (HTML) & Replace the existing related javascript code **(From line 331 to 377 in `index.html`**) with the given one below to work it in your localhost
'''javascript
toggleBtn.addEventListener('click', () => {
        if (!webcamActive) {
          Webcam.set({ width: 320, height: 240, image_format: 'jpeg', jpeg_quality: 90 });
          Webcam.attach('#camera');
          cameraEl.style.display = 'block';
          captureBtn.style.display = 'inline-block';
          toggleBtn.textContent = 'Stop Webcam';
          webcamActive = true;
        } else {
          Webcam.reset();
          cameraEl.style.display = 'none';
          captureBtn.style.display = 'none';
          toggleBtn.textContent = 'Start Webcam';
          webcamActive = false;
        }
      });

      captureBtn.addEventListener('click', async () => {
        if (!webcamActive) return;
        Webcam.snap(async (data_uri) => {
          try {
            const blob = await (await fetch(data_uri)).blob();
            const formData = new FormData();
            formData.append('image', blob, 'webcam.jpg');
            const res = await fetch('/detect', { method: 'POST', body: formData });
            if (!res.ok) throw new Error(`Server returned ${res.status}`);
            const imgBlob = await res.blob();
            const url = URL.createObjectURL(imgBlob);
            showAnalyzedImage(url); // Use the function to display results with zoomable modal
            // Optionally call onEmotionDetected if server returns emotion in headers or JSON
            // Example: const json = await res.json(); if (json.emotion) window.onEmotionDetected(json.emotion);
          } catch (err) {
            console.error(err);
          }
        });
      });
'''

## 📂 Project Structure
```
DNA_Scanner/
│── routes/              # Core backend file: detect.py
│── static/              # CSS, JS, videos & logos
│── templates/           # HTML template
│── .python-version      # For Render Deploy (3.10.9)
│── deploy.sh            # For Ezerhost SM 50 (Self Managed) Instance Deployment
│── main.py              # Main backend script
│── README.md            # Reasearch Paper
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
│── redeploy.sh          # For Redeployment of latest push updates
│── render.yaml          # For render deploy (Optional)
│── robots.txt           # For Robots of Google Search Console (SEO)
│── sitemap.xml          # For Google Search Console (SEO)
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

**Disclaimer:** This application is intended for **educational/entertainment and demonstration purposes only**.  
It does not replace professional analysis or judgment. Always interpret results responsibly.