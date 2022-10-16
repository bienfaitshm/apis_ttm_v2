import os

from django.conf import settings
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa


def link_callback(uri, rel):
    print("python>>>>>>>>>>>", uri, rel)
    return settings.BASE_DIR


def link_callback2(uri, rel):  # sourcery skip: raise-specific-error
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    base_dir = settings.BASE_DIR

    print("finder......>>>>>>>", uri, rel)
    # result = finders.find(uri)
    result = None
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        print("paths==============>", uri, rel)
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
            print("paths.........", path)
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
            print("paths2.........", path)
        else:
            return uri

        # make sure that file exists
        # if not os.path.isfile(path):
        #     raise Exception(f'media URI must start with {sUrl} or {mUrl}')
    return base_dir
