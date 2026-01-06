# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the topic_summary directory
COPY topic_summary /app/topic_summary

# Install dependencies
RUN pip install --no-cache-dir streamlit crewai[tools]==1.7.2

# Set the working directory to topic_summary
WORKDIR /app/topic_summary

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
