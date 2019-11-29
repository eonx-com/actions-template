FROM python:3.7

COPY template.py /opt/template/template.py
COPY requirements.txt /opt/template/requirements.txt
COPY TemplateEngine/__init__.py /opt/template/TemplateEngine/__init__.py
COPY TemplateEngine/TemplateBuilder.py /opt/template/TemplateEngine/TemplateBuilder.py
COPY TemplateEngine/TemplateEngine.py /opt/template/TemplateEngine/TemplateEngine.py

COPY entrypoint.sh /bin
ENTRYPOINT ["/bin/entrypoint.sh"]