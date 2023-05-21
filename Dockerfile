FROM python:3.10-slim

# Install dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
RUN pip install pytest

COPY ./app/ /var/www/

WORKDIR /var/www

EXPOSE 8080
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
