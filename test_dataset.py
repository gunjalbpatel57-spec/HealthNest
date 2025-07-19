#!/usr/bin/env python3
"""
Test script for the medical dataset integration
"""

from medical_dataset import medical_dataset
import json

def test_dataset_functionality():
    print("=== Medical Dataset Test ===\n")
    
    # Test 1: Get all symptoms
    print("1. Available Symptoms:")
    symptoms = medical_dataset.get_all_symptoms()
    print(f"   Total: {len(symptoms)}")
    print(f"   List: {', '.join(symptoms[:5])}...\n")
    
    # Test 2: Get all illnesses
    print("2. Available Illnesses:")
    illnesses = medical_dataset.get_all_illnesses()
    print(f"   Total: {len(illnesses)}")
    print(f"   List: {', '.join(illnesses[:5])}...\n")
    
    # Test 3: Diagnose symptoms
    print("3. Diagnosis Test:")
    test_symptoms = ["fever", "cough", "fatigue"]
    print(f"   Input symptoms: {test_symptoms}")
    result = medical_dataset.get_illness_by_symptoms(test_symptoms)
    if result:
        print(f"   Diagnosis: {result['illness']}")
        print(f"   Confidence: {result['confidence']:.2f}")
        print(f"   Medicines: {result['data']['medicines']}")
        print(f"   Severity: {result['data']['severity']}")
        print(f"   Duration: {result['data']['duration']}\n")
    
    # Test 4: Get illness details
    print("4. Illness Details (flu):")
    flu_data = medical_dataset.get_illness_data("flu")
    if flu_data:
        print(f"   Symptoms: {flu_data['symptoms']}")
        print(f"   Medicines: {flu_data['medicines']}")
        print(f"   Prevention: {flu_data['prevention']}\n")
    
    # Test 5: Search functionality
    print("5. Search Test:")
    search_results = medical_dataset.search_illnesses("headache")
    print(f"   Search for 'headache': {len(search_results)} results")
    for result in search_results:
        print(f"   - {result['illness']}: {result['data']['medicines']}\n")
    
    # Test 6: Medicine information
    print("6. Medicine Information (Paracetamol):")
    med_info = medical_dataset.get_medicine_info("Paracetamol")
    if med_info:
        print(f"   Type: {med_info['type']}")
        print(f"   Dosage: {med_info['dosage']}")
        print(f"   Side Effects: {med_info['side_effects']}")
        print(f"   Price: {med_info['price_range']}\n")
    
    # Test 7: Export dataset
    print("7. Exporting dataset...")
    medical_dataset.export_to_json("test_export.json")
    print("   Dataset exported to test_export.json\n")
    
    print("=== Test Complete ===")

def test_text_analysis():
    print("=== Text Analysis Test ===\n")
    
    # Test symptom extraction from text
    test_texts = [
        "I have a fever and cough with body aches",
        "My head hurts and I feel nauseous",
        "I have a rash on my skin and it's itchy",
        "I'm feeling tired and have a sore throat"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"Test {i}: '{text}'")
        symptoms = medical_dataset.get_all_symptoms()
        extracted = []
        text_lower = text.lower()
        
        for symptom in symptoms:
            if symptom in text_lower:
                extracted.append(symptom)
        
        print(f"   Extracted symptoms: {extracted}")
        
        if extracted:
            result = medical_dataset.get_illness_by_symptoms(extracted)
            if result:
                print(f"   Likely illness: {result['illness']} (confidence: {result['confidence']:.2f})")
            else:
                print("   No matching illness found")
        else:
            print("   No symptoms detected")
        print()

if __name__ == "__main__":
    test_dataset_functionality()
    test_text_analysis() 
