# Language Placement System (DLC Placement)

This application allows testers and advisors to manage student language placement exam results in a database. Advisors can then login to the application to lookup results, get reports, and spreadsheet files for importing into Banner.

## Features

- Django Python Framework Version 1.9
- LDAP connectivity (Requires python-ldap library)
- Banner connectivity (Requires cx_Oracle and Oracle Instant Client libraries)
- CAS Authentication (Requires python-cas and django-cas-ng libraries)

## Usage

To run dlc placement locally you will first need to download a copy of the db.  Db is hosted via EFS in AWS.  To access dbs please connect to the banner whitelist EC2 instance.  Private key can be found in LastPass

```
scp -i "dlc-placement-prod.pem" ec2-user@ec2-54-188-169-201.us-west-2.compute.amazonaws.com:'/home/ec2-user/staging_dbs/*.sqlite3' /YOUR_LOCAL_DB_PATH
```

inside the repo folder run the below command to build the image

```
docker build -t dlc-placement
```

lastly run the app with

```
docker run -p LOCAL_PORT:80 --env-file ./.env -v /YOUR_LOCAL_DB_PATH:/var/www/html/placement/db dlc-placement
```

where local port is an open local port youd like to access the app at.  For example if you select 5000 you would navigate to localhost:5000 to acess the app