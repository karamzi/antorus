# Укажите необходимую версию python
FROM python:3.8

RUN apt update
RUN apt install netcat-traditional

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR /opt/antorus

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'antorus.settings'

# Скопируйте в контейнер файлы, которые редко меняются
COPY req.txt req.txt
COPY uwsgi.ini uwsgi.ini

# Установите зависимости
RUN  pip install --upgrade pip \
     && pip install -r req.txt --no-cache-dir

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла.
COPY . .

RUN chmod +x docker-entrypoint.sh

# Укажите, как запускать ваш сервис
ENTRYPOINT ["./docker-entrypoint.sh"]