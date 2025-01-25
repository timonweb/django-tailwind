FROM python:3.12-slim-bookworm

WORKDIR /app

ARG NODE_MAJOR=18

RUN apt-get update \
  && apt-get install -y ca-certificates curl gnupg \
  && mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
  && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
  && apt-get update \
  && apt-get install nodejs -y \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && chown python:python -R /app

USER python

COPY --chown=python:python requirements*.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip list

# ENV DEBUG="${DEBUG}" \
ENV PYTHONUNBUFFERED="true" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

COPY --chown=python:python . .

WORKDIR /app

RUN python manage.py tailwind install --no-input;
RUN python manage.py tailwind build --no-input;
RUN python manage.py collectstatic --no-input;
# RUN SECRET_KEY=nothing python manage.py tailwind install --no-input;
# RUN SECRET_KEY=nothing python manage.py tailwind build --no-input;
# RUN SECRET_KEY=nothing python manage.py collectstatic --no-input;

CMD ["python", "manage.py", "runserver"]
