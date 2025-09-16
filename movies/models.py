from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_image/')
    amount_left = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
    def is_avaliable(self):
        return self.amount_left is None or self.amount_left > 0
    
    def reduce_stock(self, qty=1):
        if self.amount_left is not None and self.amount_left > 0:
            self.amount_left = max(self.amount_left-qty, 0)
            self.save()
            
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
