FROM python:3.9.2-buster

# chrome yükle ve temizle
RUN apt-get update
RUN apt-get install zip unzip -y
RUN apt-get install fonts-liberation -y
RUN apt-get install libasound2 -y
RUN apt-get install libatk-bridge2.0-0 -y
RUN apt-get install libatk1.0-0 -y
RUN apt-get install libatspi2.0-0 -y
RUN apt-get install libcups2 -y
RUN apt-get install libdbus-1-3 -y
RUN apt-get install libdrm2 -y
RUN apt-get install libgbm1 -y
RUN apt-get install libgtk-3-0 -y
RUN apt-get install libnspr4 -y
RUN apt-get install libnss3 -y
RUN apt-get install libxcomposite1 -y
RUN apt-get install libxdamage1 -y
RUN apt-get install libxfixes3 -y
RUN apt-get install libxkbcommon0 -y
RUN apt-get install libxrandr2 -y
RUN apt-get install libxshmfence1 -y
RUN apt-get install xdg-utils -y
RUN apt-get install libu2f-udev -y
RUN apt-get install libvulkan1 -y
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

#chromedriver indir version 89 için. ve temizle
WORKDIR /usr/bin
RUN wget https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN rm chromedriver_linux64.zip

WORKDIR /app
COPY . .
RUN git config --global user.email "safaemreyildirim@gmail.com"
RUN git config --global user.name "Safa Emre YILDIRIM"
RUN mkdir .venv
RUN pip install pipenv
RUN pipenv install
# CMD [ "pipenv", "run", "celery", "-A", "app.celery", "worker", "--loglevel=INFO", "&&", "pipenv", "run", "python", "run.py" ]
# CMD [ "pipenv", "run", "celery", "-A", "app.celery:app", "worker", "--loglevel=INFO"]
# CMD [ "pipenv", "run", "python", "run.py" ]