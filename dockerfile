FROM alpine:latest

RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    apache2 \
    curl \
    git \
    libapache2-mod-php5 \
    php5 \
    php5-mcrypt \
    php5-mysql \
    python3.4 \
    python3-pip

RUN pip install "fastapi[standard]"
RUN pip install "astropy[recommended]" --upgrade
RUN pip install -U --pre "astroquery"