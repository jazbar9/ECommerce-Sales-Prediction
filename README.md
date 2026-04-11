# ECommerce-Sales-Prediction
api para modelo de machine learning e-commerce sales prediction 

## Descripcion
Este proyecto desarrolla un modelo de Machine Learning para predecir ventas en e-commerce,  pero lo hace aprendiendo comportamiento de compra del cliente segun variables como: país, hora, día, mes, fin de semana, cantidad vendida

El modelo es entrenado en notebooks, exportado como archivos `.pkl` y luego consumido tanto por una API Flask y como por una interfaz Gradio, dependiendo del entorno de ejecución.

## API Flask
La aplicación implementa un API REST con operaciones CRUD sobre ventas.

## Deployment
Se incluye una versión adaptada en la carpeta `hf_app` la cual utiliza Gradio para su despliegue en Hugging Face Spaces.

## Estructura del Proyecto
ECommerce-Sales-Prediction/
│
├── app.py                 API Flask (backend principal)
├── model.py               Lógica de predicción
├── requirements.txt       Dependencias del proyecto
│
├── model/                 Modelos entrenados (.pkl)
│
├── templates/             HTML (interfaz web con Flask)
│
├── notebooks/             EDA y entrenamiento del modelo
│
├── hf_app/                Versión para deployment en Hugging Face
│   ├── app.py             App con Gradio
│   ├── model.py           Lógica adaptada
│   ├── *.pkl              Modelo y scalers
│
├── .env.example           Variables sensibles 
├── .gitignore             Archivos ignorados por Git