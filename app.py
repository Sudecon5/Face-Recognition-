from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import base64
import threading
import os

app = Flask(__name__)

# Load your face detection model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Global variables for video streaming
camera = None
frame = None
lock = threading.Lock()

def generate_frames():
    global camera, frame, lock
    camera = cv2.VideoCapture(0)
    
    while True:
        success, img = camera.read()
        if not success:
            break
        else:
            with lock:
                # Convert to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Detect faces
                faces = face_cascade.detectMultiScale(gray, 1.5, 4)
                # Draw rectangles around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                
                frame = img.copy()
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', img)
            frame_bytes = buffer.tobytes()
            
            # Yield frame for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect_faces', methods=['POST'])
def detect_faces():
    global frame, lock
    with lock:
        if frame is not None:
            # Convert frame to base64 for JSON response
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                'status': 'success',
                'image': frame_base64
            })
        else:
            return jsonify({'status': 'error', 'message': 'No frame available'})

@app.route('/stop_camera')
def stop_camera():
    global camera
    if camera:
        camera.release()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)