# ============================================================================
# FIRE DETECTION API - FLASK SERVER FOR RENDER.COM
# ============================================================================
# Deploy này lên Render.com để ESP32-CAM có thể gọi API
# Model: Fire, Smoke, Neutral detection
# ============================================================================

from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
from datetime import datetime

app = Flask(__name__)

# ============================================================================
# LOAD MODEL
# ============================================================================
print("🔥 Loading Fire Detection Model...")

# Đường dẫn model (upload folder fire_smoke_ultimate_model/ hoặc fire_smoke_detection_model/)
MODEL_PATH = 'fire_smoke_detection_model'  # Thay tên folder model của bạn

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"✓ Model loaded successfully from {MODEL_PATH}")
    print(f"✓ Model input shape: {model.input_shape}")
    print(f"✓ Model output shape: {model.output_shape}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Class names (PHẢI ĐÚNG THỨ TỰ khi train!)
CLASS_NAMES = ['Fire', 'Neutral', 'Smoke']

# Image preprocessing parameters
IMG_SIZE = 224
CONFIDENCE_THRESHOLD = 0.75  # 75% confidence

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def preprocess_image(image_bytes):
    """
    Preprocess image for model prediction
    Input: Image bytes
    Output: Preprocessed numpy array (1, 224, 224, 3)
    """
    try:
        # Load image from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to 224x224
        img = img.resize((IMG_SIZE, IMG_SIZE))
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Normalize to [0, 1]
        img_array = img_array.astype('float32') / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def get_prediction_details(predictions):
    """
    Extract prediction details with confidence scores
    """
    predictions = predictions[0]  # Remove batch dimension
    
    # Get predicted class
    predicted_idx = np.argmax(predictions)
    predicted_class = CLASS_NAMES[predicted_idx]
    confidence = float(predictions[predicted_idx])
    
    # All class probabilities
    all_predictions = {
        CLASS_NAMES[i]: float(predictions[i]) 
        for i in range(len(CLASS_NAMES))
    }
    
    # Determine if prediction is reliable
    is_reliable = confidence >= CONFIDENCE_THRESHOLD
    
    return {
        'predicted_class': predicted_class,
        'confidence': confidence,
        'is_reliable': is_reliable,
        'all_predictions': all_predictions,
        'threshold': CONFIDENCE_THRESHOLD
    }

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'online',
        'service': 'Fire & Smoke Detection API',
        'version': '3.0',
        'model_status': 'loaded' if model else 'error',
        'classes': CLASS_NAMES,
        'confidence_threshold': CONFIDENCE_THRESHOLD,
        'endpoints': {
            'predict': '/predict (POST)',
            'health': '/ (GET)'
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint
    
    Request:
        - Method: POST
        - Content-Type: multipart/form-data
        - Body: image file
    
    Response:
        {
            "success": true,
            "predicted_class": "Fire",
            "confidence": 0.95,
            "is_reliable": true,
            "all_predictions": {
                "Fire": 0.95,
                "Neutral": 0.03,
                "Smoke": 0.02
            },
            "alert_level": "HIGH",
            "message": "DANGER: Fire detected with high confidence!",
            "timestamp": "2024-01-15 10:30:45"
        }
    """
    
    # Check if model is loaded
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded',
            'message': 'Server error - model initialization failed'
        }), 500
    
    # Check if image is in request
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image provided',
            'message': 'Please send an image file with key "image"'
        }), 400
    
    try:
        # Get image file
        image_file = request.files['image']
        image_bytes = image_file.read()
        
        # Preprocess image
        img_array = preprocess_image(image_bytes)
        
        if img_array is None:
            return jsonify({
                'success': False,
                'error': 'Image preprocessing failed',
                'message': 'Unable to process the image'
            }), 400
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        
        # Get detailed results
        result = get_prediction_details(predictions)
        
        # Determine alert level
        predicted_class = result['predicted_class']
        confidence = result['confidence']
        
        if predicted_class == 'Fire' and confidence >= CONFIDENCE_THRESHOLD:
            alert_level = 'HIGH'
            message = f'🔥 DANGER: Fire detected with {confidence*100:.1f}% confidence!'
        elif predicted_class == 'Smoke' and confidence >= CONFIDENCE_THRESHOLD:
            alert_level = 'MEDIUM'
            message = f'💨 WARNING: Smoke detected with {confidence*100:.1f}% confidence!'
        elif predicted_class == 'Neutral' and confidence >= CONFIDENCE_THRESHOLD:
            alert_level = 'SAFE'
            message = f'✅ SAFE: No fire or smoke detected ({confidence*100:.1f}% confidence)'
        else:
            alert_level = 'UNCERTAIN'
            message = f'⚠️ UNCERTAIN: Low confidence prediction ({confidence*100:.1f}%)'
        
        # Build response
        response = {
            'success': True,
            'predicted_class': predicted_class,
            'confidence': confidence,
            'is_reliable': result['is_reliable'],
            'all_predictions': result['all_predictions'],
            'alert_level': alert_level,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'threshold': CONFIDENCE_THRESHOLD
        }
        
        # Log prediction
        print(f"[{response['timestamp']}] Prediction: {predicted_class} ({confidence*100:.1f}%) - {alert_level}")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({
            'success': False,
            'error': 'Prediction failed',
            'message': str(e)
        }), 500

@app.route('/test', methods=['GET'])
def test():
    """
    Test endpoint with dummy data
    """
    return jsonify({
        'message': 'API is working!',
        'model_loaded': model is not None,
        'classes': CLASS_NAMES,
        'test_prediction': 'Send POST request to /predict with an image'
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'Available endpoints: / (GET), /predict (POST), /test (GET)'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(error)
    }), 500

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    # Render.com will use PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print("🔥 FIRE DETECTION API SERVER")
    print("="*60)
    print(f"Model: {MODEL_PATH}")
    print(f"Classes: {CLASS_NAMES}")
    print(f"Confidence threshold: {CONFIDENCE_THRESHOLD}")
    print(f"Port: {port}")
    print("="*60 + "\n")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)