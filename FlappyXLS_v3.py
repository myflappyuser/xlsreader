# En esta versión se encontro un detalle de que las columnas solo llegaban de la A-Z y se busca que llegue de la A-AZ

import streamlit as st
import pandas as pd
import json
from dotenv import load_dotenv
import os
from utils import(
    generate_excel_columns,
    column_letter_to_index,
    guardar_template,
    cargar_template,
    listar_templates,
    borrar_template
)
from distance import calcular_distancia_carretera

#Configuración de la página
st.set_page_config("FlappyXLS", layout="wide")

#Titulo de la aplicación
st.title("📄 Extracción de información")

#Campos de la carta porte
campos_carta_porte = [
    "Cantidad",
    "ID unidad embalaje",
    "Descripción material carga",
    "Peso",
    "ID Unidad de peso",
    "Clave de Productos y Servicios",
    "Clave Unidad",
    "Clave Fracción arancelaria",
    "UUID Comercio Exterior",
    "Es material peligroso",
    "Clave material peligroso",
    "Tipo de embalaje",
    "Descripción de embalaje",
    "Aplica tarifa",
    "Tarifa",
    "Importe",
    "Importe Base",
    "Número de pedimento",
    "Fecha",
    "Aduana",
    "Orden",
    "ID Origen",
    "RFC (Remitente)",
    "Calle (Remitente)",
    "Número (Remitente)",
    "Municipio (Remitente)",
    "Estado (Remitente)",
    "Pais (Remitente)",
    "Código postal (Remitente)",
    "Colonia (Remitente)",
    "Localidad (Remitente)",
    "ID (Destinatario)",
    "RFC (Destinatario)",
    "Calle (Destinatario)",
    "Número (Destinatario)",
    "Municipio (Destinatario)",
    "Estado (Destinatario)",
    "Pais (Destinatario)",
    "Código postal (Destinatario)",
    "Colonia (Destinatario)",
    "Localidad (Destinatario)",
    "Distancia Recorrida"
]

#Lista de las columnas disponibles (A-Z)
columnas_disponibles = generate_excel_columns('AZ')
#st.write(columnas_disponibles) #Lo utilizamos para ver hasta donde estaba llegando las columnas

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
            col1, col2, col3 = st.columns([0.4,0.4,0.7])
            with col1:
                #Precargar la columna del template si existe, de lo contrario usar A
                columna = st.selectbox(
                    f"Columna: {campo}", 
                    columnas_disponibles, 
                    index = columnas_disponibles.index(template_actual.get(campo, {}).get('columna','A')),
                    key=f"columna_{campo}"
                    )
                
            
            with col2:
                #Precargar la fila del template si existe, de lo contrario usar 1
                fila = st.number_input(
                    f"Fila: {campo}", 
                    min_value=1, 
                    value=template_actual.get(campo, {}).get('fila', 1),
                    key=f"fila_{campo}"
                    )

            with col3:
                if columna and fila:                
                    #Convertir letra de columna a número de indice (A0,B1,C1)
                    col_num = column_letter_to_index(columna)
                    valor = df.iloc[fila - 2, col_num] #Extraer el valor de la celda
                    st.info(f"{valor}")
                    carta_porte_info[campo] = valor 

                else:
                    st.warning(f"Ingresa la columna y fila para {campo}")

            #Guardar la coordenada en el template
            template_data[campo] = {
                "columna": columna,
                "fila": fila
            }

    col1, col2, col3 = st.columns([1,1,1])
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


