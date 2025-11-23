FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install -- no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "app/main.py"]