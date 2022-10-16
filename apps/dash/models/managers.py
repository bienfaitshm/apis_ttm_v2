"""
    managers
"""
from django.db import models


class JourneyManager(models.Manager):
    def more_info(self):
        return self.annotate(

        )
