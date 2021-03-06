from django.db import models


class Table(models.Model):
    name = models.CharField(max_length=200, default="Nueva mesa")
    x = models.IntegerField()
    y = models.IntegerField()
    join_with = models.OneToOneField("self", on_delete=models.CASCADE, null=True, blank=True)
    join_direction = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Mesa '{self.name}' con id {self.id} en [{self.x}, {self.y}]"
