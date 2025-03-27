import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import base64
from datetime import datetime

# ==============
# 1. CREDENCIALES
# ==============
# Reemplaza 'credenctials' con tu cadena Base64 real
credenctials = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAibWVudS00NDUyMTQiLAogICJwcml2YXRlX2tleV9pZCI6ICJhMGM2NzI2MTM0MTQ1NDc3NTJlZWEwZmJhZDRiNWYyZjY2NDExNzk1IiwKICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUURBa3dZazVualM5NmxVXG5WSXdBZEtnQ3RDN3NENUFhQmNDelVFRVBoNy9LNTJsb0ZLUDZadXY5L29CYnpnVUZRdWVrMWxyemhsd2kxUVQrXG4vWS8xVmFPVmtGWEg2cUhzWUJGUmkrVnE3S2E0NnFVd2c2ZUFHTFdBb2tkVFJ6Y0lYbVBIQ2xMbWNoRlJycnNvXG5FSTM5TDg0dFQ4VEt6RFhLUURxNjIxeWsrVkl0V2FQVzNtNEtwUmlUMGpPc0tWTkwyLzlRcjR0TGMrVTQwSmdlXG5jMEZqS2lnTzgyMjlxcWFQQ3ZPT3MvUE8yeU1JRW1qMXAvVjVzczYzUVRDbFdiZmVjVUIzQ01VYkRLQmF1WkVGXG5GRmNCWG5TRVMvd2VrS0VpKzFEMnZUU0YzNUV4Z1Vnb0p2Vmx4UG1UTG9WU09wM1V2S2xVb0I3MndNV2RVZlM3XG5SY2xkczUrUkFnTUJBQUVDZ2dFQUZiQTVUK3laRFFHUms0cldIYk1GdlJBMy9LUWdFWjQyUHJ1NktCcWMwaWhQXG42Y1h4VmVGRGtONlo3RHordWNINFBzdFpnUFhQNktoZklLekVDdGh6VFFQdGRVK0tud21PeWNWY3VEY2c2OUNaXG5mQ1pIdGhpU1VJTjJUdjNGUis4Qmc4ZzQzL1ZXMkFFNjJOOU1ib2gweXd1aDJVazRnYWZNTllGQkpOOWpqdkhJXG5oYTR0NHZSYjlxZDdsamFsL0Q1QlhZYmVCN2psa2VLMUdqckV4MWJHblF6RjY3dnA3QUNkVzgrdlZDVjFLcW5hXG5TWm1UV2RJcG5XWVBhMW9EaEJTWHVHdkJzdEhJa0dEZU1ZQTFUSXpFYmloUFhMeGYyTWN1NVo0VXVLMFJkZDN0XG43dFgzWkx3bTV2Wmh1bE9XQnI2MDY1TUpzY1E2ZTVmK3JhWU1IN2Mzc1FLQmdRRGs3VWJkYkdEVm1tVThIalMyXG5uMmlWai8xL2w3WFBBc21EWmgzU3FmdlhqZXFOTi9tUktjcHNsM2ovMzlVT3NMZlRoS2JEV08ydlRlN3BpQmoyXG5zQ1RhVkRMMGUrQTEzZWNKeUVWcmJxR05YL1FTMzB1YVg1a1EyRVB1eHFZR3pvc01zUEV5Rityb1NZcHRISkRQXG5Qc040cjhENFN3WHFrRGpMUEN1QWZrM1dUUUtCZ1FEWFdTNEF2dTRjTzNLbGtxb1I2SHJaVm1xdW9CMDJ3SG1rXG5OVjlyem1OWThDNnU2REx6ZWxJMERwc0ZqdysrenFGWEVJVCswVEFiVEoxVzZtMG5mbzE0N3lQWlY1SGFNckE5XG5zZ1pyeGJoMnplTFY5aUdHVyt2aTdsVmwxbmhaRVpTYTBiUUE0TUM1ODBUVVR5VVlXTEpYeXNoSkE3QzRLbU93XG5GTmRzSjNWWVZRS0JnRGpLYkNRTitNL0VwNHlNYWNOTU5HTzEvc3NpVmFYdktSS0J5TEEwSHhmUVN2bVJnMFh4XG51aGZLVStnV0hRS3g4RWgyeGUvOEphcXhpSzFDWi83Nm40blNEWG45S1JmejNwYmNxZXdHMitqNGZ0SVh0dWVyXG5BNHZjT3E0SGRiU0dsSlFuYVE1bVJJNHZnRG1sTm45VE1LYkY0dmMxbFZnbFF4R1g4YXJFcW9hWkFvR0JBSjlBXG5XdTNBUkhQcVhva2xJZEhtZTFyWU5rSjNNOE4ycVQ0UEhrYXFOUHZqZXBKc01xbXRycmJDaWsrZEVVYklwYld1XG5DTHdzVklnTHExdElOM3A2Y3dLWXpvais0bVJiRWN3K0o5TnhQMDNVU2NoeW9TNHNNZy82c25xQ0ZUUEE5WVZjXG5TT0pSVXhUd1d0a3F3a0x6N01kUnRiV1JIaEhEZno4SzJwZ253ZmFWQW9HQUJxd2k1anNvN0tlUXRPZm9VdTlPXG5YVGI4VUhHQ0hnRkdnVkd4R296ZSthSTk5UEJYaytaV2lpSTExV1JkYTRNM1lWeCtuRzgxSzB4VU9TZmxZbTJuXG5Tek0yWTVRZ2xyQzZndTE2N1FlQUoyWE91dWpBMEhVbDNBRDI4cFhvRG91dENsSHluVkxIUEY4SWF2c3ZGWWIvXG5WOGdsODlyS0w0U3lLOFNEQU91YVRzbz1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsCiAgImNsaWVudF9lbWFpbCI6ICJyLTY4OS0yMDlAbWVudS00NDUyMTQuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJjbGllbnRfaWQiOiAiMTE1MTEwNTU4NzkyNTk1MzgzNTE1IiwKICAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLAogICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLAogICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwKICAiY2xpZW50X3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vcm9ib3QvdjEvbWV0YWRhdGEveDUwOS9yLTY4OS0yMDklNDBtZW51LTQ0NTIxNC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQ=="  # por ejemplo

SERVICE_ACCOUNT_INFO = json.loads(base64.b64decode(credenctials))
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
client = gspread.authorize(credentials)

# ==================
# 2. CONFIGURACIÓN SHEETS
# ==================
SPREADSHEET_ID = "1qrtz-CNqzIpaWZlK_Z33cDY0P5lKiNqZcINyj1TEX8Y"

# Hoja 1: donde se registran los pedidos
pedidos_worksheet = client.open_by_key(SPREADSHEET_ID).worksheet("Pedidos")

# Hoja 2: "Menú del Día" (aquí están todos los platos)
menu_worksheet = client.open_by_key(SPREADSHEET_ID).worksheet("Menú del Día")

# ========================================
# 3. FUNCIÓN PARA GUARDAR PEDIDOS (Hoja 1)
# ========================================
def registrar_pedido(fecha, nombre, tipo_menu, plato, extra, acompanamiento, comentarios):
    """
    Inserta una nueva fila al final de 'pedidos_worksheet' con la información del pedido.
    [fecha, nombre, tipo_menu, plato, extra, acompanamiento, comentarios]
    """
    pedidos_worksheet.append_row([
        fecha, 
        nombre, 
        tipo_menu, 
        plato, 
        extra, 
        acompanamiento, 
        comentarios
    ])

# ===========================
# 4. CONFIGURACIÓN DE STREAMLIT
# ===========================
st.set_page_config(
    page_title="Sistema de Pedidos",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍴 Sistema de Pedidos - SKRB 🍴")
st.markdown(
    "Bienvenido al sistema de pedidos. Selecciona tus opciones favoritas y registra tu pedido fácilmente."
)

# =========================
# 5. LECTURA DEL MENÚ DESDE HOJA 2
# =========================
menu_data = menu_worksheet.get_all_records()

# Filtramos por la fecha actual en formato 'YYYY-MM-DD'
hoy_str = datetime.now().strftime("%Y-%m-%d")
menus_hoy = [item for item in menu_data if str(item["Fecha"]) == hoy_str]

# Separamos los menús en categorías
menus_extra = [m for m in menus_hoy if m["Tipo de menú"].strip().lower() == "extra"]
menus_acomp = [m for m in menus_hoy if m["Tipo de menú"].strip().lower() == "acompañamiento"]

# Unificamos Carne, Vegetariano y Menú del Día en un solo "Menú principal"
# Regla: "Menú principal" = (Carne, Vegetariano, o cualquier "menu del dia...")
menus_principal = [
    m for m in menus_hoy
    if (
        m["Tipo de menú"].strip().lower() in ["carne", "vegetariano"]
        or m["Tipo de menú"].strip().lower().startswith("menu del dia")
    )
]

# ================
# 6. INTERFAZ MENÚ
# ================
# -- MENÚ PRINCIPAL (unificado) --
st.subheader("Menú Principal")
if menus_principal:
    # Construimos dos listas paralelas: labels y data (para poder identificar el plato seleccionado)
    opciones_principal_labels = ["Ninguno"]
    opciones_principal_data = [None]

    for item in menus_principal:
        tipo = item["Tipo de menú"]
        plato = item["Plato"]
        precio = item["Precio"]
        # Ejemplo de label: "Bife de carne ($ 4700) (Carne)"
        label = f"{plato} ($ {precio}) ({tipo})"
        opciones_principal_labels.append(label)
        opciones_principal_data.append(item)

else:
    opciones_principal_labels = ["No hay menús principales para hoy"]
    opciones_principal_data = [None]

seleccion_principal = st.selectbox(
    "Selecciona tu plato principal",
    options=range(len(opciones_principal_labels)),
    format_func=lambda i: opciones_principal_labels[i]
)

# -- EXTRAS --
st.subheader("Extras")
if menus_extra:
    opciones_extra = ["Ninguno"] + [
        f"{m['Plato']} ($ {m['Precio']})" for m in menus_extra
    ]
else:
    opciones_extra = ["No hay extras disponibles hoy"]
seleccion_extra = st.selectbox("Selecciona un extra (opcional)", opciones_extra)

# -- ACOMPAÑAMIENTOS --
st.subheader("Acompañamientos")
if menus_acomp:
    opciones_acomp = ["Ninguno"] + [
        f"{m['Plato']} ($ {m['Precio']})" for m in menus_acomp
    ]
else:
    opciones_acomp = ["No hay acompañamientos disponibles hoy"]
seleccion_acomp = st.selectbox("Selecciona un acompañamiento", opciones_acomp)

# ==============
# 7. COMENTARIOS
# ==============
st.subheader("Comentarios / Observaciones")
comentarios = st.text_area("¿Algo más que debamos saber? (opcional)", "")

# ================
# 8. REGISTRO PEDIDO
# ================
st.header("Registro de Pedido")
nombre = st.text_input("Ingresa tu nombre y apellido", "")

# Botón para abrir Google Sheet
if st.button("Abrir Google Sheet"):
    st.markdown(
        """
        [Haz clic aquí para revisar o editar la hoja de Google Sheets](https://docs.google.com/spreadsheets/d/1qrtz-CNqzIpaWZlK_Z33cDY0P5lKiNqZcINyj1TEX8Y/edit#gid=0)
        """
    )

# Botón para registrar pedido
if st.button("Registrar Pedido"):
    if not nombre:
        st.error("Por favor, ingresa tu nombre.")
        st.stop()

    # Caso: no hay menús disponibles (o eligieron "Ninguno"/"No hay...")
    if opciones_principal_labels[seleccion_principal] in [
        "Ninguno", "No hay menús principales para hoy"
    ]:
        st.error("No has seleccionado ningún menú principal.")
        st.stop()

    # Obtenemos el diccionario completo del plato principal elegido
    plato_dict = opciones_principal_data[seleccion_principal]
    if not plato_dict:
        st.error("Selección inválida. Intenta de nuevo.")
        st.stop()

    # Extra y Acompañamiento
    extra_final = ""
    if seleccion_extra not in ["Ninguno", "No hay extras disponibles hoy"]:
        extra_final = seleccion_extra

    acomp_final = ""
    if seleccion_acomp not in ["Ninguno", "No hay acompañamientos disponibles hoy"]:
        acomp_final = seleccion_acomp

    # Extraemos datos del plato principal
    tipo_menu_final = plato_dict["Tipo de menú"]
    plato_final = f"{plato_dict['Plato']} ($ {plato_dict['Precio']})"

    # Guardamos la fecha actual
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    # Registramos el pedido
    registrar_pedido(
        fecha=fecha_hoy,
        nombre=nombre,
        tipo_menu=tipo_menu_final.strip(),
        plato=plato_final.strip(),
        extra=extra_final.strip(),
        acompanamiento=acomp_final.strip(),
        comentarios=comentarios.strip()
    )
    st.success("¡Pedido registrado con éxito!")

# ==========================
# 9. LISTADO DE PEDIDOS RECIENTES
# ==========================
st.header("📋 Pedidos Recientes")
pedidos = pedidos_worksheet.get_all_records()

if pedidos:
    st.table(pedidos)
else:
    st.write("No hay pedidos registrados aún.")
