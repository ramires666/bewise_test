FROM python:3.11-slim
WORKDIR /app
ADD . /app
#RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
LABEL authors="grom.alexey"
ENTRYPOINT ["python", "main.py"]