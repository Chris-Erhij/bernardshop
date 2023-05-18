from django.db import models
from django.db.models import (
    Model, CharField, DateTimeField, IntegerField, BooleanField,
)
from django.core.validators import MaxValueValidator, MinValueValidator


class Coupon(Model):
    code: CharField = models.CharField(max_length=50, unique=True)
    valid_from: DateTimeField = models.DateTimeField()
    valid_to: DateTimeField = models.DateTimeField()
    discount: IntegerField = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                help_text="Percentage value (0 to 100)"
                                                )
    active: BooleanField = models.BooleanField()

    def __str__(self) -> str:
        return self.code
