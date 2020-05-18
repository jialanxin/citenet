FROM python:slim

WORKDIR /app
COPY ./main.py .
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir 
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","443","--ssl-keyfile","/app/lxj230.key","--ssl-certfile","/app/lxj230.pem"]