import streamlit as st
import serial
import pandas as pd
from collections import deque
from datetime import datetime
import time

# =====================================================
# CONFIGURACIÓN
# =====================================================

PUERTO = "COM3"      # Cambiar según corresponda
BAUDIOS = 9600

# =====================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Incubadora Neonatal",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ Sistema de Control Térmico")
st.subheader("Monitor de Incubadora Neonatal")

# =====================================================
# CONEXIÓN SERIAL
# =====================================================

@st.cache_resource
def conectar_serial():
    return serial.Serial(
        port=PUERTO,
        baudrate=BAUDIOS,
        timeout=1
    )

try:
    arduino = conectar_serial()
except Exception as e:
    st.error(f"No se pudo conectar con Arduino: {e}")
    st.stop()

# =====================================================
# VARIABLES DE SESIÓN
# =====================================================

if "temperaturas" not in st.session_state:
    st.session_state.temperaturas = deque(maxlen=100)

if "setpoints" not in st.session_state:
    st.session_state.setpoints = deque(maxlen=100)

if "potencias" not in st.session_state:
    st.session_state.potencias = deque(maxlen=100)

if "tiempos" not in st.session_state:
    st.session_state.tiempos = deque(maxlen=100)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("Configuración")

    nuevo_setpoint = st.number_input(
        "Setpoint (°C)",
        min_value=30.0,
        max_value=40.0,
        value=36.5,
        step=0.1
    )

    if st.button("Actualizar Setpoint"):

        try:

            comando = f"SP:{nuevo_setpoint}\n"

            arduino.write(comando.encode())

            st.success(
                f"Setpoint enviado: {nuevo_setpoint:.1f} °C"
            )

        except Exception as e:

            st.error(f"Error enviando SP: {e}")

# =====================================================
# LECTURA SERIAL
# =====================================================

temperatura = 0.0
setpoint = 0.0
error = 0.0
u = 0.0

try:

    if arduino.in_waiting:

        linea = arduino.readline().decode().strip()

        datos = linea.split(",")

        if len(datos) == 4:

            temperatura = float(datos[0])
            setpoint = float(datos[1])
            error = float(datos[2])
            u = float(datos[3])

            st.session_state.temperaturas.append(
                temperatura
            )

            st.session_state.setpoints.append(
                setpoint
            )

            st.session_state.potencias.append(
                u
            )

            st.session_state.tiempos.append(
                datetime.now()
            )

except:
    pass

# =====================================================
# MÉTRICAS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Temperatura",
        f"{temperatura:.2f} °C"
    )

with col2:
    st.metric(
        "Setpoint",
        f"{setpoint:.2f} °C"
    )

with col3:
    st.metric(
        "Error",
        f"{error:.2f} °C"
    )

with col4:
    st.metric(
        "Potencia",
        f"{u:.1f} %"
    )

# =====================================================
# ESTADO
# =====================================================

st.markdown("### Estado del Sistema")

if error > 0.5:
    st.warning("🔥 Calentando")

elif error < -0.5:
    st.info("❄️ Enfriando")

else:
    st.success("✅ Temperatura Estable")

# =====================================================
# DATAFRAME HISTÓRICO
# =====================================================

if len(st.session_state.tiempos) > 0:

    df = pd.DataFrame({
        "Tiempo": list(st.session_state.tiempos),
        "Temperatura": list(st.session_state.temperaturas),
        "Setpoint": list(st.session_state.setpoints),
        "Potencia": list(st.session_state.potencias)
    })

    df = df.set_index("Tiempo")

    col_g1, col_g2 = st.columns(2)

    with col_g1:

        st.markdown("### Temperatura vs Setpoint")

        st.line_chart(
            df[["Temperatura", "Setpoint"]]
        )

    with col_g2:

        st.markdown("### Acción de Control PI")

        st.line_chart(
            df[["Potencia"]]
        )

# =====================================================
# INFORMACIÓN ADICIONAL
# =====================================================

st.divider()

col5, col6 = st.columns(2)

with col5:

    st.markdown("### Parámetros del Controlador")

    st.write("Kp = 3.89")
    st.write("Ki = 1.07")
    st.write("Tm = 2 s")

with col6:

    st.markdown("### Hardware")

    st.write("Arduino UNO")
    st.write("Sensor DHT11")
    st.write("Controlador PI")
    st.write("Calefactor AC")

# =====================================================
# AUTOREFRESH
# =====================================================

time.sleep(0.5)
st.rerun()
