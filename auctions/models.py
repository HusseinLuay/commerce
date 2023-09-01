from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    Category_name = models.CharField(max_length=50)
    def __str__(self) :
        return self.Category_name

class bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    # def __str__(self) :
    #     return self.bid
    
class Auction_listings(models.Model):
    product_title = models.CharField(max_length=50 , null=False)
    description = models.CharField(max_length=150)
    image_url = models.CharField(max_length=1500)
    price = models.ForeignKey(bid , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    category = models.ForeignKey(Categories , on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(User ,null=True, related_name="watchlist")

class comments(models.Model):
    current_user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Auction_listings , on_delete=models.CASCADE)
    comment = models.CharField(max_length=180)
    def __str__(self) :
        return self.comment
    

    


