FROM python:3.9.18
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "katlonbot.py"]
