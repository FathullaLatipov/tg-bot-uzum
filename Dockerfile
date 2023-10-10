FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requierements.txt
CMD ["python", "main_bot.py"]