FROM python:3.8


WORKDIR /app

# set the flags for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install gcc
RUN apt-get update && apt-get install gcc git -y && apt-get clean autoclean && apt-get autoremove -y

# upgrade pip
RUN pip install --upgrade pip

# install requirements
#COPY ./requirements.txt .

# install requirements
RUN pip install --no-cache flask

# Clone the latest version of the Flask application
RUN git clone https://github.com/yancyvance/dev-server.git .

# Expose the port
EXPOSE 5000

# Run the server
#CMD ["python3", "server.py"]

# Run the application and keep it updated
CMD git pull origin main && python server.py
