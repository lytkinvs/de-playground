FROM apache/superset:latest


user root

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt


COPY ./superset-init.sh /app/superset-init.sh

RUN chmod +x /app/superset-init.sh
# COPY superset_config.py /app/
# ENV SUPERSET_CONFIG_PATH /app/superset_config.py
user superset
ENTRYPOINT ["/app/superset-init.sh"]