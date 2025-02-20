# Imagine de bază
FROM python:3.11

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele în container
COPY . .

# Instalează dependențele
RUN pip install -r requirements.txt

# Rulează botul
CMD ["python", "main.py"]
