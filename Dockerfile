FROM python:3.7

COPY template.py /opt/template/template.py
COPY requirements.txt /opt/template/requirements.txt

COPY entrypoint.sh /bin
ENTRYPOINT ["/bin/entrypoint.sh"]