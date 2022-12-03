import os

from collections import OrderedDict
from dataclasses import dataclass
from typing import List

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


@dataclass
class PassengersPdf:
    name: str
    birth_date: str
    user_type: str
    unit_price: int
    taxe: int
    total_price: int
    taxe_price: int
    devise: str

    def format_with_devise(self, price: int) -> str:
        return f"{price}{self.devise}"

    @property
    def f_unit_price(self):
        return self.format_with_devise(self.unit_price)

    @property
    def f_total_taxe(self):
        return self.format_with_devise(self.total_price)

    @property
    def f_pttc(self):
        return self.format_with_devise(self.total_price)


@dataclass
class InfoReservationPdf:
    pnr: str
    devise: str
    reservation_date: str
    expired_end_date: str
    passengers: List[PassengersPdf]

    @property
    def total_taxe_price(self):
        return sum(passengers.taxe_price for passengers in self.passengers)

    @property
    def total_prices(self):
        return sum(psg.unit_price for psg in self.passengers)

    @property
    def total_ttc(self):
        return

    def format_with_devise(self, price: int) -> str:
        return f"{price}{self.devise}"

    def get_into_dict(self):
        return OrderedDict(
            pnr=self.pnr,
            passengers=self.passengers
        )


def link_callback(uri, rel):  # sourcery skip: raise-specific-error
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    if result := finders.find(uri):
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = [os.path.realpath(path) for path in result]
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(f'media URI must start with {sUrl} or {mUrl}')
    return path


def template_render(value: InfoReservationPdf, template_path: str = "clients/ticket_template.html", ):
    template = get_template(template_path)
    return template.render(value.get_into_dict())


def render_pdf_view(request, html: str):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
    # find the template and render it.

    # return HttpResponse(html)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:  # type: ignore
        return HttpResponse(f'We had some errors <pre>{html}</pre>')
    return response
