FROM python:3.12-slim

#Establecer el directorio de trabajo
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#Copiar el resto del código al contenedor
COPY . .
EXPOSE 8501

# Establecer variables de entorno (opcional)
ENV GOOGLE_MAPS_API_KEY="AIzaSyDrTYgq2dNLoFiYVVDbKkWohBXsF6VMYto"

CMD ["streamlit","run","FlappyXLS_v3.py","--server.port=8501","--server.address=0.0.0.0"]