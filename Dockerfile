FROM python:3.13-slim

RUN python -m venv /venv  
ENV PATH="/venv/bin:$PATH"  

RUN pip install --upgrade pip && \
    pip install "django<6" "django-simple-captcha" "django-debug-toolbar" && \
    pip install "django<6" gunicorn  


COPY src /src

WORKDIR /src

CMD ["gunicorn", "--bind", ":8888", "Blog.wsgi:application"]