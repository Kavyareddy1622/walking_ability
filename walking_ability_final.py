# -*- coding: utf-8 -*-
"""walking_ability_final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Jt10PFAHL8MkMSvl4Q1qWpAn4sAShcJe
"""

# Install dependencies
!pip install ipywidgets scikit-learn pandas numpy matplotlib seaborn

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display, clear_output

# Load and preprocess data
df = pd.read_csv('simulated_lll_dataset.csv')

# Encode categorical variables
categorical_cols = ['Gender', 'Smoking_Status', 'Diabetes', 'Amputation_Level']
df_encoded = df.copy()
le_dict = {}
for col in categorical_cols:
    le_dict[col] = LabelEncoder()
    df_encoded[col] = le_dict[col].fit_transform(df_encoded[col])

# Split features and target
X = df_encoded.drop('K_Level', axis=1)
y = df_encoded['K_Level']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Model Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Define feature configurations for the form
features = [
    {'name': 'Age', 'type': 'float', 'label': 'Age (18-100)', 'min': 18.0, 'max': 100.0},
    {'name': 'BMI', 'type': 'float', 'label': 'BMI (15-40)', 'min': 15.0, 'max': 40.0},
    {'name': 'Education_Years', 'type': 'float', 'label': 'Education Years (0-20)', 'min': 0.0, 'max': 20.0},
    {'name': 'Balance_Level', 'type': 'float', 'label': 'Balance Level (0-3)', 'min': 0.0, 'max': 3.0},
    {'name': 'Muscle_Strength_RE_Hip', 'type': 'float', 'label': 'Muscle Strength RE Hip (1-5)', 'min': 1.0, 'max': 5.0},
    {'name': 'Muscle_Strength_IE_Hip', 'type': 'float', 'label': 'Muscle Strength IE Hip (1-5)', 'min': 1.0, 'max': 5.0},
    {'name': 'Muscle_Strength_IE_PF', 'type': 'float', 'label': 'Muscle Strength IE PF (1-5)', 'min': 1.0, 'max': 5.0},
    {'name': 'BDI_Score', 'type': 'float', 'label': 'BDI Score (0-63)', 'min': 0.0, 'max': 63.0},
    {'name': 'MSPSS_Score', 'type': 'float', 'label': 'MSPSS Score (1-7)', 'min': 1.0, 'max': 7.0},
    {'name': 'Gender', 'type': 'select', 'label': 'Gender', 'options': ['Select...', 'Male', 'Female']},
    {'name': 'Smoking_Status', 'type': 'select', 'label': 'Smoking Status', 'options': ['Select...', 'Non-Smoker', 'Ex-Smoker', 'Smoker']},
    {'name': 'Diabetes', 'type': 'select', 'label': 'Diabetes', 'options': ['Select...', 'Yes', 'No']},
    {'name': 'Amputation_Level', 'type': 'select', 'label': 'Amputation Level', 'options': ['Select...', 'Transfemoral', 'Transtibial']},
]

# Create input widgets
input_widgets = {}
for feature in features:
    if feature['type'] == 'select':
        input_widgets[feature['name']] = widgets.Dropdown(
            options=feature['options'],
            value='Select...',  # Start with placeholder
            description=feature['label'],
            style={'description_width': 'initial'},
            layout={'width': '500px'}
        )
    else:
        input_widgets[feature['name']] = widgets.BoundedFloatText(
            value=None,  # Blank input
            min=feature['min'],
            max=feature['max'],
            step=0.1,
            description=feature['label'],
            style={'description_width': 'initial'},
            layout={'width': '500px'}
        )

# Create buttons and output area
predict_button = widgets.Button(
    description="Predict K-Level",
    button_style='primary',
    tooltip='Click to predict K-Level',
    layout={'width': '200px', 'margin': '10px'}
)
edit_button = widgets.Button(
    description="Edit Inputs",
    button_style='info',
    tooltip='Click to review and edit inputs',
    layout={'width': '200px', 'margin': '10px'}
)
output = widgets.Output()

# Encode user input (unchanged)
def encode_user_input(user_data):
    user_df = pd.DataFrame([user_data])
    for col in categorical_cols:
        try:
            user_df[col] = le_dict[col].transform(user_df[col])
        except ValueError:
            print(f"Error: Invalid {col} value. Please use one of {le_dict[col].classes_}")
            return None
    return user_df

# Predict and visualize (unchanged)
def predict_and_visualize(user_data, user_df):
    user_df = user_df[X.columns]
    prediction = model.predict(user_df)[0]
    probabilities = model.predict_proba(user_df)[0]

    print(f"\nPredicted K_Level: {prediction}")
    print("K_Level Interpretation:")
    print("1: Limited household ambulation")
    print("2: Limited community ambulation")
    print("3: Full community ambulation")

    plt.figure(figsize=(8, 6))
    sns.barplot(x=['K_Level 1', 'K_Level 2', 'K_Level 3'], y=probabilities, palette='Blues_d')
    plt.title('Probability of Each K_Level')
    plt.ylabel('Probability')
    plt.ylim(0, 1)
    for i, prob in enumerate(probabilities):
        plt.text(i, prob + 0.02, f'{prob:.2f}', ha='center', va='bottom')
    plt.show()

    numeric_cols = ['Age', 'BMI', 'Education_Years', 'Balance_Level',
                    'Muscle_Strength_RE_Hip', 'Muscle_Strength_IE_Hip',
                    'Muscle_Strength_IE_PF', 'BDI_Score', 'MSPSS_Score']

    plt.figure(figsize=(14, 8))
    melted_df = df[numeric_cols].melt()
    sns.boxplot(x='variable', y='value', data=melted_df, color='lightblue')
    for i, col in enumerate(numeric_cols):
        plt.scatter(i, user_data[col], color='red', s=100, label='User Input' if i == 0 else None)
    plt.title('User Input vs. Dataset Distribution (Numeric Features)')
    plt.xlabel('Feature')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='Age', y='BMI', hue='K_Level', palette='Set1', size='K_Level', sizes=(50, 200))
    plt.scatter(user_data['Age'], user_data['BMI'], color='black', s=300, marker='*',
                label='User Input', edgecolor='white')
    plt.title('Age vs. BMI by K_Level (User Input Highlighted)')
    plt.xlabel('Age')
    plt.ylabel('BMI')
    plt.legend(title='K_Level')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Get user input from widgets
def get_user_input_from_widgets():
    user_data = {}
    for feature in features:
        value = input_widgets[feature['name']].value
        if feature['type'] == 'select' and value == 'Select...':
            raise ValueError(f"Please select a valid option for {feature['label']}.")
        if feature['type'] == 'float' and value is None:
            raise ValueError(f"Please enter a value for {feature['label']}.")
        user_data[feature['name']] = value
    return user_data

# Handle predict button click
def on_predict_button_clicked(b):
    with output:
        clear_output()
        try:
            user_data = get_user_input_from_widgets()
            user_df = encode_user_input(user_data)
            if user_df is None:
                print("Prediction aborted due to invalid input.")
                return
            predict_and_visualize(user_data, user_df)
        except Exception as e:
            print(f"Error: {str(e)}")

# Handle edit button click
def on_edit_button_clicked(b):
    with output:
        clear_output()
        user_data = get_user_input_from_widgets()
        print("\nCurrent Input Data:")
        for key, value in user_data.items():
            if value == 'Select...' or value is None:
                print(f"{key}: Not entered")
            else:
                print(f"{key}: {value}")
        print("\nModify the fields above and click 'Predict K-Level' to submit or 'Edit Inputs' to review again.")

# Connect button handlers
predict_button.on_click(on_predict_button_clicked)
edit_button.on_click(on_edit_button_clicked)

# Display the interface
print("Enter Patient Details:")
form = widgets.VBox([widgets.HBox([predict_button, edit_button])] +
                    [input_widgets[feature['name']] for feature in features] +
                    [output])
display(form)