from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
from PIL import Image
import os
from transformers import pipeline
import re
from medical_dataset import medical_dataset
import numpy as np

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key here or via environment variable
API_KEY = ENTER_YOUR_API_KEY
openai.api_key = os.getenv('OPENAI_API_KEY', API_KEY)

# Load HuggingFace image classification pipeline
image_classifier = pipeline('image-classification', model='google/vit-base-patch16-224')

# Medical image mapping - maps common image labels to medical conditions
medical_image_mapping = {
    'rash': ['rash', 'skin rash', 'dermatitis', 'eczema', 'psoriasis'],
    'acne': ['acne', 'pimple', 'zit', 'blackhead'],
    'bruise': ['bruise', 'contusion', 'hematoma'],
    'cut': ['cut', 'laceration', 'wound'],
    'burn': ['burn', 'thermal burn', 'chemical burn'],
    'swelling': ['swelling', 'edema', 'inflammation'],
    'redness': ['redness', 'erythema', 'inflammation'],
    'blister': ['blister', 'vesicle', 'bubble'],
    'mole': ['mole', 'nevus', 'skin lesion'],
    'wart': ['wart', 'verruca'],
    'fungal': ['fungal', 'ringworm', 'tinea', 'yeast infection'],
    'allergic': ['allergic', 'hives', 'urticaria', 'allergic reaction'],
    'infection': ['infection', 'bacterial', 'viral', 'infected'],
    'inflammation': ['inflammation', 'swollen', 'red', 'painful']
}

def extract_symptoms_from_text(text):
    """Extract symptoms from text using the dataset"""
    symptoms = []
    text_lower = text.lower()
    
    # Get all available symptoms from dataset
    available_symptoms = medical_dataset.get_all_symptoms()
    
    for symptom in available_symptoms:
        if symptom in text_lower:
            symptoms.append(symptom)
    
    print(symptoms)
    return symptoms

def get_medicine_and_img(illness):
    """Get medicine and image from dataset"""
    illness_data = medical_dataset.get_illness_data(illness.lower())
    if illness_data:
        return illness_data['medicines'], illness_data['img']
    return ['Consult a doctor'], '/static/img/doctor.png'

def analyze_medical_image(image):
    """Analyze medical image and map to medical conditions"""
    try:
        # Use the image classifier
        results = image_classifier(image)
        
        # Get the top predictions
        top_predictions = results[:3]  # Get top 3 predictions
        
        # Map image labels to medical conditions
        detected_conditions = []
        
        for pred in top_predictions:
            label = pred['label'].lower()
            confidence = pred['score']
            
            # Check if the label maps to any medical condition
            for medical_condition, related_terms in medical_image_mapping.items():
                if any(term in label for term in related_terms):
                    detected_conditions.append({
                        'condition': medical_condition,
                        'confidence': confidence,
                        'original_label': label
                    })
        
        # If no medical conditions detected, try to infer from the image
        if not detected_conditions:
            # Use OpenAI to analyze the image description
            image_description = " ".join([pred['label'] for pred in top_predictions])
            
            # Map common image descriptions to symptoms
            if any(term in image_description.lower() for term in ['red', 'rash', 'skin']):
                detected_conditions.append({
                    'condition': 'rash',
                    'confidence': 0.7,
                    'original_label': image_description
                })
            elif any(term in image_description.lower() for term in ['swollen', 'inflammation']):
                detected_conditions.append({
                    'condition': 'swelling',
                    'confidence': 0.7,
                    'original_label': image_description
                })
            elif any(term in image_description.lower() for term in ['cut', 'wound', 'injury']):
                detected_conditions.append({
                    'condition': 'cut',
                    'confidence': 0.7,
                    'original_label': image_description
                })
        
        return detected_conditions, top_predictions
        
    except Exception as e:
        print(f"Error analyzing medical image: {e}")
        return [], []

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    data = request.json
    symptoms_text = data.get('symptoms', '')
    
    if not symptoms_text:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    try:
        # Extract symptoms from text using dataset
        extracted_symptoms = extract_symptoms_from_text(symptoms_text)
        
        if extracted_symptoms:
            # Use dataset to find illness
            result = medical_dataset.get_illness_by_symptoms(extracted_symptoms)
            
            if result:
                illness_data = result['data']
                return jsonify({
                    'illness': result['illness'],
                    'confidence': result['confidence'],
                    'medicine': illness_data['medicines'],
                    'img': illness_data['img'],
                    'severity': illness_data['severity'],
                    'duration': illness_data['duration'],
                    'prevention': illness_data['prevention'],
                    'extracted_symptoms': extracted_symptoms
                })
        else:
            return jsonify({
                'illness': 'unknown',
                'confidence': 0.0,
                'medicine': ['Consult a doctor'],
                'img': '/static/img/doctor.png',
                'extracted_symptoms': extracted_symptoms
            })
        
        # Fallback to OpenAI if no match found in dataset
        prompt = f"A patient describes the following symptoms: {symptoms_text}. What is the most likely illness? Respond with only the illness name, no explanation."
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10
        )
        illness = response.choices[0].message.content.strip().lower()
        medicine, img = get_medicine_and_img(illness)
        
        return jsonify({
            'illness': illness,
            'medicine': medicine,
            'img': img,
            'confidence': 0.5,  # Lower confidence for AI-generated results
            'extracted_symptoms': extracted_symptoms
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    try:
        image = Image.open(file.stream)
        
        # Analyze the medical image
        detected_conditions, top_predictions = analyze_medical_image(image)
        
        if detected_conditions:
            # Get the most confident medical condition
            best_condition = max(detected_conditions, key=lambda x: x['confidence'])
            
            # Map to illness in our dataset
            illness = best_condition['condition']
            
            # Get illness data from dataset
            illness_data = medical_dataset.get_illness_data(illness)
            
            if illness_data:
                return jsonify({
                    'illness': illness,
                    'confidence': best_condition['confidence'],
                    'medicine': illness_data['medicines'],
                    'img': illness_data['img'],
                    'severity': illness_data['severity'],
                    'duration': illness_data['duration'],
                    'prevention': illness_data['prevention'],
                    'detected_conditions': detected_conditions,
                    'image_analysis': top_predictions
                })
            else:
                # If not in dataset, provide generic response
                medicine, img = get_medicine_and_img(illness)
                return jsonify({
                    'illness': illness,
                    'confidence': best_condition['confidence'],
                    'medicine': medicine,
                    'img': img,
                    'detected_conditions': detected_conditions,
                    'image_analysis': top_predictions,
                    'message': 'Condition detected but not in database. Please consult a doctor.'
                })
        else:
            # No medical conditions detected
            return jsonify({
                'illness': 'unknown',
                'confidence': 0.0,
                'medicine': ['Consult a doctor'],
                'img': '/static/img/doctor.png',
                'image_analysis': top_predictions,
                'message': 'No medical conditions detected in the image. Please consult a doctor for proper diagnosis.'
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze_medical_image', methods=['POST'])
def analyze_medical_image_endpoint():
    """Enhanced medical image analysis endpoint"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    try:
        image = Image.open(file.stream)
        
        # Analyze the medical image
        detected_conditions, top_predictions = analyze_medical_image(image)
        
        # Get all possible illnesses based on detected conditions
        possible_illnesses = []
        
        for condition in detected_conditions:
            # Search for illnesses that might match the detected condition
            search_results = medical_dataset.search_illnesses(condition['condition'])
            for result in search_results:
                possible_illnesses.append({
                    'illness': result['illness'],
                    'confidence': condition['confidence'],
                    'data': result['data']
                })
        
        return jsonify({
            'detected_conditions': detected_conditions,
            'possible_illnesses': possible_illnesses,
            'image_analysis': top_predictions,
            'total_detections': len(detected_conditions)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms"""
    try:
        symptoms = medical_dataset.get_all_symptoms()
        return jsonify({
            'symptoms': symptoms,
            'count': len(symptoms)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/illnesses', methods=['GET'])
def get_illnesses():
    """Get all available illnesses"""
    try:
        illnesses = medical_dataset.get_all_illnesses()
        return jsonify({
            'illnesses': illnesses,
            'count': len(illnesses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/illness/<illness_name>', methods=['GET'])
def get_illness_details(illness_name):
    """Get detailed information about a specific illness"""
    try:
        illness_data = medical_dataset.get_illness_data(illness_name)
        if illness_data:
            return jsonify({
                'illness': illness_name,
                'data': illness_data
            })
        else:
            return jsonify({'error': 'Illness not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicine/<medicine_name>', methods=['GET'])
def get_medicine_details(medicine_name):
    """Get detailed information about a specific medicine"""
    try:
        medicine_data = medical_dataset.get_medicine_info(medicine_name)
        if medicine_data:
            return jsonify({
                'medicine': medicine_name,
                'data': medicine_data
            })
        else:
            return jsonify({'error': 'Medicine not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_illnesses():
    """Search illnesses by query"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        results = medical_dataset.search_illnesses(query)
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diagnose', methods=['POST'])
def diagnose_symptoms():
    """Diagnose based on list of symptoms"""
    data = request.json
    symptoms = data.get('symptoms', [])
    
    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    try:
        result = medical_dataset.get_illness_by_symptoms(symptoms)
        if result:
            return jsonify({
                'diagnosis': result,
                'input_symptoms': symptoms
            })
        else:
            return jsonify({
                'diagnosis': None,
                'message': 'No matching illness found for the provided symptoms',
                'input_symptoms': symptoms
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/export', methods=['POST'])
def export_dataset():
    """Export the dataset to JSON"""
    try:
        filename = request.json.get('filename', 'medical_dataset_export.json')
        medical_dataset.export_to_json(filename)
        return jsonify({
            'message': f'Dataset exported to {filename}',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/stats', methods=['GET'])
def get_dataset_stats():
    """Get statistics about the dataset"""
    try:
        stats = {
            'total_symptoms': len(medical_dataset.symptoms_data),
            'total_illnesses': len(medical_dataset.illnesses_data),
            'total_medicines': len(medical_dataset.medicines_data),
            'symptoms': list(medical_dataset.symptoms_data.keys()),
            'illnesses': list(medical_dataset.illnesses_data.keys()),
            'medicines': list(medical_dataset.medicines_data.keys())
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/img', filename)

if __name__ == '__main__':
    app.run(debug=True) 
