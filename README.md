FlappyXLS - Extracción de Información desde Excel para Carta Porte
Bienvenido a FlappyXLS, una aplicación desarrollada con Streamlit que permite extraer información específica de archivos Excel para generar un JSON o XML con los datos necesarios para una Carta Porte. Esta herramienta es útil para empresas que manejan diferentes formatos de Excel y necesitan extraer información de manera eficiente y consistente.

Atributos del Comprobante
Version (Ej. "3.3")
Serie (Ej. "A")
Folio (Ej. "12345")
Fecha (Formato: "2024-10-07T12:00:00")
Sello (Ej. "...")
FormaPago (Ej. "99")
NoCertificado (Ej. "00001000000403258748")
Certificado (Ej. "...")
SubTotal (Ej. "0.00")
Moneda (Ej. "XXX")
Total (Ej. "0.00")
TipoDeComprobante (Ej. "I")
MetodoPago (Ej. "PPD")
LugarExpedicion (Ej. "12345")
Emisor
Rfc
Nombre
RegimenFiscal
Receptor
Rfc
Nombre
UsoCFDI
Complemento > CartaPorte
Version (Ej. "2.0")
TranspInternac (Ej. "No")
Ubicacion Origen
TipoUbicacion (Fijo: "Origen")
Calle
NoExterior
Colonia
Municipio
Estado
Pais
CodigoPostal
Ubicacion Destino
TipoUbicacion (Fijo: "Destino")
Calle
NoExterior
Colonia
Municipio
Estado
Pais
CodigoPostal
Mercancias > Mercancia
BienesTransp
Descripcion
PesoBruto
PesoNeto
UnidadPeso
FraccionArancelaria
Transporte
DatosEmbarque
TipoTransporte
PermSCT
DatosIdentificacionVehicular
TipoVehiculo
Placa
Autotransporte
RFCChofer
NombreChofer
NumPermiso
Ruta > Tramo
DistanciaRecorrida
IdentificacionTramo
Ubicacion Intermedio
TipoUbicacion (Fijo: "Intermedio")
Calle
NoExterior
Colonia
Municipio
Estado
Pais
CodigoPostal
Conceptos > Concepto
ClaveProdServ
Cantidad
ClaveUnidad
Unidad
Descripcion
ValorUnitario
Importe
Impuestos
TotalImpuestosTrasladados
Traslados
