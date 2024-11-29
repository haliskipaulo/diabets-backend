from flask import Flask, render_template, request, jsonify
from joblib import load
import pandas as pd

app = Flask(__name__)



label_encoders = {
    'Family History': load('./joblibs/Family_History_label_encoder.joblib'),
    'Physical Activity': load('./joblibs/Physical_Activity_label_encoder.joblib'),
    'Dietary Habits': load('./joblibs/Dietary_Habits_label_encoder.joblib'),
    'Socioeconomic Factors': load('./joblibs/Socioeconomic_Factors_label_encoder.joblib'),
    'Smoking Status': load('./joblibs/Smoking_Status_label_encoder.joblib'),
    'Alcohol Consumption': load('./joblibs/Alcohol_Consumption_label_encoder.joblib'),
    'Steroid Use History': load('./joblibs/Steroid_Use_History_label_encoder.joblib'),
    'Liver Function Tests': load('./joblibs/Liver_Function_Tests_label_encoder.joblib'),
}

selected_columns = ['Family History', 'Age', 'BMI', 'Physical Activity', 
                    'Dietary Habits', 'Socioeconomic Factors', 
                    'Smoking Status', 'Alcohol Consumption', 
                    'Steroid Use History', 'Liver Function Tests']

scaler = load('./joblibs/scaler.joblib')


@app.route('/')
def home():
    return render_template('home.html') 


@app.route('/graficos')
def graficos():
    return render_template('graficos.html')  


def prediction(df, model_path="./joblibs/random_forest_model.joblib", label_encoders=label_encoders, scaler=scaler, selected_columns=selected_columns):
    model = load(model_path)

    if label_encoders:
        for column in label_encoders:
            if column in df.select_dtypes(include=['object']).columns:
                if column in label_encoders:
                    le = label_encoders[column]
                    df[column] = le.transform(df[column])

    if scaler:
        df_scaled = scaler.transform(df[selected_columns])
    else:
        df_scaled = df[selected_columns]
    
    predictions = model.predict(df_scaled)

    return predictions



@app.route('/submit', methods=['POST'])
def submit():    
    data = {
        "Family History": request.form.get("Family History"),
        "Age": float(request.form.get("Age")),
        "BMI": float(request.form.get("BMI")),
        "Physical Activity": request.form.get("Physical Activity"),
        "Dietary Habits": request.form.get("Dietary Habits"),
        "Socioeconomic Factors": request.form.get("Socioeconomic Factors"),
        "Smoking Status": request.form.get("Smoking Status"),
        "Alcohol Consumption": request.form.get("Alcohol Consumption"),
        "Steroid Use History": request.form.get("Steroid Use History"),
        "Liver Function Tests": request.form.get("Liver Function Tests"),
    }

    df = pd.DataFrame(data, index=[0])

    predictions = prediction(
        df,
        model_path="./joblibs/random_forest_model.joblib",
        label_encoders=label_encoders,
        scaler=scaler,
        selected_columns=selected_columns
    )

    return jsonify({"predictions": predictions.tolist()})

if __name__ == "__main__":
    model = load("joblibs/random_forest_model.joblib")
    print("Features esperadas pelo modelo:", selected_columns)
    app.run(debug=True)
