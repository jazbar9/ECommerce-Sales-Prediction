import gradio as gr
from model import predict_sales

countries = [
    "United Kingdom", "France", "Australia", "Ireland", "Germany",
    "Portugal", "Poland", "Netherlands", "Spain", "Cyprus",
    "Belgium", "Greece", "Norway", "Austria", "United Arab Emirates",
    "Denmark", "Italy", "Switzerland", "Sweden", "United States",
    "Japan", "Finland", "Malta", "South Africa", "Singapore",
    "Bahrain", "Israel", "Thailand", "Lithuania", "Nigeria",
    "Korea, Rep.", "Brazil", "Canada", "Iceland"
]

def predict_ui(country, quantity_sold, month, day_of_week, order_hour, is_weekend):
    return f"💰 Predicted Sales: £ {predict_sales(country, quantity_sold, month, day_of_week, order_hour, is_weekend)}"

css = """
body, .gradio-container {
    background-image: linear-gradient(to right top, #51b5e4, #94c4ef, #c2d5f5, #e5e9fa, #ffffff);
    font-family: 'Arial', sans-serif;
    max-width: 100% !important;
    width: 100% !important;
    min-height: 100vh !important;
    padding: 30px !important;
    color: #111827 !important;
}

/* TITULOS PRINCIPALES */
h1, h2, h3 {
    color: #3232A5 !important;
    font-weight: 800 !important;
}

/* LABELS DE INPUTS (GRADIO MODERNO) */
label, .wrap label, .svelte-1ipelgc {
    color: #111827 !important;
    font-weight: 600 !important;
}

/* INPUTS */
input, select, textarea {
    border-radius: 10px !important;
    background-color: white !important;
    color: #111827 !important;
}

/* DROPDOWN */
.gradio-dropdown {
    background: white !important;
}

/* RADIO BUTTONS */
.gr-radio label {
    color: #111827 !important;
    font-weight: 600 !important;
}

/* círculo externo */
.gradio-radio input[type="radio"] {
    appearance: none;
    transform: scale(1.2);
}

.gradio-radio input[type="radio"]:checked {
   background-color: #3232A5 !important; /* Fondo azul oscuro al marcar */
    border: 2px solid #090979 !important;
    transform: scale(1.1);
    box-shadow: 0 0 0 4px rgba(50, 50, 165, 0.25);
}
/* contenedor de opciones */
.gradio-radio {
    background: white !important;
    padding: 10px !important;
    border-radius: 10px !important;
    border: 1px solid #e5e7eb !important;
}

/* BOTÓN PRINCIPAL (TU COLOR) */
button {
    background: #3232a5 !important;
    color: white !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    padding: 12px !important;
    border: none !important;
    transition: 0.3s;
}

button:hover {
    background: #25258a !important;
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(50,50,165,0.3);
}

/* RESULTADO */
#resultado {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #3232a5 !important;
    text-align: center;
}
"""

with gr.Blocks(css=css, title="E-Commerce Sales Prediction") as demo:

    gr.Markdown("# 💰 E-Commerce Sales Prediction AI")
    gr.Markdown("### Predict your sales using Machine Learning")

    with gr.Row():
        with gr.Column():
            country = gr.Dropdown(countries, label="Country", value="France")
            quantity_sold = gr.Number(label="Quantity Sold", value=1)
            month = gr.Number(label="Month (1-12)", value=1)
            day_of_week = gr.Number(label="Day of Week (0-6)", value=1)
            order_hour = gr.Number(label="Order Hour (0-23)", value=12)
            is_weekend = gr.Radio(
                choices=[("No", 0), ("Yes", 1)],
                label="Is Weekend",
                value=0
            )

            btn = gr.Button("🚀 Predict Sales")

        with gr.Column():
            output = gr.Textbox(
                label="Prediction Result",
                lines=5
            )

    btn.click(
        fn=predict_ui,
        inputs=[country, quantity_sold, month, day_of_week, order_hour, is_weekend],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)