import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Diagnóstico de Modelos", page_icon="🛠️")
st.title("🛠️ Diagnóstico: ¿Qué modelos tengo?")

# 1. Intentar conectar
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ API Key detectada correctamente.")
except Exception as e:
    st.error(f"❌ Error con la API Key: {e}")
    st.stop()

# 2. Botón para listar
if st.button("🔍 Listar Modelos Disponibles"):
    try:
        st.info("Consultando servidores de Google...")
        
        # Buscar modelos que sirvan para generar contenido
        lista_modelos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                lista_modelos.append({
                    "NOMBRE TÉCNICO (Copia esto)": m.name,
                    "Nombre Amigable": m.display_name
                })
        
        if lista_modelos:
            st.success(f"¡Conectado! Encontré {len(lista_modelos)} modelos disponibles para ti:")
            st.table(lista_modelos)
        else:
            st.warning("Me conecté, pero la lista volvió vacía. Qué raro.")
            
    except Exception as e:
        st.error(f"❌ Error fatal al conectar con Google: {e}")
        st.write("Pista: Si el error dice '403' o 'PermissionDenied', tu clave API no sirve o no tiene permisos.")
