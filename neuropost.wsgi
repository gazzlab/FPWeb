VIRTUAL_ENVIRONMENT = '/var/www/secure/neuropost/virt-env'
activate = VIRTUAL_ENVIRONMENT + '/bin/activate_this.py'
execfile(activate, {'__file__': activate})

from main import app as application

