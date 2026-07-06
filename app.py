from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open("C:\\Users\\Vineela\\Desktop\\Sector\\vehicle_health_model.pkl", "rb"))

def overall_condition(score):
    if score >= 80:
        return "NORMAL"
    elif score >= 50:
        return "MAINTENANCE REQUIRED"
    else:
        return "REPAIR REQUIRED"

def diagnose(temp, rpm, oil, mileage, vib):
    issues = []

    if oil < 40:
        issues.append({
            "part": "Engine Lubrication System",
            "reason": "Low engine oil level",
            "precaution": "Avoid high speed and long drives",
            "action": "Refill or change engine oil",
            "time": "Within 3 days"
        })

    if temp > 95:
        issues.append({
            "part": "Cooling System",
            "reason": "Engine overheating",
            "precaution": "Stop vehicle if temperature rises",
            "action": "Check radiator and coolant",
            "time": "Within 24 hours"
        })

    if vib > 1.5:
        issues.append({
            "part": "Engine Mount / Suspension",
            "reason": "Excessive vibration",
            "precaution": "Avoid sudden acceleration",
            "action": "Inspect engine mounts",
            "time": "5–7 days"
        })

    return issues

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = [
        float(request.form['engine_temp']),
        float(request.form['engine_rpm']),
        float(request.form['oil_level']),
        float(request.form['vehicle_mileage']),
        float(request.form['vibration'])
    ]

    score = int(model.predict([data])[0])
    condition = overall_condition(score)

    issues = []
    if condition != "NORMAL":
        issues = diagnose(*data)

    return render_template(
        'result.html',
        score=score,
        condition=condition,
        issues=issues
    )

if __name__ == "__main__":
    app.run(debug=True)
