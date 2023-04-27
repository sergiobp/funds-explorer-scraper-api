FROM python:3.10-slim
ENV TZ="America/Sao_Paulo"
ENV PYTHONUNBUFFERED=1
COPY dist/*.whl /tmp
RUN pip install /tmp/*.whl
CMD ["python", "-m", "funds_explorer_scraper_api"]
