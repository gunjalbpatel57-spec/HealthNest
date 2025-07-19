import json
import pandas as pd
from typing import Dict, List, Optional

class MedicalDataset:
    def __init__(self):
        self.symptoms_data = {
            "fever": {
                "illnesses": ["flu", "cold", "covid", "infection", "malaria"],
                "severity": "moderate",
                "description": "Elevated body temperature above normal range"
            },
            "cough": {
                "illnesses": ["cold", "flu", "bronchitis", "covid", "pneumonia"],
                "severity": "moderate",
                "description": "Sudden expulsion of air from the lungs"
            },
            "headache": {
                "illnesses": ["migraine", "tension_headache", "sinusitis", "dehydration"],
                "severity": "mild",
                "description": "Pain in the head or upper neck"
            },
            "fatigue": {
                "illnesses": ["flu", "covid", "anemia", "depression", "sleep_disorder"],
                "severity": "moderate",
                "description": "Extreme tiredness and lack of energy"
            },
            "nausea": {
                "illnesses": ["food_poisoning", "migraine", "pregnancy", "gastritis"],
                "severity": "moderate",
                "description": "Feeling of sickness with urge to vomit"
            },
            "rash": {
                "illnesses": ["allergic_reaction", "eczema", "psoriasis", "measles"],
                "severity": "mild",
                "description": "Red, itchy patches on the skin"
            },
            "sore_throat": {
                "illnesses": ["cold", "flu", "strep_throat", "tonsillitis"],
                "severity": "moderate",
                "description": "Pain or irritation in the throat"
            },
            "runny_nose": {
                "illnesses": ["cold", "allergies", "sinusitis"],
                "severity": "mild",
                "description": "Excess nasal discharge"
            },
            "body_aches": {
                "illnesses": ["flu", "covid", "fibromyalgia"],
                "severity": "moderate",
                "description": "Generalized muscle and joint pain"
            },
            "diarrhea": {
                "illnesses": ["food_poisoning", "gastroenteritis", "ibs"],
                "severity": "moderate",
                "description": "Loose, watery stools"
            }
        }
        
        self.illnesses_data = {
            "flu": {
                "symptoms": ["fever", "cough", "fatigue", "body_aches", "headache"],
                "medicines": ["Paracetamol", "Ibuprofen", "Rest", "Fluids"],
                "severity": "moderate",
                "duration": "7-10 days",
                "prevention": ["Flu vaccine", "Good hygiene", "Avoid sick people"],
                "img": "/static/img/flu.png"
            },
            "cold": {
                "symptoms": ["runny_nose", "sore_throat", "cough", "congestion"],
                "medicines": ["Decongestants", "Antihistamines", "Rest", "Fluids"],
                "severity": "mild",
                "duration": "3-7 days",
                "prevention": ["Good hygiene", "Vitamin C", "Adequate sleep"],
                "img": "/static/img/cold.png"
            },
            "headache": {
                "symptoms": ["headache", "sensitivity_to_light", "nausea"],
                "medicines": ["Ibuprofen", "Paracetamol", "Rest", "Hydration"],
                "severity": "mild",
                "duration": "Few hours to days",
                "prevention": ["Stress management", "Regular sleep", "Eye care"],
                "img": "/static/img/headache.png"
            },
            "migraine": {
                "symptoms": ["severe_headache", "nausea", "sensitivity_to_light", "aura"],
                "medicines": ["Triptans", "Pain relievers", "Anti-nausea medication"],
                "severity": "severe",
                "duration": "4-72 hours",
                "prevention": ["Identify triggers", "Regular sleep", "Stress management"],
                "img": "/static/img/migraine.png"
            },
            "food_poisoning": {
                "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal_pain", "fever"],
                "medicines": ["Oral rehydration", "Anti-diarrheal", "Rest"],
                "severity": "moderate",
                "duration": "1-3 days",
                "prevention": ["Food safety", "Proper cooking", "Hand hygiene"],
                "img": "/static/img/food_poisoning.png"
            },
            "allergic_reaction": {
                "symptoms": ["rash", "itching", "swelling", "difficulty_breathing"],
                "medicines": ["Antihistamines", "Epinephrine (severe cases)", "Corticosteroids"],
                "severity": "moderate",
                "duration": "Hours to days",
                "prevention": ["Avoid allergens", "Carry epinephrine", "Medical alert bracelet"],
                "img": "/static/img/allergy.png"
            },
            "eczema": {
                "symptoms": ["rash", "itching", "dry_skin", "redness"],
                "medicines": ["Moisturizers", "Corticosteroid creams", "Antihistamines"],
                "severity": "mild",
                "duration": "Chronic condition",
                "prevention": ["Moisturize regularly", "Avoid triggers", "Gentle skincare"],
                "img": "/static/img/eczema.png"
            },
            "bronchitis": {
                "symptoms": ["cough", "mucus", "chest_discomfort", "fatigue"],
                "medicines": ["Cough suppressants", "Expectorants", "Rest", "Fluids"],
                "severity": "moderate",
                "duration": "1-3 weeks",
                "prevention": ["Avoid smoking", "Good hygiene", "Vaccination"],
                "img": "/static/img/bronchitis.png"
            },
            "sinusitis": {
                "symptoms": ["headache", "runny_nose", "congestion", "facial_pain"],
                "medicines": ["Decongestants", "Saline nasal spray", "Pain relievers"],
                "severity": "moderate",
                "duration": "1-2 weeks",
                "prevention": ["Good hygiene", "Humidifier", "Avoid allergens"],
                "img": "/static/img/sinusitis.png"
            },
            "gastritis": {
                "symptoms": ["nausea", "abdominal_pain", "bloating", "loss_of_appetite"],
                "medicines": ["Antacids", "Proton pump inhibitors", "Diet modification"],
                "severity": "moderate",
                "duration": "Days to weeks",
                "prevention": ["Avoid spicy foods", "Limit alcohol", "Manage stress"],
                "img": "/static/img/gastritis.png"
            }
        }
        
        self.medicines_data = {
            "Paracetamol": {
                "type": "Pain reliever",
                "dosage": "500-1000mg every 4-6 hours",
                "side_effects": ["Nausea", "Liver problems (high doses)"],
                "contraindications": ["Liver disease", "Alcohol abuse"],
                "price_range": "$5-15"
            },
            "Ibuprofen": {
                "type": "NSAID",
                "dosage": "200-400mg every 4-6 hours",
                "side_effects": ["Stomach upset", "Kidney problems"],
                "contraindications": ["Stomach ulcers", "Kidney disease"],
                "price_range": "$8-20"
            },
            "Antihistamines": {
                "type": "Allergy medication",
                "dosage": "As directed on package",
                "side_effects": ["Drowsiness", "Dry mouth"],
                "contraindications": ["Glaucoma", "Prostate problems"],
                "price_range": "$10-25"
            },
            "Decongestants": {
                "type": "Nasal decongestant",
                "dosage": "As directed on package",
                "side_effects": ["Insomnia", "Increased blood pressure"],
                "contraindications": ["High blood pressure", "Heart disease"],
                "price_range": "$8-18"
            },
            "Corticosteroid creams": {
                "type": "Topical steroid",
                "dosage": "Apply thin layer 1-2 times daily",
                "side_effects": ["Skin thinning", "Discoloration"],
                "contraindications": ["Skin infections", "Open wounds"],
                "price_range": "$15-35"
            }
        }

    def get_illness_by_symptoms(self, symptoms: List[str]) -> Dict:
        """Find the most likely illness based on symptoms"""
        illness_scores = {}
        
        for symptom in symptoms:
            if symptom.lower() in self.symptoms_data:
                for illness in self.symptoms_data[symptom.lower()]["illnesses"]:
                    if illness in illness_scores:
                        illness_scores[illness] += 1
                    else:
                        illness_scores[illness] = 1
        
        if not illness_scores:
            return None
            
        # Get the illness with the highest score
        most_likely_illness = max(illness_scores, key=illness_scores.get)
        
        if most_likely_illness in self.illnesses_data:
            return {
                "illness": most_likely_illness,
                "confidence": illness_scores[most_likely_illness] / len(symptoms),
                "data": self.illnesses_data[most_likely_illness]
            }
        
        return None

    def get_illness_data(self, illness: str) -> Optional[Dict]:
        """Get complete data for a specific illness"""
        return self.illnesses_data.get(illness.lower())

    def get_medicine_info(self, medicine: str) -> Optional[Dict]:
        """Get detailed information about a medicine"""
        return self.medicines_data.get(medicine)

    def get_all_symptoms(self) -> List[str]:
        """Get list of all available symptoms"""
        return list(self.symptoms_data.keys())

    def get_all_illnesses(self) -> List[str]:
        """Get list of all available illnesses"""
        return list(self.illnesses_data.keys())

    def search_illnesses(self, query: str) -> List[Dict]:
        """Search illnesses by name or symptoms"""
        results = []
        query = query.lower()
        
        for illness, data in self.illnesses_data.items():
            if query in illness or any(query in symptom for symptom in data["symptoms"]):
                results.append({
                    "illness": illness,
                    "data": data
                })
        
        return results

    def export_to_json(self, filename: str = "medical_dataset.json"):
        """Export the dataset to a JSON file"""
        export_data = {
            "symptoms": self.symptoms_data,
            "illnesses": self.illnesses_data,
            "medicines": self.medicines_data
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)

    def load_from_json(self, filename: str = "medical_dataset.json"):
        """Load dataset from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.symptoms_data = data.get("symptoms", {})
                self.illnesses_data = data.get("illnesses", {})
                self.medicines_data = data.get("medicines", {})
        except FileNotFoundError:
            print(f"Dataset file {filename} not found. Using default dataset.")

# Create a global instance
medical_dataset = MedicalDataset() 
