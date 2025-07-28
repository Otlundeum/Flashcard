# Utilise une image officielle Python
FROM python:3.12-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code du projet
COPY . .

# Expose le port 8000
EXPOSE 8000

# Commande de démarrage
CMD ["python", "monblog/manage.py", "runserver", "0.0.0.0:8000"]
