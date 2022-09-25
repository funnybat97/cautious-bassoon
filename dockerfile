FROM python:3.9

COPY ./requirements.txt /var/project/requirements.txt
COPY ./data /var/project/data
COPY ./navigate /var/project/navigate

ENV PYTHONPATH "${PYTHONPATH}:/var/project/"

RUN pip install -r /var/project/requirements.txt
WORKDIR /var/project
EXPOSE 8000
CMD ["python" ,"navigate/run.py" ]