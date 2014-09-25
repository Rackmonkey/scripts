scripts
=======

## readme explanations ##

**dependency:** Scripts you must start before you can use it. 

## setup_debian_basics ##
Installs some basic tools and add the sid repo to sources.list for the newest Apache and PHP  
**dependency:** -

## setup_apache_phpfpm_fcgi ##
Installs a full Apache 2.4, PHP-fpm 5.6 and fcgi Setup.  
**dependency:** setup_debian_basics  


## setup_domain ##

Setups a vHost for an Domain.  
**dependency:** setup_apache_phpfpm_fcgi **&&** setup_debian_basics
