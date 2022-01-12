FROM python:3.8.5
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python app.py
EXPOSE 5000