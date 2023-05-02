FROM python:3.10-slim
ENV TZ="America/Sao_Paulo"
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /tmp/app
WORKDIR /tmp/app
COPY . .
RUN pip install .
CMD ["python", "-m", "funds_explorer_scraper_api"]
