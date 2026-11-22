ARG PYTHON_IMAGE=library/python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
FROM ${PYTHON_IMAGE}
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin reference
COPY app.py ./
USER 10001:10001
EXPOSE 8000
CMD ["python", "app.py"]
