from django.db import models


class Client(models.Model):
    NATURAL = 'natural'
    LEGAL = 'legal'
    CLIENT_TYPE_CHOICES = [
        (NATURAL, 'Persona Natural'),
        (LEGAL, 'Persona Jurídica'),
    ]
    code = models.CharField(max_length=20, unique=True)
    client_type = models.CharField(max_length=10, choices=CLIENT_TYPE_CHOICES)
    dni = models.CharField(max_length=12, blank=True, null=True)
    ruc = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.code} - {self.name}"
