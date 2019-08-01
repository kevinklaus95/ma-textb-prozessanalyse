# Start with a Python image.
FROM nikolaik/python-nodejs:latest

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

# Install some necessary things.
RUN apt-get update \
    && apt-get install -y libssl-dev dpkg-dev libpq-dev python-dev \
    && pip install -U pip==19.0.2 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && mkdir /code

WORKDIR /code
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

EXPOSE 8000

# Copy all our files into the image.
COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]