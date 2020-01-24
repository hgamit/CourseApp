import ldap, os
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_SERVER_URI = os.environ.get("LDAP_HOST")
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_BIND_DN = os.environ.get("LDAP_USERNAME")
AUTH_LDAP_BIND_PASSWORD = os.environ.get("LDAP_PASSWORD")
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=mybiz,dc=mybiz,dc=com", ldap.SCORE.SUBTREE, "sAMAccountName=%(user)s"
)
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

#https://fle.github.io/combine-ldap-and-classical-authentication-in-django.html
##https://sixfeetup.com/blog/new-ldap3-python-ldap-library