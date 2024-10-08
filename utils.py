import streamlit as st
import pandas as pd
import os
import string
import json
from itertools import product

import xml.etree.ElementTree as ET
from xml.dom import minidom


#Directorio donde se guardarán los templates
TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)

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

def generate_excel_columns(max_col='AZ'):
    letters = string.ascii_uppercase
    columnas = []
    max_col_reached = False

    for n in range(1,3): #Para caombinaciones de 1 y 2 letras
        for combo in product(letters, repeat=n):
            col = ''.join(combo)
            columnas.append(col)
            if col == max_col:
                max_col_reached = True
                break
        if max_col_reached:
            break
    return columnas

def column_letter_to_index(column_letter):
    letters = string.ascii_uppercase
    column_letter = column_letter.upper()
    result = 0
    for i, char in enumerate(reversed(column_letter)):
        result += (letters.index(char) + 1) * (26 ** i)
    return result - 1 #Restamos 1 para que A=0, B=1

#Función para generar un XML
def generar_xml(carta_porte_info):

    #Definir namespaces
    namespaces = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'cartaporte20': 'http://www.sat.gob.mx/cartaporte20'
    }

    # Registrar namespaces
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    #Crear elemento raíz
    comprobante_attrib = {
        'Fecha': str(carta_porte_info.get('Fecha', '')),
        'FormaPago': str(carta_porte_info.get('FormaPago', '')),
        'Moneda': str(carta_porte_info.get('Moneda', '')),
        'SubTotal': str(carta_porte_info.get('SubTotal', '')),
        'Total': str(carta_porte_info.get('Total', '')),
        'MetodoPago': str(carta_porte_info.get('MetodoPago', ''))
    }

    comprobante = ET.Element(f"{{{namespaces['cfdi']}}}Comprobante", attrib=comprobante_attrib)
    #Emisor
    emisor = ET.SubElement(comprobante, f"{{{namespaces['cfdi']}}}Emisor", attrib={
        'RFC': str(carta_porte_info.get('RFC Emisor', '')),
        'Nombre': str(carta_porte_info.get('Nombre Emisor', '')),
        'CodigoPostal': str(carta_porte_info.get('Código Postal Emisor', ''))
    })

    #Receptor
    receptor = ET.SubElement(comprobante, f"{{{namespaces['cfdi']}}}Receptor", attrib={
        'RFC': str(carta_porte_info.get('RFC Receptor', '')),
        'Nombre': str(carta_porte_info.get('Nombre Receptor', '')),
        'CodigoPostal': str(carta_porte_info.get('Código Postal Receptor', ''))
    })

    #Origen

    #Destino

    #Mercancías

    #Transporte

    #DatosIdentificadorVehicular

    #Autotransporte

    #Distancia recorrida

    #Conceptos

    #Convertir el árbol XML a una cadena con formato
    xml_str = ET.tostring(comprobante, encoding='utf-8')
    reparsed = minidom.parseString(xml_str)
    pretty_xml = reparsed.toprettyxml(indent=" ")

    return pretty_xml