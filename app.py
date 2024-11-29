from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/graficos')
def graficos():
    return render_template('graficos.html')  


@app.route('/submit', methods=['POST'])
def submit():    
    data = {
        "Age": float(request.form.get("Age")),
        "BMI": float(request.form.get("BMI")),
        "Family History": request.form.get("Family History"),
        "Physical Activity": request.form.get("Physical Activity"),
        "Dietary Habits": request.form.get("Dietary Habits"),
        "Socioeconomic Factors": request.form.get("Socioeconomic Factors"),
        "Smoking Status": request.form.get("Smoking Status"),
        "Alcohol Consumption": request.form.get("Alcohol Consumption"),
        "Steroid Use History": request.form.get("Steroid Use History"),
        "Genetic Testing": request.form.get("Genetic Testing"),
        "Liver Function Tests": request.form.get("Liver Function Tests"),
    }

  

if __name__ == "__main__":
    app.run(debug=True)
