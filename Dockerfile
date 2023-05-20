FROM python:3.10-slim

COPY ./app/ /var/www/
WORKDIR /var/www

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt



EXPOSE 8080
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
