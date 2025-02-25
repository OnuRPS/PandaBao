# Imagine de bază mai ușoară
FROM python:3.11-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele necesare în container
COPY . .

# Instalează dependențele din requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Rulează botul
CMD ["python", "main.py"]
