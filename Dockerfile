FROM python:3.11-slim

WORKDIR /app
ADD . /app

# Install 'curl' and 'wait-for-it' script
RUN apt-get update && apt-get install -y curl \
    && curl -o /app/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /app/wait-for-it.sh \
    && pip install -r requirements.txt

EXPOSE 5000

LABEL authors="grom.alexey"

ENTRYPOINT ["./wait-for-it.sh", "db:5432", "--", "python", "main.py"]