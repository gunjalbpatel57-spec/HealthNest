# HealthNest - Medical Dataset Integration

## Overview
HealthNest is a comprehensive medical diagnosis application that integrates a structured medical dataset with AI-powered analysis. The system provides both dataset-driven and AI-powered diagnosis capabilities for various medical conditions.

## Features

### 🏥 Medical Dataset Integration
- **Comprehensive Medical Data**: 10+ symptoms, 10+ illnesses, and 5+ medicines
- **Symptom-Illness Mapping**: Intelligent mapping between symptoms and potential illnesses
- **Medicine Information**: Detailed medicine data including dosage, side effects, and contraindications
- **Confidence Scoring**: Algorithm-based confidence scoring for diagnoses

### 🔍 Analysis Capabilities
- **Text-based Symptom Analysis**: Extract symptoms from natural language and provide diagnosis
- **Image-based Analysis**: Analyze medical images using AI models
- **Direct Symptom Diagnosis**: Diagnose based on selected symptoms
- **Search Functionality**: Search illnesses by name or symptoms

### 📊 API Endpoints
- **RESTful API**: Complete REST API for all dataset operations
- **Real-time Analysis**: Fast response times for medical queries
- **Export/Import**: Dataset export and import capabilities
- **Statistics**: Comprehensive dataset statistics

## Project Structure

```
HealthNest/
├── app.py                 # Main Flask application
├── medical_dataset.py     # Medical dataset module
├── test_dataset.py        # Dataset testing script
├── dataset_test.html      # Web interface for testing
├── requirements.txt       # Python dependencies
├── API_DOCUMENTATION.md   # Complete API documentation
├── README.md             # This file
├── index.html            # Original frontend
├── style.css             # Original styling
└── static/               # Static assets
    └── img/              # Medical condition images
```

## Dataset Structure

### Symptoms Data
Each symptom contains:
- **Associated Illnesses**: List of illnesses that commonly present with this symptom
- **Severity Level**: mild/moderate/severe classification
- **Description**: Detailed description of the symptom

### Illnesses Data
Each illness contains:
- **Symptoms**: List of associated symptoms
- **Medicines**: Recommended treatment medications
- **Severity**: Illness severity classification
- **Duration**: Expected duration of the illness
- **Prevention**: Preventive measures
- **Image**: Associated medical image

### Medicines Data
Each medicine contains:
- **Type**: Medicine classification
- **Dosage**: Recommended dosage information
- **Side Effects**: Potential side effects
- **Contraindications**: Medical contraindications
- **Price Range**: Estimated cost range

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd HealthNest
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Test the dataset**:
```bash
python test_dataset.py
```

## Usage

### Web Interface
1. Open `dataset_test.html` in your browser
2. Use the interface to test all dataset functionality
3. View real-time statistics and analysis results

### API Usage

#### Text-based Symptom Analysis
```python
import requests

response = requests.post('http://localhost:5000/analyze_text', 
                        json={'symptoms': 'I have fever and cough'})
result = response.json()
print(f"Diagnosis: {result['illness']}")
print(f"Confidence: {result['confidence']}")
print(f"Medicines: {result['medicine']}")
```

#### Direct Symptom Diagnosis
```python
response = requests.post('http://localhost:5000/api/diagnose', 
                        json={'symptoms': ['fever', 'cough', 'fatigue']})
result = response.json()
print(f"Diagnosis: {result['diagnosis']['illness']}")
```

#### Get Dataset Statistics
```python
response = requests.get('http://localhost:5000/api/dataset/stats')
stats = response.json()
print(f"Total symptoms: {stats['total_symptoms']}")
print(f"Total illnesses: {stats['total_illnesses']}")
```

### JavaScript Usage
```javascript
// Analyze symptoms
fetch('http://localhost:5000/analyze_text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ symptoms: 'I have fever and cough' })
})
.then(response => response.json())
.then(data => console.log('Diagnosis:', data.illness));

// Get illness details
fetch('http://localhost:5000/api/illness/flu')
.then(response => response.json())
.then(data => console.log('Flu details:', data.data));
```

## API Endpoints

### Core Analysis
- `POST /analyze_text` - Text-based symptom analysis
- `POST /analyze_image` - Image-based analysis
- `POST /api/diagnose` - Direct symptom diagnosis

### Dataset Access
- `GET /api/symptoms` - Get all symptoms
- `GET /api/illnesses` - Get all illnesses
- `GET /api/illness/{name}` - Get illness details
- `GET /api/medicine/{name}` - Get medicine details
- `GET /api/search?q={query}` - Search illnesses

### Dataset Management
- `GET /api/dataset/stats` - Get dataset statistics
- `POST /api/dataset/export` - Export dataset to JSON

## Dataset Content

### Available Symptoms (10)
- fever, cough, headache, fatigue, nausea
- rash, sore_throat, runny_nose, body_aches, diarrhea

### Available Illnesses (10)
- flu, cold, headache, migraine, food_poisoning
- allergic_reaction, eczema, bronchitis, sinusitis, gastritis

### Available Medicines (5)
- Paracetamol, Ibuprofen, Antihistamines
- Decongestants, Corticosteroid creams

## Testing

### Run Dataset Tests
```bash
python test_dataset.py
```

### Test Results Example
```
=== Medical Dataset Test ===

1. Available Symptoms:
   Total: 10
   List: fever, cough, headache, fatigue, nausea...

2. Available Illnesses:
   Total: 10
   List: flu, cold, headache, migraine, food_poisoning...

3. Diagnosis Test:
   Input symptoms: ['fever', 'cough', 'fatigue']
   Diagnosis: flu
   Confidence: 1.00
   Medicines: ['Paracetamol', 'Ibuprofen', 'Rest', 'Fluids']
   Severity: moderate
   Duration: 7-10 days
```

## Key Features

### 🎯 Intelligent Symptom Extraction
- Automatically extracts symptoms from natural language text
- Maps symptoms to potential illnesses using weighted scoring
- Provides confidence levels for diagnoses

### 🔬 Comprehensive Medical Data
- Structured medical knowledge base
- Evidence-based symptom-illness relationships
- Detailed medicine information with safety data

### ⚡ Fast and Reliable
- Dataset-driven analysis for instant results
- AI fallback for complex cases
- Real-time response times

### 📱 Multiple Interfaces
- RESTful API for programmatic access
- Web interface for interactive testing
- Command-line testing tools

## Contributing

### Adding New Data
1. Edit `medical_dataset.py`
2. Add new symptoms, illnesses, or medicines to the respective dictionaries
3. Update the relationships between symptoms and illnesses
4. Test with `test_dataset.py`

### Extending the API
1. Add new endpoints in `app.py`
2. Update `API_DOCUMENTATION.md`
3. Test with the web interface

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **OpenAI**: AI-powered analysis
- **Pillow**: Image processing
- **Transformers**: AI model pipeline
- **Pandas**: Data manipulation
- **Torch**: Deep learning framework

## License

This project is for educational and research purposes. Please consult healthcare professionals for actual medical advice.

## Disclaimer

This application is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with questions about medical conditions.

## Support

For questions or issues:
1. Check the API documentation
2. Run the test scripts
3. Review the dataset structure
4. Consult the web interface for examples 
