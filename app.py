import streamlit as st
import numpy as np
import joblib
import os


# --------------------------
# ✅ Load Model and Scaler Safely
# --------------------------
def load_model(model_path):
    """Load the model safely."""
    try:
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"⚠️ Error loading {model_path}: {str(e)}")
        return None

def load_scaler(scaler_path):
    """Load the scaler safely or return None if not found."""
    if os.path.exists(scaler_path):
        try:
            return joblib.load(scaler_path)
        except Exception as e:
            st.warning(f"⚠️ Error loading scaler {scaler_path}: {str(e)}")
    return None

# --------------------------
# ✅ Load Models and Scalers
# --------------------------
models = {
    "Diabetes": {
        "model": load_model("diabetes_model.pkl"),
        "scaler": load_scaler("diabetes_scaler.pkl")
    },
    "Heart Disease": {
        "model": load_model("heart_disease_model.pkl"),
        "scaler": load_scaler("heart_disease_scaler.pkl")
    },
    "Lung Cancer": {
        "model": load_model("lung_cancer_model.pkl"),
        "scaler": None  # No scaler for lung cancer
    },
    "Liver Disease": {
        "model": load_model("liver_disease_model.pkl"),
        "scaler": load_scaler("liver_disease_scaler.pkl")
    },
    "Breast Cancer": {
        "model": load_model("breast_cancer_model.pkl"),
        "scaler": load_scaler("breast_cancer_scaler.pkl")
    },
    "Kidney Disease": {
        "model": load_model("kidney_disease_model.pkl"),
        "scaler": load_scaler("kidney_disease_scaler.pkl")
    }
}

# --------------------------
# ✅ Preprocessing Function (Only uses User Input)
# --------------------------
def preprocess_input(user_input):
    """
    Converts the user input into a NumPy array.
    """
    input_array = np.array(list(user_input.values())).reshape(1, -1)
    return input_array

# --------------------------
# ✅ Prediction Function (Without Scaler Dependency)
# --------------------------
def predict_disease(disease, user_input):
    """Make predictions based on user input only, without scaler correction."""
    
    model_data = models.get(disease)
    
    if not model_data or not model_data["model"]:
        return "⚠️ Model not available. Please check the model file."
    
    try:
        model = model_data["model"]
        input_array = preprocess_input(user_input)

        # ⚠️ Skip scaler if dimensions don't match
        scaler = model_data["scaler"]
        if scaler and input_array.shape[1] == scaler.n_features_in_:
            input_array = scaler.transform(input_array)

        # Make prediction
        prediction = model.predict(input_array)

        # Get probabilities if available
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_array)[:, 1][0] * 100
            result = f"Positive ({probability:.2f}% confidence)" if prediction[0] == 1 else f"Negative ({100 - probability:.2f}% confidence)"
        else:
            result = "Positive" if prediction[0] == 1 else "Negative"
        
        return result
    
    except Exception as e:
        return f"⚠️ Prediction failed: {str(e)}"

# --------------------------
# ✅ Streamlit UI
# --------------------------
st.title("⚕️AI-Powered Medical Predictor")

# Disease selection
disease = st.selectbox("⬇️Choose Disease to Analyse", list(models.keys()))

user_data = {}

# --------------------------
# ✅ Input fields for each disease
# --------------------------
if disease == "Breast Cancer":
    user_data = {
        "Radius Mean": st.number_input("Radius Mean", min_value=0.0),
        "Texture Mean": st.number_input("Texture Mean", min_value=0.0),
        "Smoothness Mean": st.number_input("Smoothness Mean", min_value=0.0),
        "Compactness Mean": st.number_input("Compactness Mean", min_value=0.0),
        "Concavity Mean": st.number_input("Concavity Mean", min_value=0.0)
    }

elif disease == "Diabetes":
    user_data = {
        "Pregnancies": st.number_input("Number of Pregnancies", min_value=0),
        "Glucose": st.number_input("Glucose Level", min_value=0),
        "BloodPressure": st.number_input("Blood Pressure", min_value=0),
        "SkinThickness": st.number_input("Skin Thickness", min_value=0),
        "Insulin": st.number_input("Insulin Level", min_value=0),
        "BMI": st.number_input("BMI", min_value=0.0),
        "DiabetesPedigreeFunction": st.number_input("Diabetes Pedigree Function", min_value=0.0),
        "Age": st.number_input("Age", min_value=0)
    }

elif disease == "Heart Disease":
    user_data = {
        "Age": st.number_input("Age", min_value=0),
        "Sex": 1 if st.radio("Sex", ["Male", "Female"]) == "Male" else 0,
        "Chest Pain Type": st.number_input("Chest Pain Type", min_value=0, max_value=3),
        "Blood Pressure": st.number_input("Resting Blood Pressure", min_value=50, max_value=200),
        "Cholesterol Level": st.number_input("Cholesterol Level", min_value=100, max_value=600)
    }

elif disease == "Lung Cancer":
    user_data = {
        "Gender": 1 if st.radio("Gender", ["Male", "Female"]) == "Male" else 0,
        "Age": st.number_input("Age", min_value=0),
        "Smoking": 1 if st.radio("Smoking", ["Yes", "No"]) == "Yes" else 0,
        "Coughing": 1 if st.radio("Coughing", ["Yes", "No"]) == "Yes" else 0
    }

elif disease == "Liver Disease":
    user_data = {
        "Age": st.number_input("Age", min_value=0),
        "Gender": 1 if st.radio("Gender", ["Male", "Female"]) == "Male" else 0,
        "Total Bilirubin": st.number_input("Total Bilirubin", min_value=0.0),
        "Direct Bilirubin": st.number_input("Direct Bilirubin", min_value=0.0),
        "Alkaline Phosphotase": st.number_input("Alkaline Phosphotase", min_value=0)
    }

elif disease == "Kidney Disease":
    user_data = {
        "Age": st.number_input("Age", min_value=0),
        "Blood Pressure": st.number_input("Blood Pressure", min_value=0),
        "Specific Gravity": st.number_input("Specific Gravity", min_value=1.000, max_value=1.030, step=0.001),
        "Albumin Level": st.number_input("Albumin Level", min_value=0, max_value=5),
        "Sugar Level": st.number_input("Sugar Level", min_value=0, max_value=5)
    }


# --------------------------
# ✅ Prediction Button
# --------------------------
if st.button("🧑‍⚕️Predict Disease"):
    if len(user_data) > 0:
        result = predict_disease(disease, user_data)
        st.success(f"**Prediction Result:** {result}")
    else:
        st.warning("🛑Enter all values before predicting")




