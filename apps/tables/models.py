from django.db import models


class Table(models.Model):
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    is_selected = models.BooleanField()
    is_open = models.BooleanField()
    name = models.TextField()

    def __str__(self):
        return f"Mesa {self.name} en la posición {self.position_x} - {self.position_y} está ocupada?: {self.is_open}"




