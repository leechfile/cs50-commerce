from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# 拍卖列表模型
class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.ImageField(upload_to='gimages/')
    category = models.CharField(max_length=50, choices=[
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        # 添加更多类别
    ])
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# 投标模型
class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid on {self.listing.title} by {self.bidder.username}"

# 评论模型
class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.listing.title} by {self.commenter.username}"

#增加评论模型
class WatchList(models.Model):

    liker = models.ForeignKey(User,on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
# 加入listing 和 User的


