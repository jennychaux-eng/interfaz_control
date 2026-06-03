import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Incubadora Neonatal",
    page_icon="🌡️",
    layout="wide"
)

# ==========================================
# ENCABEZADO
# ==========================================

st.title("🌡️ Sistema de Control Térmico")
st.subheader("Monitor de Incubadora Neonatal")

st.divider()

# ==========================================
# VARIABLES SIMULADAS
# ==========================================

temperatura = 35.8
setpoint = 36.5
error = setpoint - temperatura
u = 65.0

# ==========================================
# TARJETAS PRINCIPALES
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Temperatura Actual",
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
        "Potencia Aplicada",
        f"{u:.1f} %"
    )

# ==========================================
# ESTADO DEL SISTEMA
# ==========================================

st.markdown("### Estado del Sistema")

if error > 0.5:
    st.warning("🔥 Calentando")

elif error < -0.5:
    st.info("❄️ Enfriando")

else:
    st.success("✅ Temperatura Estable")

st.divider()

# ==========================================
# DATOS PARA LAS GRÁFICAS
# ==========================================

n = 60

tiempo = pd.date_range(
    end=datetime.now(),
    periods=n,
    freq="s"
)

temperatura_hist = np.linspace(34.5, 35.8, n)
setpoint_hist = np.ones(n) * 36.5

potencia_hist = np.linspace(100, 65, n)

# ==========================================
# GRÁFICAS
# ==========================================

col_g1, col_g2 = st.columns(2)

with col_g1:

    st.markdown("### Temperatura vs Setpoint")

    df_temp = pd.DataFrame({
        "Temperatura": temperatura_hist,
        "Setpoint": setpoint_hist
    }, index=tiempo)

    st.line_chart(df_temp)

with col_g2:

    st.markdown("### Acción de Control PI")

    df_u = pd.DataFrame({
        "u[k] (%)": potencia_hist
    }, index=tiempo)

    st.line_chart(df_u)

st.divider()

# ==========================================
# INFORMACIÓN ADICIONAL
# ==========================================

col5, col6 = st.columns(2)

with col5:

    st.markdown("### Parámetros del Controlador")

    st.write("**Kp:** 3.89")
    st.write("**Ki:** 1.07")
    st.write("**Periodo de muestreo:** 2 s")

with col6:

    st.markdown("### Información del Sistema")

    st.write("Estado del calefactor: ON")
    st.write("Sensor: DHT11")
    st.write("Controlador: PI Discreto")

st.divider()

st.caption(
    "Universidad Autónoma de Occidente - Ingeniería Biomédica"
)
