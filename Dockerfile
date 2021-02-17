FROM python:2.7
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install libapache2-mod-wsgi
RUN apt-get -y install python-pip
RUN apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev

RUN a2enmod rewrite

ADD ./site-config.conf /etc/apache2/sites-available/000-default.conf 
ADD ./requirements.txt /var/www/html
ADD ./startup.sh /var/www/html 

COPY www  /var/www/html 
WORKDIR /var/www/html
RUN chmod +x  ./startup.sh
RUN pip install -r requirements.txt
RUN chmod 775 /var/www/html/placement/placement 
RUN echo ". /etc/environment" >> /etc/apache2/envvars

EXPOSE 80 3500 
CMD ["/bin/bash", "/var/www/html/startup.sh"]
