FROM python:3.9.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 50001

CMD python main.py
