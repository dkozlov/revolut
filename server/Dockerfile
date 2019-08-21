FROM python:3-slim
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements/prod.txt
EXPOSE 8080
CMD [ "gunicorn", "--bind", "0.0.0.0:8080","manage:app" ]
