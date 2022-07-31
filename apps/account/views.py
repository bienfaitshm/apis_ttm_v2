from rest_framework import viewsets

from .models import Client, Company, Employe
from .serializers import ClientSerializer, CompanySerializer, EmployeSerializer


class ClientView(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class EmployeView(viewsets.ModelViewSet):
    serializer_class = EmployeSerializer
    queryset = Employe.objects.all()
