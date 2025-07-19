# HealthNest API Documentation

## Overview
HealthNest is a medical diagnosis application that integrates a comprehensive medical dataset with AI-powered analysis. The backend provides both dataset-driven and AI-powered diagnosis capabilities for various medical conditions.

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, no authentication is required for API endpoints.

## Endpoints

### 1. Text-based Symptom Analysis
**POST** `/analyze_text`

Analyzes text input to extract symptoms and provide diagnosis.

**Request Body:**
```json
{
    "symptoms": "I have fever, cough, and body aches"
}
```

**Response:**
```json
{
    "illness": "flu",
    "confidence": 0.8,
    "medicine": ["Paracetamol", "Ibuprofen", "Rest", "Fluids"],
    "img": "/static/img/flu.png",
    "severity": "moderate",
    "duration": "7-10 days",
    "prevention": ["Flu vaccine", "Good hygiene", "Avoid sick people"],
    "extracted_symptoms": ["fever", "cough", "body_aches"]
}
```

### 2. Image-based Analysis
**POST** `/analyze_image`

Analyzes uploaded images for medical conditions with enhanced medical mapping.

**Request:** Multipart form data with image file

**Response:**
```json
{
    "illness": "rash",
    "confidence": 0.85,
    "medicine": ["Moisturizers", "Corticosteroid creams", "Antihistamines"],
    "img": "/static/img/eczema.png",
    "severity": "mild",
    "duration": "Chronic condition",
    "prevention": ["Moisturize regularly", "Avoid triggers", "Gentle skincare"],
    "detected_conditions": [
        {
            "condition": "rash",
            "confidence": 0.85,
            "original_label": "skin rash"
        }
    ],
    "image_analysis": [
        {
            "label": "skin rash",
            "score": 0.85
        }
    ]
}
```

### 3. Enhanced Medical Image Analysis
**POST** `/api/analyze_medical_image`

Provides detailed medical image analysis with multiple condition detection.

**Request:** Multipart form data with image file

**Response:**
```json
{
    "detected_conditions": [
        {
            "condition": "rash",
            "confidence": 0.85,
            "original_label": "skin rash"
        },
        {
            "condition": "inflammation",
            "confidence": 0.72,
            "original_label": "redness"
        }
    ],
    "possible_illnesses": [
        {
            "illness": "eczema",
            "confidence": 0.85,
            "data": {
                "symptoms": ["rash", "itching", "dry_skin", "redness"],
                "medicines": ["Moisturizers", "Corticosteroid creams", "Antihistamines"],
                "severity": "mild",
                "duration": "Chronic condition"
            }
        }
    ],
    "image_analysis": [
        {
            "label": "skin rash",
            "score": 0.85
        }
    ],
    "total_detections": 2
}
```

### 4. Get All Symptoms
**GET** `/api/symptoms`

Returns all available symptoms in the dataset.

**Response:**
```json
{
    "symptoms": ["fever", "cough", "headache", "fatigue", "nausea", ...],
    "count": 10
}
```

### 5. Get All Illnesses
**GET** `/api/illnesses`

Returns all available illnesses in the dataset.

**Response:**
```json
{
    "illnesses": ["flu", "cold", "headache", "migraine", "food_poisoning", ...],
    "count": 10
}
```

### 6. Get Illness Details
**GET** `/api/illness/{illness_name}`

Returns detailed information about a specific illness.

**Response:**
```json
{
    "illness": "flu",
    "data": {
        "symptoms": ["fever", "cough", "fatigue", "body_aches", "headache"],
        "medicines": ["Paracetamol", "Ibuprofen", "Rest", "Fluids"],
        "severity": "moderate",
        "duration": "7-10 days",
        "prevention": ["Flu vaccine", "Good hygiene", "Avoid sick people"],
        "img": "/static/img/flu.png"
    }
}
```

### 7. Get Medicine Details
**GET** `/api/medicine/{medicine_name}`

Returns detailed information about a specific medicine.

**Response:**
```json
{
    "medicine": "Paracetamol",
    "data": {
        "type": "Pain reliever",
        "dosage": "500-1000mg every 4-6 hours",
        "side_effects": ["Nausea", "Liver problems (high doses)"],
        "contraindications": ["Liver disease", "Alcohol abuse"],
        "price_range": "$5-15"
    }
}
```

### 8. Search Illnesses
**GET** `/api/search?q={query}`

Searches for illnesses by name or symptoms.

**Response:**
```json
{
    "query": "headache",
    "results": [
        {
            "illness": "headache",
            "data": { ... }
        },
        {
            "illness": "migraine",
            "data": { ... }
        }
    ],
    "count": 2
}
```

### 9. Diagnose Symptoms
**POST** `/api/diagnose`

Diagnoses based on a list of symptoms.

**Request Body:**
```json
{
    "symptoms": ["fever", "cough", "fatigue"]
}
```

**Response:**
```json
{
    "diagnosis": {
        "illness": "flu",
        "confidence": 0.8,
        "data": { ... }
    },
    "input_symptoms": ["fever", "cough", "fatigue"]
}
```

### 10. Export Dataset
**POST** `/api/dataset/export`

Exports the medical dataset to a JSON file.

**Request Body:**
```json
{
    "filename": "medical_dataset_export.json"
}
```

**Response:**
```json
{
    "message": "Dataset exported to medical_dataset_export.json",
    "filename": "medical_dataset_export.json"
}
```

### 11. Get Dataset Statistics
**GET** `/api/dataset/stats`

Returns statistics about the dataset.

**Response:**
```json
{
    "total_symptoms": 10,
    "total_illnesses": 10,
    "total_medicines": 5,
    "symptoms": ["fever", "cough", "headache", ...],
    "illnesses": ["flu", "cold", "headache", ...],
    "medicines": ["Paracetamol", "Ibuprofen", ...]
}
```

## Medical Image Analysis Features

### Supported Medical Conditions
The image analysis system can detect and map the following medical conditions:

- **Skin Conditions**: rash, acne, eczema, psoriasis, fungal infections
- **Injuries**: cuts, bruises, burns, blisters
- **Inflammation**: swelling, redness, edema
- **Growths**: moles, warts, skin lesions
- **Allergic Reactions**: hives, urticaria, allergic dermatitis
- **Infections**: bacterial, viral, infected wounds

### Image Analysis Process
1. **Image Classification**: Uses Google's Vision Transformer model
2. **Medical Mapping**: Maps generic labels to medical conditions
3. **Condition Detection**: Identifies specific medical conditions
4. **Illness Matching**: Matches conditions to illnesses in the dataset
5. **Treatment Recommendations**: Provides medicines and care instructions

## Dataset Structure

### Symptoms Data
Each symptom contains:
- `illnesses`: List of associated illnesses
- `severity`: Severity level (mild/moderate/severe)
- `description`: Description of the symptom

### Illnesses Data
Each illness contains:
- `symptoms`: List of associated symptoms
- `medicines`: Recommended medicines
- `severity`: Illness severity classification
- `duration`: Expected duration of the illness
- `prevention`: Preventive measures
- `img`: Image path

### Medicines Data
Each medicine contains:
- `type`: Medicine classification
- `dosage`: Recommended dosage information
- `side_effects`: Potential side effects
- `contraindications`: Medical contraindications
- `price_range`: Estimated cost range

## Error Responses

All endpoints return error responses in the following format:

```json
{
    "error": "Error message description"
}
```

Common HTTP status codes:
- `400`: Bad Request (missing parameters)
- `404`: Not Found (resource not found)
- `500`: Internal Server Error

## Usage Examples

### Python Example
```python
import requests

# Analyze text symptoms
response = requests.post('http://localhost:5000/analyze_text', 
                        json={'symptoms': 'I have fever and cough'})
result = response.json()
print(f"Diagnosis: {result['illness']}")

# Analyze medical image
with open('medical_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/analyze_image', files=files)
    result = response.json()
    print(f"Detected condition: {result['illness']}")

# Enhanced image analysis
with open('medical_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/api/analyze_medical_image', files=files)
    result = response.json()
    print(f"Detected conditions: {len(result['detected_conditions'])}")

# Get all symptoms
response = requests.get('http://localhost:5000/api/symptoms')
symptoms = response.json()['symptoms']
print(f"Available symptoms: {symptoms}")
```

### JavaScript Example
```javascript
// Analyze symptoms
fetch('http://localhost:5000/analyze_text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ symptoms: 'I have fever and cough' })
})
.then(response => response.json())
.then(data => console.log('Diagnosis:', data.illness));

// Analyze medical image
const formData = new FormData();
formData.append('image', imageFile);

fetch('http://localhost:5000/analyze_image', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log('Detected condition:', data.illness));

// Get illness details
fetch('http://localhost:5000/api/illness/flu')
.then(response => response.json())
.then(data => console.log('Flu details:', data.data));
```

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Test the dataset:
```bash
python test_dataset.py
```

4. Open the web interface:
```bash
# Open dataset_test.html in your browser
```

The application will be available at `http://localhost:5000`

## Image Analysis Tips

### Best Practices for Medical Images
1. **Good Lighting**: Ensure the image is well-lit and clear
2. **Close-up Shots**: Focus on the affected area
3. **Multiple Angles**: Take images from different angles if needed
4. **High Resolution**: Use high-quality images for better analysis
5. **Clean Background**: Avoid cluttered backgrounds

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- Maximum file size: 10MB

### Analysis Limitations
- The system is for educational purposes only
- Not a substitute for professional medical diagnosis
- Accuracy depends on image quality and condition visibility
- Always consult healthcare professionals for actual medical advice 
