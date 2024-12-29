from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib

FIELD_DESCRIPTIONS = {
    'months_as_customer': {
        'description': 'Duration of customer relationship',
        'range': '1-600 months',
        'typical': '50-300 months'
    },
    'policy_deductable': {
        'description': 'Amount paid before insurance coverage begins',
        'options': [500, 1000, 2000],
        'typical': 1000
    },
    'umbrella_limit': {
        'description': 'Additional liability coverage',
        'range': '0-10,000,000',
        'typical': '0-6,000,000'
    },
    'capital-gains': {
        'description': 'Capital gains from investments',
        'range': '0-100,000',
        'typical': '20,000-70,000'
    },
    'capital-loss': {
        'description': 'Capital losses from investments',
        'range': '-100,000-0',
        'typical': '-70,000-0'
    },
    'incident_hour': {
        'description': 'Hour when incident occurred',
        'range': '0-23',
        'typical': 'Any'
    },
    'vehicles_involved': {
        'description': 'Number of vehicles involved in incident',
        'range': '1-4',
        'typical': '1-2'
    },
    'bodily_injuries': {
        'description': 'Number of bodily injuries',
        'range': '0-2',
        'typical': '0-1'
    },
    'witnesses': {
        'description': 'Number of witnesses',
        'range': '0-3',
        'typical': '1-2'
    },
    'injury_claim': {
        'description': 'Amount claimed for injuries',
        'range': '0-20,000',
        'typical': '500-15,000'
    },
    'property_claim': {
        'description': 'Amount claimed for property damage',
        'range': '0-20,000',
        'typical': '500-15,000'
    },
    'vehicle_claim': {
        'description': 'Amount claimed for vehicle damage',
        'range': '0-80,000',
        'typical': '2,000-60,000'
    }
}

app = Flask(__name__)

# Load the trained model
model = joblib.load('extratrees_model.joblib')

@app.route('/')
def home():
    return render_template('index.html', field_info=FIELD_DESCRIPTIONS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Initialize all columns with zeros
        input_data = {
            'months_as_customer': int(data['months_as_customer']),
            'policy_deductable': int(data['policy_deductable']),
            'umbrella_limit': int(data['umbrella_limit']),
            'capital-gains': float(data['capital-gains']),
            'capital-loss': float(data['capital-loss']),
            'incident_hour_of_the_day': int(data['incident_hour']),
            'number_of_vehicles_involved': int(data['vehicles_involved']),
            'bodily_injuries': int(data['bodily_injuries']),
            'witnesses': int(data['witnesses']),
            'injury_claim': float(data['injury_claim']),
            'property_claim': float(data['property_claim']),
            'vehicle_claim': float(data['vehicle_claim']),
            'policy_csl_250/500': 0,
            'policy_csl_500/1000': 0,
            'insured_sex_MALE': 0,
            'insured_education_level_College': 0,
            'insured_education_level_High School': 0,
            'insured_education_level_JD': 0,
            'insured_education_level_MD': 0,
            'insured_education_level_Masters': 0,
            'insured_education_level_PhD': 0,
            'insured_occupation_armed-forces': 0,
            'insured_occupation_craft-repair': 0,
            'insured_occupation_exec-managerial': 0,
            'insured_occupation_farming-fishing': 0,
            'insured_occupation_handlers-cleaners': 0,
            'insured_occupation_machine-op-inspct': 0,
            'insured_occupation_other-service': 0,
            'insured_occupation_priv-house-serv': 0,
            'insured_occupation_prof-specialty': 0,
            'insured_occupation_protective-serv': 0,
            'insured_occupation_sales': 0,
            'insured_occupation_tech-support': 0,
            'insured_occupation_transport-moving': 0,
            'insured_relationship_not-in-family': 0,
            'insured_relationship_other-relative': 0,
            'insured_relationship_own-child': 0,
            'insured_relationship_unmarried': 0,
            'insured_relationship_wife': 0,
            'incident_type_Parked Car': 0,
            'incident_type_Single Vehicle Collision': 0,
            'incident_type_Vehicle Theft': 0,
            'collision_type_Rear Collision': 0,
            'collision_type_Side Collision': 0,
            'incident_severity_Minor Damage': 0,
            'incident_severity_Total Loss': 0,
            'incident_severity_Trivial Damage': 0,
            'authorities_contacted_Fire': 0,
            'authorities_contacted_Other': 0,
            'authorities_contacted_Police': 0,
            'property_damage_YES': 0,
            'police_report_available_YES': 0
        }
        
        # Set the appropriate binary columns to 1
        input_data[f"policy_csl_{data['policy_csl']}"] = 1
        input_data[f"insured_sex_{data['insured_sex']}"] = 1
        input_data[f"insured_education_level_{data['insured_education']}"] = 1
        input_data[f"insured_occupation_{data['insured_occupation']}"] = 1
        input_data[f"insured_relationship_{data['insured_relationship']}"] = 1
        input_data[f"incident_type_{data['incident_type']}"] = 1
        input_data[f"collision_type_{data['collision_type']}"] = 1
        input_data[f"incident_severity_{data['incident_severity']}"] = 1
        
        # Handle authorities contacted
        if data['authorities_contacted'] != 'None':
            input_data[f"authorities_contacted_{data['authorities_contacted']}"] = 1
            
        # Handle boolean fields
        if data['property_damage'] == 'YES':
            input_data['property_damage_YES'] = 1
        if data['police_report'] == 'YES':
            input_data['police_report_available_YES'] = 1
        
        # Create DataFrame with the correct column order
        df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(df)[0]
        
        # Enhanced response with more details
        result = {
            'success': True,
            'prediction': 'Fraudulent' if prediction == 1 else 'Not Fraudulent',
            'confidence': round(float(model.predict_proba(df)[0][1]) * 100, 2),
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'risk_factors': {
                'high_claim_amount': float(df['vehicle_claim']) > 50000,
                'multiple_vehicles': int(df['number_of_vehicles_involved']) > 1,
                'bodily_injuries': int(df['bodily_injuries']) > 0
            },
            'summary': {
                'total_claim': float(df['vehicle_claim'] + df['property_claim'] + df['injury_claim']),
                'severity': data['incident_severity'],
                'witnesses': int(df['witnesses'])
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
