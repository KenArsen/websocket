from django.db import models


class Role(models.TextChoices):
    GUEST = "GUEST", "GUEST"
    DISPATCHER = "DISPATCHER", "DISPATCHER"
    HR = "HR", "HR"
    ACCOUNTANT = "ACCOUNTANT", "ACCOUNTANT"
    DRIVER = "DRIVER", "DRIVER"
