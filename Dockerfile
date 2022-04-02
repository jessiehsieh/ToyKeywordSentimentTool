FROM python:3.8-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt
RUN pip install Flask gunicorn
EXPOSE 8080
CMD exec gunicorn --bind :8888 --workers 1 --threads 8 --timeout 0 app:app
