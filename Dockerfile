FROM python:3.13-slim

RUN python -m venv /venv  
ENV PATH="/venv/bin:$PATH"  

RUN pip install --upgrade pip && \
    pip install "django<6" "django-simple-captcha" "django-debug-toolbar"

COPY src /src

WORKDIR /src

CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]