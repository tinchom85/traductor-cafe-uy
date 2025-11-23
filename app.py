import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Clarito: Sommelier AI 🇺🇾", page_icon="☕", layout="centered")

st.markdown("""
    <style>
    .stApp {background-color: #FAFAFA;}
    h1 {color: #2C3E50;}
    div.stButton > button {background-color: #A0522D; color: white; border-radius: 8px; width: 100%; font-weight: bold;}
    /* Estilo para el botón de Maps */
    a {text-decoration: none;}
    .map-btn {
        display: inline-block;
        background-color: #4285F4;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        width: 100%;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API KEY ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.stop()

# --- INTERFAZ ---
st.title("☕ Clarito: Sommelier 360°")
st.write("Análisis sensorial + Buscador de Maridaje.")

metodo_usuario = st.selectbox(
    "Seleccioná tu método:",
    ("✨ Sorprendeme", "AeroPress", "V60 / Origami", "Chemex", "Prensa Francesa", "Moka Italiana", "Espresso", "Cold Brew")
)

archivo = st.file_uploader("📸 Foto de la etiqueta", type=["jpg", "png", "jpeg"])

# --- EL CEREBRO CON "EXTRACCIÓN DE DATOS" ---
def analizar_experto(imagen, metodo):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    prompt = f"""
    Eres un Sommelier de Café experto en Uruguay. Analiza esta etiqueta. Usuario usa: {metodo}.

    --- 1. ANÁLISIS ---
    Identifica Variedad, Proceso y Altura. Explica el perfil sensorial.

    --- 2. RECETA TÉCNICA ---
    Define Ratio, Temperatura y Molienda para {metodo}.

    --- 3. MARIDAJE DE AUTOR ---
    Recomienda UN plato específico de la gastronomía de cafetería uruguaya (Dulce o Salado) que combine perfecto.
    Justifica la elección.

    --- INSTRUCCIÓN FINAL OBLIGATORIA (IMPORTANTE) ---
    Al final de tu respuesta, escribe una línea separada que diga EXACTAMENTE así:
    SEARCH_QUERY: [Nombre del plato recomendado]
    
    Ejemplo:
    ...disfrutarás el contraste.
    SEARCH_QUERY: Carrot Cake
    """
    
    try:
        with st.spinner('Analizando café y buscando dónde comer rico... 🧐'):
            response = model.generate_content([prompt, imagen])
            texto_completo = response.text
            
            # --- LÓGICA PARA SEPARAR EL PLATO DEL TEXTO ---
            plato_a_buscar = "Cafetería de Especialidad" # Default por si falla
            texto_visible = texto_completo

            if "SEARCH_QUERY:" in texto_completo:
                partes = texto_completo.split("SEARCH_QUERY:")
                texto_visible = partes[0].strip() # Lo que mostramos al usuario
                plato_a_buscar = partes[1].strip() # Lo que mandamos a Google Maps
            
            return texto_visible, plato_a_buscar

    except Exception as e:
        return f"Error: {e}", None

if archivo is not None:
    image = Image.open(archivo)
    st.image(image, use_column_width=True)
    
    if st.button('🔍 Iniciar Cata y Buscar Comida'):
        # Llamamos a la función que devuelve dos cosas: Texto y Plato
        texto_resultado, plato = analizar_experto(image, metodo_usuario)
        
        # 1. Mostramos el análisis
        st.markdown(texto_resultado)
        
        # 2. Generamos el Botón Inteligente de Maps
        if plato:
            # Limpiamos el texto para la URL (espacios por +)
            query_url = plato.replace(" ", "+")
            url_maps = f"https://www.google.com/maps/search/{query_url}+cerca+de+mi"
            
            st.success(f"🍽️ Recomendación: **{plato}**")
            
            # Usamos st.link_button (nativo de Streamlit)
            st.link_button(
                label=f"📍 Buscar dónde comer '{plato}' cerca de mí",
                url=url_maps,
                help="Esto abrirá Google Maps con la búsqueda lista"
            )
