from django.db import models


class Table(models.Model):
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    currentorder = models.IntegerField(default=None, null=True, blank=True)
    joinWith = models.IntegerField(default=None, null=True, blank=True)

    #is_selected = models.BooleanField()
    #is_open = models.BooleanField()
    #name = models.TextField()

    def __str__(self):
        return f"Mesa {self.id} en la posición {self.position_x} - {self.position_y} está unida con la mesa numero: {self.joinWith}"
