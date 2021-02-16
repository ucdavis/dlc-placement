FROM python:2.7
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install libapache2-mod-wsgi
RUN apt-get -y install python-pip
RUN apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev


ADD ./site-config.conf /etc/apache2/sites-available/000-default.conf 
ADD ./requirements.txt /var/www/html
ADD ./startup.sh /var/www/html 

COPY www  /var/www/html 
WORKDIR /var/www/html
RUN chmod 777 ./startup.sh
RUN pip install -r requirements.txt
RUN ls
RUN pwd
RUN mkdir /var/www/html/placement/logs
RUN chmod 775 /var/www/html/placement/logs
RUN chown :www-data /var/www/html/placement/logs
RUN chmod 775 /var/www/html/placement/placement 
#RUN chmod 664 /var/www/html/placement/db.sqlite3 
#RUN chmod 664 /var/www/html/placement/production.sqlite3
#RUN chown :www-data /var/www/html/placement/db.sqlite3
#RUN chown :www-data /var/www/html/placement/production.sqlite3 
RUN chmod 777 /var/www/html/placement #TODO remove once permission issue figured out
RUN echo ". /etc/environment" >> /etc/apache2/envvars

EXPOSE 80 3500 
CMD ["/bin/bash", "/var/www/html/startup.sh"]
#CMD ["apachectl", "-D", "FOREGROUND"]