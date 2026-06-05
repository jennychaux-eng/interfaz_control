import streamlit as st
import serial
import pandas as pd
from datetime import datetime
import time

# Configuración
PUERTO = "COM3"      # Cambia según tu PC
BAUDIOS = 9600

st.set_page_config(page_title="Monitor Serial", layout="wide")

st.title("🌡️ Monitor de Temperatura")

# Conexión serial
try:
    arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
    time.sleep(2)
except Exception as e:
    st.error(f"Error al conectar: {e}")
    st.stop()

# Variables persistentes
if "datos" not in st.session_state:
    st.session_state.datos = []

placeholder_metric = st.empty()
placeholder_chart = st.empty()

while True:

    if arduino.in_waiting:

        try:
            linea = arduino.readline().decode().strip()

            temperatura = float(linea)

            st.session_state.datos.append({
                "Tiempo": datetime.now(),
                "Temperatura": temperatura
            })

            # Mantener últimos 100 puntos
            st.session_state.datos = st.session_state.datos[-100:]

            # Indicador
            placeholder_metric.metric(
                "Temperatura Actual",
                f"{temperatura:.2f} °C"
            )

            # Gráfica
            df = pd.DataFrame(st.session_state.datos)

            placeholder_chart.line_chart(
                df.set_index("Tiempo")
            )

        except:
            pass

    time.sleep(0.1)
