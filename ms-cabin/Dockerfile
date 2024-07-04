# Utiliza una imagen base con Python 3.10 Slim (Debian Bullseye)
FROM python:3.10-slim-bullseye

# Establece las variables de entorno
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.local/bin

# Instala las dependencias del sistema necesarias para psycopg2
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /home/flaskapp

# Copia los archivos de la aplicación
COPY ./app ./app
COPY ./app.py .

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000
EXPOSE 5000

# Define el comando de inicio de la aplicación
#CMD ["python", "./app.py"]
CMD [ "gunicorn", "--workers", "1", "--log-level", "INFO", "--bind", "0.0.0.0:5000", "app:create_app()" ]
