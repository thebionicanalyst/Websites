# Use the official Python image from Docker Hub
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt

# Set the working directory
WORKDIR /code

# Copy the project files
COPY . /code/

# Expose ports for Django and Streamlit
EXPOSE 1111
EXPOSE 2222

# Command to run the application
CMD ["sh", "-c", "python portfoliowebsite/manage.py runserver 0.0.0.0:1111 & streamlit run portfoliowebsite/StBionicHealth.py --server.port 2222 --server.headless true"]
