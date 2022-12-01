import logging

from django.conf import settings
from django.core.mail import send_mail


class SendTicket:
    @classmethod
    def send_ticket(cls, *args, **kwargs):
        print("type setting", dir())
        print("send ticket", kwargs, args)
        if adress := kwargs.get("to"):
            if hasattr(settings, "SEND_TICKET_EMAIL") and settings.SEND_TICKET_EMAIL:
                cls._send_email(to=adress)

    @classmethod
    def _send_email(cls, to: str):
        sended = send_mail(
            subject="Ttm Ticket",
            message="Bonjour vous venez de faire la reservation",
            from_email="ttm.ticket@gmail.com",
            recipient_list=[to],
            fail_silently=False,
        )

        print("sended...........", sended)


class SendEmailReservation:
    def send_email(self, *args, **kwargs):
        print("sended...........", *args, **kwargs)
        logging.info("SEMD EMAIL CONFIRMATION", kwargs)
