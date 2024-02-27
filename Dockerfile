FROM python:3.7-buster
RUN apt-get update
RUN apt-get install -y apt-utils curl apache2 apache2-utils
RUN apt-get -y install libapache2-mod-wsgi-py3=4.6.5-1
RUN apt-get -y install libsasl2-dev python3-dev libldap2-dev libssl-dev
RUN apt-get install -y libaio1 wget unzip
WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

RUN a2enmod rewrite

ADD ./site-config.conf /etc/apache2/sites-available/000-default.conf 
ADD ./requirements.txt /var/www/html
ADD ./startup.sh /var/www/html 

COPY www  /var/www/html 
WORKDIR /var/www/html
RUN wget https://truststore.pki.rds.amazonaws.com/us-west-2/us-west-2-bundle.pem -O us-west-2-bundle.pem -q
RUN chmod +x  ./startup.sh
RUN pip install -r requirements.txt
RUN mkdir /var/www/html/placement/temp
RUN chown :www-data /var/www/html/placement/temp
RUN chmod 775 /var/www/html/placement/temp
RUN chmod 775 /var/www/html/placement/placement
RUN echo ". /etc/environment" >> /etc/apache2/envvars

EXPOSE 80 3500 
CMD ["/bin/bash", "/var/www/html/startup.sh"]
