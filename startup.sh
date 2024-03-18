#!/usr/bin/env bash
echo "export LDAP_PASS=${LDAP_PASS}" >> /etc/environment
echo "export LDAP_SERVER=${LDAP_SERVER}" >> /etc/environment
echo "export LDAP_BASE=${LDAP_BASE}" >> /etc/environment
echo "export LDAP_USER=${LDAP_USER}" >> /etc/environment
echo "export CAS_SERVER_URL=${CAS_SERVER_URL}" >> /etc/environment
echo "export EMAIL_HOST=${EMAIL_HOST}" >> /etc/environment
echo "export EMAIL_PORT=${EMAIL_PORT}" >> /etc/environment
echo "export EMAIL_HOST_USER=${EMAIL_HOST_USER}" >> /etc/environment
echo "export EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" >> /etc/environment
echo "export SECRET_KEY=${SECRET_KEY}" >> /etc/environment
echo "export EMAIL_USE_TLS=${EMAIL_USE_TLS}" >> /etc/environment
echo "export DEBUG_APP=${DEBUG_APP}" >> /etc/environment
echo "export ALLOWED_HOSTS=${ALLOWED_HOSTS}" >> /etc/environment
echo "export CSRF_TRUSTED_ORIGINS=${CSRF_TRUSTED_ORIGINS}" >> /etc/environment
echo "export EMAIL_FAIL_SILENTLY=${EMAIL_FAIL_SILENTLY}" >> /etc/environment
echo "export ADMIN_EMAIL_LIST=${ADMIN_EMAIL_LIST}" >> /etc/environment
echo "export BANNER_HOST=${BANNER_HOST}" >> /etc/environment
echo "export BANNER_USER=${BANNER_USER}" >> /etc/environment
echo "export BANNER_PASS=${BANNER_PASS}" >> /etc/environment
echo "export BANNER_PORT=${BANNER_PORT}" >> /etc/environment
echo "export BANNER_DB=${BANNER_DB}" >> /etc/environment
echo ". /etc/environment" >> /etc/apache2/envvars
apachectl -D FOREGROUND