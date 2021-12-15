FROM python:3.8

RUN pip3.8 install flask==2.0.0

ADD code /code
WORKDIR /code
CMD ["python", "vk_api_mock.py"]
