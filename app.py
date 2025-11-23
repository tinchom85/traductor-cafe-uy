import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Traductor de Café 🇺🇾",
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
# Intentamos obtener la clave de los secretos de Streamlit
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Falta la API Key. Configúrala en los 'Secrets' de Streamlit.")
    st.stop()

# --- 3. INTERFAZ DE USUARIO ---
st.title("☕ Traductor de Café y Sommelier")
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
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Actúa como un experto barista y sommelier de Uruguay. 
    Analiza esta imagen de una etiqueta de café.
    El usuario va a usar esta cafetera: {metodo}.

    Responde en formato limpio y bonito (usando Markdown), con tono amable y uruguayo (voseo suave).
    
    Estructura tu respuesta así:
    
    ### 🧐 ¿Qué estás tomando?
    (Traduce: Variedad, Proceso, Altura y Notas. Explica los términos difíciles como "Lavado" o "Honey" en español simple).

    ### ⚙️ Tu Receta Perfecta ({metodo})
    (Dile: Cantidad de café/agua, Temperatura del agua y Molienda. Si eligió "Recomendame vos", sugiere el mejor método para este grano).

    ### 🥐 El Maridaje Uruguayo
    (Recomienda UN acompañamiento clásico de panadería uruguaya que combine con este sabor específico. Ej: Alfajor de Maicena, Yo-Yo, Salchichón, Medialunas, Torta Frita, etc. Explica por qué combinan).
    """
    
    try:
        with st.spinner('Analizando etiqueta y buscando un bizcocho... 🧉'):
            response = model.generate_content([prompt, imagen])
            return response.text
    except Exception as e:
        return f"Ups, no pude leer bien. Probá sacar la foto más de cerca. Error: {e}"

# --- 5. MOSTRAR RESULTADO ---
if archivo is not None:
    image = Image.open(archivo)
    st.image(image, use_column_width=True, caption="Tu Café")
    
    if st.button('✨ Analizar Ahora'):
        resultado = analizar_cafe(image, metodo_usuario)
        st.markdown(resultado)
        st.success("¡Que lo disfrutes!")
