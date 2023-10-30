FROM python:3.10
EXPOSE 5002
RUN mkdir -p /opt/Terapia_bot
WORKDIR /opt/Terapia_bot

RUN mkdir -p /opt/Terapia_bot/requirements
ADD requirements.txt /opt/Terapia_bot/

COPY . /opt/Terapia_bot/

RUN pip install -r requirements.txt
CMD ["python", "/opt/Terapia_bot/main.py"]