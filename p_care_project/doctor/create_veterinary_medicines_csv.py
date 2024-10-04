import pandas as pd

# Define the data
data = {
    'name': [
        'Frontline', 'Heartgard', 'Cerenia', 'Rimadyl', 'Apoquel', 
        'Metronidazole', 'Revolution', 'Doxycycline', 'Furosemide', 'Benadryl'
    ],
    'dosage': [
        '0.67ml', '1mg', '24mg', '75mg', '16mg', 
        '250mg', '0.25ml', '100mg', '20mg', '25mg'
    ],
    'description': [
        'Used for flea and tick prevention', 
        'Used for heartworm prevention', 
        'Used for nausea and vomiting', 
        'Used for pain and inflammation', 
        'Used for itching and allergies',
        'Used for gastrointestinal infections', 
        'Used for flea, tick, and heartworm prevention',
        'Used for bacterial infections',
        'Used for heart failure and edema',
        'Used for allergic reactions'
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('veterinary_medicines.csv', index=False)

print("CSV file 'veterinary_medicines.csv' has been created.")
