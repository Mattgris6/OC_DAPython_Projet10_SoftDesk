import os

command = 'flake8 softdesk/itsystem/views.py softdesk/itsystem/serializers.py '\
    'softdesk/itsystem/permissions.py'\
    ' softdesk/itsystem/models.py softdesk/itsystem/admin.py softdesk/softdesk/urls.py'\
    ' softdesk/softdesk/settings.py'\
    ' --max-line-length 119 --format=html --htmldir=flake8_rapport'
os.system(command)