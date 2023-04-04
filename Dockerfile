FROM python:3.9-slim-buster


WORKDIR /app


COPY . /app


RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install protobuf==3.20.0

EXPOSE 8501

CMD ["streamlit", "run", "myapp.py"]
