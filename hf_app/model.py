import joblib
import numpy as np
import pandas as pd
import os

# Cargar 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model/model.pkl"))
scaler_X = joblib.load(os.path.join(BASE_DIR, "model/scaler_X.pkl"))
scaler_y = joblib.load(os.path.join(BASE_DIR, "model/scaler_y.pkl"))
transformer = joblib.load(os.path.join(BASE_DIR, "model/transformer.pkl"))



# FUNCIÓN DE PREDICCIÓN

def predict_sales(
    country_input, 
    quantity_sold, 
    month, 
    day_of_week, 
    order_hour, 
    is_weekend):

    new_data = pd.DataFrame([{
        'country': country_input,
        'quantity_sold': quantity_sold,
        'month': month,
        'day_of_week': day_of_week,
        'order_hour': order_hour,
        'is_weekend': is_weekend
    }])

    # Transformación
    X_transformed = transformer.transform(new_data)

    # Escalado
    X_scaled = scaler_X.transform(X_transformed)

    # Predicción (log scale)
    pred_scaled = model.predict(X_scaled)

    # Inversa scaler target
    pred_log = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

    # Inversa log1p
    pred_final = np.expm1(pred_log)

    return float(pred_final)


#WRAPER PARA GRADIO SE AGREGA ESTO
def predict_sales_from_list(features):
    """
    Wrapper para Gradio
    features = [
        country_input,
        quantity_sold,
        month,
        day_of_week,
        order_hour,
        is_weekend
    ]
    """
    return predict_sales(*features)