from django.db import models


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live now'),
        ('sold', 'Sold out'),
    ]

    name = models.CharField(max_length=160)
    details = models.CharField(max_length=220)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    tickets_sold = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['date', 'name']

    def __str__(self):
        return self.name
