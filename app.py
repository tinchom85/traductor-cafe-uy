import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Clarito ☕",
    page_icon="☕",
    layout="centered"
)

# Estilos para que parezca App de celular
st.markdown("""
    <style>
    .stApp {background-color: #FAFAFA;}
    h1 {color: #4F3A2A; font-size: 28px !important;}
    div.stButton > button {
        background-color: #D2691E; 
        color: white; 
        border-radius: 12px; 
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN CON LA IA (SECRETS) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Falta la API Key. Configúrala en los 'Secrets' de Streamlit.")
    st.stop()

# --- 3. INTERFAZ DE USUARIO ---
st.title("☕ Clarito: Tu Sommelier")
st.write("Subí la foto de tu paquete. Te explico qué es, cómo hacerlo y con qué comerlo.")

# Pregunta clave para la receta
metodo_usuario = st.selectbox(
    "¿Qué cafetera vas a usar?",
    ("No sé, recomendame vos", "Prensa Francesa", "Cafetera Moka (Italiana)", "Filtro (V60/Melitta)", "Espresso", "Cafetera Eléctrica Común")
)

# Botón para subir foto o usar cámara
archivo = st.file_uploader("📸 Saca una foto a la etiqueta", type=["jpg", "png", "jpeg"])

# --- 4. EL CEREBRO DE LA IA ---
def analizar_cafe(imagen, metodo):
    # AQUÍ ESTABA EL ERROR: CAMBIAMOS AL MODELO QUE SÍ TIENES
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    prompt = prompt = f"""
    Actúa como un Sommelier de Café experto y Barista profesional de una cafetería de especialidad en Uruguay.
    Analiza esta imagen de una etiqueta de café.
    El usuario va a usar esta cafetera: {metodo}.

    TU TONO DE VOZ:
    - Profesional, educado y cálido (Rioplatense neutro).
    - Evita la jerga callejera ("bo", "fiera", "salado").
    - Habla con la autoridad de quien sabe mucho pero explica simple.

    Estructura tu respuesta así:
    
    ### 🧐 Perfil Sensorial
    (Traduce: Variedad, Proceso, Altura. Explica las "Notas de Cata" de forma elegante. Ej: "Encontrarás una acidez brillante..." en lugar de "es ácido").

    ### ⚙️ Guía de Preparación ({metodo})
    (Instrucciones precisas: Ratio café/agua, Temperatura y Molienda. Si es "Recomendame vos", elige el método que mejor respete el grano).

    ### 🥐 Maridaje Sugerido (Cafetería Local)
    (Recomienda UN acompañamiento ideal para Desayuno o Merienda que se encuentre en una cafetería uruguaya.
    
    REGLAS DE MARIDAJE:
    - Cafés Frutales/Florales/Ligeros: Van bien con Scones de Queso (el contraste salado realza el dulce), Medialunas de Manteca o Tostadas con queso blanco.
    - Cafés Chocolatosos/Nuez/Dulces: Van bien con Alfajor de Maicena, Cookie de Chocolate o Brownie.
    - Cafés Intensos/Tostado Medio-Alto: Van bien con Tostado Mixto (Jamón y Queso) para limpiar paladar o Medialunas de Grasa.
    - Cafés Especiados/Complejos: Carrot Cake o Budín de Limón.
    
    Justifica brevemente por qué combinan esos sabores).
    """
    
    try:
        with st.spinner('Analizando etiqueta y buscando un bizcocho... 🧉'):
            response = model.generate_content([prompt, imagen])
            return response.text
    except Exception as e:
        return f"Ups, no pude leer bien. Probá sacar la foto más de cerca. Error técnico: {e}"

# --- 5. MOSTRAR RESULTADO ---
if archivo is not None:
    image = Image.open(archivo)
    st.image(image, use_column_width=True, caption="Tu Café")
    
    if st.button('✨ Analizar Ahora'):
        resultado = analizar_cafe(image, metodo_usuario)
        st.markdown(resultado)
        st.success("¡Que lo disfrutes!")
