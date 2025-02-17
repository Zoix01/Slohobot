from django.db import models

class Word(models.Model):
    order = models.IntegerField()  # Pořadí slova ve větě
    word = models.CharField(max_length=255)  # Samotné slovo

    def __str__(self):
        return f"{self.order}: {self.word}"
