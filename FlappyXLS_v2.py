# En esta versión lo que haremos es que se podrán guardan las filas y columnas en un template predeterminado.

import streamlit as st
import pandas as pd
import json
import os

st.set_page_config("FlappyXLS", layout="wide")

#Directorio donde se guardarán los templates
TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)

#Titulo de la aplicación
st.title("Extracción de información")

#Campos de la carta porte
campos_carta_porte = [
    "Cantidad",
    "ID unidad embalaje",
    "Descripción material carga"
]

#Lista de las columnas disponibles (A-Z)
columnas_disponibles = [chr(i) for i in range (65,91)] #De A a Z


# ------------------FUNCIONES------------------

#Función para guardar el template en un archivo JSON
def guardar_template(nombre_template, template_data):
    template_path = os.path.join(TEMPLATE_DIR, f"{nombre_template}.json")
    with open(template_path, "w", encoding="utf=8") as f:
        json.dump(template_data, f, indent=4, ensure_ascii=False)
    st.success(f"Template guardado como {nombre_template}.json")

#Función para cargar un template desde un archivo JSON
def cargar_template(nombre_template):
    template_path = os.path.join(TEMPLATE_DIR, f"{nombre_template}.json")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    else: 
        st.error(f"Template '{nombre_template}' no encontrado")
        return {}
    
#Función para listar templates existentes
def listar_templates():
    templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".json")]
    templates_nombres = [os.path.splitext(f)[0] for f in templates]
    return templates_nombres

#Función para eliminar template desde un archivo JSON
def borrar_template(nombre_template):
    template_path = os.path.join(TEMPLATE_DIR, f"{nombre_template}.json")
    if os.path.exists(template_path):
        os.remove(template_path)

# -----------------SIDEBAR------------------
#Sidebar para gestionar templates
st.sidebar.header("Gestión de templates")

#Seleccionar un template existente o crear uno nuevo
templates_existentes = listar_templates()
opciones_templates = ["Escoge una opción"] + templates_existentes + ["Nuevo template"]
template_seleccionado = st.sidebar.selectbox("Selecciona un template", opciones_templates, index=0)

#Si no se ha seleccionado ningúna opción, no hacer nada
if template_seleccionado == "Escoge una opción":
    st.sidebar.info("Selecciona un template o crea uno nuevo")
else:     #Si se selecciona un template seguir con la lógica actual
    #Variable para almacenar el template actual
    template_actual = {}

    #Input para el nombre del template si se está creando uno nuevo
    if template_seleccionado == "Nuevo template":
        nombre_template = st.sidebar.text_input("Nombre del nuevo template", placeholder="Ejemplo: Empresa A")
        if nombre_template:
            st.sidebar.success(f"{nombre_template}")
        else:
            st.sidebar.warning("Ingresa un nombre para el nuevo template")

    #Si se selecciona un template existente, cargarlo
    if template_seleccionado in templates_existentes:
        template_actual = cargar_template(template_seleccionado)
        st.sidebar.success(f"Template '{template_seleccionado}' cargado")
    elif template_seleccionado == "Nuevo template":
        st.sidebar.info("Crea un nuevo template ingresando el nombre y configurando las columnas y filas")
    

    #---------------------AREA PRINCIPAL ---------------------------
    #Area principal para configurar el template
    st.subheader("Configura las columnas y las filas para cada campo")

    # ------------------EXCEL------------------

    #Subir el archivo de excel
    archivo_excel = st.file_uploader("Sube tu archivo de Excel", type= ["xlsx", "xls"])

    if archivo_excel:
        #Cargar el archivo de excel usando pandas
        excel_data = pd.read_excel(archivo_excel, sheet_name=None) #Leer todas las hojas del excel
        st.success("El archivo se ha cargado con exito")

        #Mostrar las hojas disponibles
        hoja_seleccionada = st.selectbox("Seleccione la hoja de excel", excel_data.keys())
        df = excel_data[hoja_seleccionada] #Datos de la hoja seleccionada

        #Crear diccionarrio para almacenar las coordenadas de los templates
        template_data = {}

        #Crear diccionario para el JSON
        carta_porte_info = {}

        st.subheader("Indica la columna y la fila para cada campo")
        
        #Obtener columna y fila para cada campo
        for campo in campos_carta_porte:
            col1, col2 = st.columns([2,1])
            with col1:
                #Precargar la columna del template si existe, de lo contrario usar A
                columna = st.selectbox(
                    f"Columna para {campo}", 
                    columnas_disponibles, 
                    index = columnas_disponibles.index(template_actual.get(campo, {}).get('columna','A'))
                    #key=f"columna_{campo}")
                )
            
            with col2:
                #Precargar la fila del template si existe, de lo contrario usar 1
                fila = st.number_input(
                    f"Fila para {campo}", 
                    min_value=1, 
                    value=template_actual.get(campo, {}).get('fila', 1)
                    #key=f"fila_{campo}"
                    )

            if columna and fila:                
                #Convertir letra de columna a número de indice (A0,B1,C1)
                col_num = ord(columna.upper()) - 65
                valor = df.iloc[fila - 2, col_num] #Extraer el valor de la celda
                st.success(f"{campo}: {valor}")
                carta_porte_info[campo] = valor 

            else:
                st.warning(f"Ingresa la columna y fila para {campo}")

            #Guardar la coordenada en el template
            template_data[campo] = {
                "columna": columna,
                "fila": fila
            }


    col1, col2, col3 = st.columns(3)
    with col1:
        #Botón para guardar el template
        if template_seleccionado == "Nuevo template" and st.button("Guardar nuevo template"):
            if nombre_template:
                guardar_template(nombre_template, template_data)
            else:
                st.sidebar.error("Ingresa un nombre para el nuevo template")

        elif template_seleccionado in templates_existentes and st.button("Guardar cambios del template"):
            guardar_template(template_seleccionado, template_data)

    with col3:
        #Botón para borrar el template
        if template_seleccionado in templates_existentes:
            if st.button("Borrar template"):
                borrar_template(template_seleccionado)
                st.success(f"Template '{template_seleccionado}' eliminado. Favor de recargar la página")

    #Mostrar el JSON generado
    if st.button("Generar JSON"):
        carta_porte_json = json.dumps(carta_porte_info, indent=4, ensure_ascii=False)
        st.subheader("Datos extraidos en formato JSON")
        st.code(carta_porte_json, language="json")


