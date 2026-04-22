FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install numpy psutil scipy
CMD ["python", "revised-simplex/problema1-revised.py"]