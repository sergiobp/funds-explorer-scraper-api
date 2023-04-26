FROM python:3.10-slim
ENV TZ="America/Sao_Paulo"
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY . .
RUN pip install .
CMD ["python", "-m", "funds_explorer_scraper_api"]
