import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import base64

credenctials = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAibWVudS00NDUyMTQiLAogICJwcml2YXRlX2tleV9pZCI6ICJhMGM2NzI2MTM0MTQ1NDc3NTJlZWEwZmJhZDRiNWYyZjY2NDExNzk1IiwKICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUURBa3dZazVualM5NmxVXG5WSXdBZEtnQ3RDN3NENUFhQmNDelVFRVBoNy9LNTJsb0ZLUDZadXY5L29CYnpnVUZRdWVrMWxyemhsd2kxUVQrXG4vWS8xVmFPVmtGWEg2cUhzWUJGUmkrVnE3S2E0NnFVd2c2ZUFHTFdBb2tkVFJ6Y0lYbVBIQ2xMbWNoRlJycnNvXG5FSTM5TDg0dFQ4VEt6RFhLUURxNjIxeWsrVkl0V2FQVzNtNEtwUmlUMGpPc0tWTkwyLzlRcjR0TGMrVTQwSmdlXG5jMEZqS2lnTzgyMjlxcWFQQ3ZPT3MvUE8yeU1JRW1qMXAvVjVzczYzUVRDbFdiZmVjVUIzQ01VYkRLQmF1WkVGXG5GRmNCWG5TRVMvd2VrS0VpKzFEMnZUU0YzNUV4Z1Vnb0p2Vmx4UG1UTG9WU09wM1V2S2xVb0I3MndNV2RVZlM3XG5SY2xkczUrUkFnTUJBQUVDZ2dFQUZiQTVUK3laRFFHUms0cldIYk1GdlJBMy9LUWdFWjQyUHJ1NktCcWMwaWhQXG42Y1h4VmVGRGtONlo3RHordWNINFBzdFpnUFhQNktoZklLekVDdGh6VFFQdGRVK0tud21PeWNWY3VEY2c2OUNaXG5mQ1pIdGhpU1VJTjJUdjNGUis4Qmc4ZzQzL1ZXMkFFNjJOOU1ib2gweXd1aDJVazRnYWZNTllGQkpOOWpqdkhJXG5oYTR0NHZSYjlxZDdsamFsL0Q1QlhZYmVCN2psa2VLMUdqckV4MWJHblF6RjY3dnA3QUNkVzgrdlZDVjFLcW5hXG5TWm1UV2RJcG5XWVBhMW9EaEJTWHVHdkJzdEhJa0dEZU1ZQTFUSXpFYmloUFhMeGYyTWN1NVo0VXVLMFJkZDN0XG43dFgzWkx3bTV2Wmh1bE9XQnI2MDY1TUpzY1E2ZTVmK3JhWU1IN2Mzc1FLQmdRRGs3VWJkYkdEVm1tVThIalMyXG5uMmlWai8xL2w3WFBBc21EWmgzU3FmdlhqZXFOTi9tUktjcHNsM2ovMzlVT3NMZlRoS2JEV08ydlRlN3BpQmoyXG5zQ1RhVkRMMGUrQTEzZWNKeUVWcmJxR05YL1FTMzB1YVg1a1EyRVB1eHFZR3pvc01zUEV5Rityb1NZcHRISkRQXG5Qc040cjhENFN3WHFrRGpMUEN1QWZrM1dUUUtCZ1FEWFdTNEF2dTRjTzNLbGtxb1I2SHJaVm1xdW9CMDJ3SG1rXG5OVjlyem1OWThDNnU2REx6ZWxJMERwc0ZqdysrenFGWEVJVCswVEFiVEoxVzZtMG5mbzE0N3lQWlY1SGFNckE5XG5zZ1pyeGJoMnplTFY5aUdHVyt2aTdsVmwxbmhaRVpTYTBiUUE0TUM1ODBUVVR5VVlXTEpYeXNoSkE3QzRLbU93XG5GTmRzSjNWWVZRS0JnRGpLYkNRTitNL0VwNHlNYWNOTU5HTzEvc3NpVmFYdktSS0J5TEEwSHhmUVN2bVJnMFh4XG51aGZLVStnV0hRS3g4RWgyeGUvOEphcXhpSzFDWi83Nm40blNEWG45S1JmejNwYmNxZXdHMitqNGZ0SVh0dWVyXG5BNHZjT3E0SGRiU0dsSlFuYVE1bVJJNHZnRG1sTm45VE1LYkY0dmMxbFZnbFF4R1g4YXJFcW9hWkFvR0JBSjlBXG5XdTNBUkhQcVhva2xJZEhtZTFyWU5rSjNNOE4ycVQ0UEhrYXFOUHZqZXBKc01xbXRycmJDaWsrZEVVYklwYld1XG5DTHdzVklnTHExdElOM3A2Y3dLWXpvais0bVJiRWN3K0o5TnhQMDNVU2NoeW9TNHNNZy82c25xQ0ZUUEE5WVZjXG5TT0pSVXhUd1d0a3F3a0x6N01kUnRiV1JIaEhEZno4SzJwZ253ZmFWQW9HQUJxd2k1anNvN0tlUXRPZm9VdTlPXG5YVGI4VUhHQ0hnRkdnVkd4R296ZSthSTk5UEJYaytaV2lpSTExV1JkYTRNM1lWeCtuRzgxSzB4VU9TZmxZbTJuXG5Tek0yWTVRZ2xyQzZndTE2N1FlQUoyWE91dWpBMEhVbDNBRDI4cFhvRG91dENsSHluVkxIUEY4SWF2c3ZGWWIvXG5WOGdsODlyS0w0U3lLOFNEQU91YVRzbz1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsCiAgImNsaWVudF9lbWFpbCI6ICJyLTY4OS0yMDlAbWVudS00NDUyMTQuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJjbGllbnRfaWQiOiAiMTE1MTEwNTU4NzkyNTk1MzgzNTE1IiwKICAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLAogICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLAogICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwKICAiY2xpZW50X3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vcm9ib3QvdjEvbWV0YWRhdGEveDUwOS9yLTY4OS0yMDklNDBtZW51LTQ0NTIxNC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQ=="

SERVICE_ACCOUNT_INFO = json.loads(base64.b64decode(credenctials))


# Configuración de credenciales para Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
client = gspread.authorize(credentials)

# Conecta con tu hoja de cálculo de Google Sheets
SPREADSHEET_ID = "1qrtz-CNqzIpaWZlK_Z33cDY0P5lKiNqZcINyj1TEX8Y"  # Reemplaza con el ID de tu Google Sheet
worksheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Función para registrar los pedidos
def registrar_pedido(nombre, menu, extras, acompañamiento):
    worksheet.append_row([nombre, menu, extras, acompañamiento])

# Configuración de la app de Streamlit
st.set_page_config(page_title="Sistema de Pedidos", page_icon="🍽️", layout="wide")

# Título y descripción
st.title("🍴 Sistema de Pedidos - Menú de Lalaña 🍴")
st.markdown(
    """
    Bienvenido al sistema de pedidos. Selecciona tus opciones favoritas del menú y registra tu pedido fácilmente.
    """
)

# Columnas para organizar la interfaz
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Menú Principal")
    menu_opciones = [
        " ",
        "Bife de carne ($4700)",
        "Pollo grille ($4000)",
        "Suprema ($4000)",
        "Suprema napolitana ($4600)",
        "Milanesa de carne ($4600)",
        "Milanesa napolitana ($5300)",
        "Tarta de pollo y brócoli ($7500 entera / $4500 media)",
        "Tarta de verduras ($7500 entera / $4500 media)",
        "Pasta - Jamón y queso ($4700)",
        "Wrap ($4000)",
        "Tortilla ($4200)"
    ]
    menu_seleccionado = st.selectbox("Selecciona tu plato principal", menu_opciones)

    st.header("Extras")
    extras_opciones = [
        " ",
        "Roquefort ($1000)",
        "Fugazzeta ($1000)",
        "Especial ($1000)",
        "A caballo ($1000)",
        "Rúcula ($1000)",
        "Sin extras",
    ]
    extras_seleccionado = st.selectbox("Selecciona un extra (opcional)", extras_opciones)

    st.header("Acompañamientos")
    acompañamientos_opciones = [
        " ",
        "Puré de papa",
        "Puré de calabaza",
        "Puré mixto",
        "Papas al horno",
        "Ensalada",
        "Arroz",
        "Fideos",
        "Soufflé de calabacín",
        "Tortilla de acelga",
        "Papas fritas (+$100)",
    ]
    acompañamiento_seleccionado = st.selectbox("Selecciona un acompañamiento", acompañamientos_opciones)

with col2:
    st.header("Registro de Pedido")
    nombre = st.text_input("Ingresa tu nombre", "")
    if st.button("Registrar Pedido"):
        if nombre and menu_seleccionado:
            registrar_pedido(nombre, menu_seleccionado, extras_seleccionado, acompañamiento_seleccionado)
            st.success("¡Pedido registrado con éxito!")
        else:
            st.error("Por favor, completa tu nombre y selecciona tu menú.")

st.header("📋 Pedidos Recientes")
pedidos = worksheet.get_all_records()
if pedidos:
    st.table(pedidos)
else:
    st.write("No hay pedidos registrados aún.")
