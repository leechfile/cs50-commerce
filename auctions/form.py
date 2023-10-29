from django import forms
from .models import AuctionListing,Bid,Comment,WatchList

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class WatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = ['liker','auction']
