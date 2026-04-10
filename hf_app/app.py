import gradio as gr
from model import predict_sales

# FUNCIÓN UI
def predict_ui(country, quantity_sold, month, day_of_week, order_hour, is_weekend):
    prediction = predict_sales(
        country,
        quantity_sold,
        month,
        day_of_week,
        order_hour,
        is_weekend
    )
    return round(prediction, 2)


# INTERFAZ GRADIO
interface = gr.Interface(
    fn=predict_ui,
    inputs=[
        gr.Textbox(label="Country"),
        gr.Number(label="Quantity Sold"),
        gr.Number(label="Month"),
        gr.Number(label="Day of Week"),
        gr.Number(label="Order Hour"),
        gr.Number(label="Is Weekend (0/1)")
    ],
    outputs=gr.Number(label="Predicción de ventas"),
    title="E-Commerce Sales Prediction",
    description="Modelo ML para predicción de ventas en e-commerce"
)

if __name__ == "__main__":
    interface.launch()