FROM python:3.11

COPY . ./app
RUN pip install --upgrade pip 
RUN pip3 install -r /requirements.txt

WORKDIR /app

EXPOSE 5000
CMD ["gunicorn","--config", "gunicorn_config.py", "run:app"]  