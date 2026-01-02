======================================================================
🔥 FIRE & SMOKE DETECTION MODEL - DEPLOYMENT PACKAGE
======================================================================

MODEL INFORMATION:
----------------------------------------------------------------------
Model Name:           fire_smoke_detection_model
Architecture:         MobileNetV2
Framework:            TensorFlow 2.19.0
Dataset:              FIRE-SMOKE-DATASET
Created:              2026-01-02 04:48:47
Input Size:           224×224×3 (RGB)
Output Classes:       3
Class Names:          Fire, Neutral, Smoke
Class Order:          ALPHABETICAL

PERFORMANCE METRICS:
----------------------------------------------------------------------
Test Accuracy:        93.33%
Test Loss:            0.5065
Test Precision:       93.24%
Test Recall:          92.00%
Best Val Accuracy:    93.33% (epoch 29)
Train-Val Gap:        -4.48%
Overall Rating:       EXCELLENT

PER-CLASS ACCURACY:
----------------------------------------------------------------------
Fire        :  89.00%
Neutral     :  95.00%
Smoke       :  96.00%

TRAINING DETAILS:
----------------------------------------------------------------------
Training Time:        21m 13s
Epochs Completed:     30/30
Best Epoch:           29
Training Samples:     2,700
Validation Samples:   300
Batch Size:           32
Initial LR:           0.001

MODEL FILES:
----------------------------------------------------------------------
1. fire_smoke_detection_model/
   → SavedModel format for Render.com deployment

2. fire_smoke_detection_model.keras (10.59 MB)
   → Keras native format

3. fire_smoke_detection_model.h5 (10.39 MB)
   → H5 format (backup)

4. fire_smoke_detection_model.tflite (2.74 MB)
   → TensorFlow Lite for ESP32/edge devices

5. model_info.json
   → Model metadata in JSON format

6. README.txt (this file)
   → Human-readable documentation

DEPLOYMENT INSTRUCTIONS:
======================================================================

STEP 1: Supabase Setup
----------------------------------------------------------------------
1. Create project at https://supabase.com
2. Create table 'detections':
   - id (uuid, primary key)
   - timestamp (timestamp)
   - class (text)
   - confidence (float)
   - image_url (text)
3. Enable Storage bucket 'fire-images'
4. Note your Supabase URL and API Key

STEP 2: Render.com Deployment
----------------------------------------------------------------------
1. Create GitHub repo with:
   - app.py (Flask API)
   - fire_smoke_detection_model/ (this model)
   - requirements.txt
2. Connect to Render.com
3. Create Web Service
4. Add environment variables:
   - SUPABASE_URL
   - SUPABASE_KEY
5. Deploy!

STEP 3: ESP32-CAM Integration
----------------------------------------------------------------------
1. Update ESP32 code with Render endpoint
2. Hardware detection (MQ-2, KY-026) as primary
3. AI model as secondary confirmation
4. Send alert to Blynk when both detect fire/smoke

API USAGE:
----------------------------------------------------------------------
Endpoint: POST /predict
Content-Type: multipart/form-data
Body: image file (224×224 recommended)

Response:
{
  "class": "Fire",
  "confidence": 0.95,
  "all_predictions": {
    "Fire": 0.XX,
    "Neutral": 0.XX,
    "Smoke": 0.XX
  }
}

PREPROCESSING:
----------------------------------------------------------------------
1. Resize image to 224×224
2. Convert to RGB (if needed)
3. Normalize pixel values to [0, 1] (divide by 255)
4. Add batch dimension: (1, 224, 224, 3)

CONFIDENCE THRESHOLD:
----------------------------------------------------------------------
Recommended: 70% (0.70)
- Fire detected: confidence ≥ 70%
- Combine with hardware sensors for best accuracy

======================================================================
🎉 MODEL READY FOR DEPLOYMENT!
======================================================================
