from apps.dash.models import Ticket


class TicketService:
    model = Ticket

    def create_passengers_ticket(self, *args, **kwargs):
        passengers = kwargs.get("passengers", [])
        tickets = [self.model(**passenger) for passenger in passengers]
        self.model.objects.bulk_create(tickets)
