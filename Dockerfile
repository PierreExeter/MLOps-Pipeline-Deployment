FROM python:3.11-slim

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
ADD . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the training script to generate pycaret-model.pkl
RUN python src/train_model.py

# Expose port 
EXPOSE 5000

# Run the application
CMD ["python", "src/app.py"]
