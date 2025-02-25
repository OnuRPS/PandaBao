# Imagine de bază mai ușoară
FROM python:3.11-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele necesare în container
COPY . .

# Instalează dependențele din requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Verifică instalarea dependențelor
RUN pip show python-telegram-bot aiohttp requests

# Rulează botul
CMD ["python", "main.py"]
