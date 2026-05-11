FROM python:3-slim
WORKDIR /programas/ingesta
RUN pip3 install boto3 pymysql
COPY . .
CMD [ "python3", "./ingesta.py" ]
