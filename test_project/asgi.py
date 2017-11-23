import os, sys

# add the hellodjango project path into the sys.path
sys.path.append('/home/env3/sockets')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/env3/lib/python3.5/site-packages')

from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

channel_layer = get_channel_layer()
