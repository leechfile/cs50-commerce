from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing',views.create_listing,name="create_listing"),
    path('watch_list',views.watch_list,name='watch_list'),
    # 使用id的方式 使用id来证明 这样你的函数在接收到id的时候就会使用这个url
    path('<int:listing_id>/',views.listing_detail,name='listing_detail'),

]


"""
nav-item 选中的bootstrap类

<div class="listing-container">
    {% for listing in auction_listing %}
        <div class="listing-item">
            <div class="listing-image">
                {% if listing.image_url %}
                    <img class="i-img" src="{{ listing.image_url.url }}" alt="{{ listing.title }}">
                {% endif %}
            </div>
            <div class="listing-details">
                <h3><a href="{% url 'listing_detail' listing.pk %}">{{ listing.title }}</a></h3>
                <p>Current Price: ${{ listing.current_bid }}</p>
                <p>Other Text and Content Here</p>
            </div>
        </div>
        <hr>
    {% endfor %}
</div>



from django.shortcuts import render
from .models import WatchList
from .models import User, AuctionListing
from django.http import HttpResponse

def add_to_watchlist(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']  # 获取用户id
        auction_id = request.POST['auction_id']  # 获取商品id

        user = User.objects.get(pk=user_id)  # 获取用户对象
        auction = AuctionListing.objects.get(pk=auction_id)  # 获取商品对象

        # 创建一个新的WatchList对象并保存
        watchlist_item = WatchList(liker=user, auction=auction)
        watchlist_item.save()

        return HttpResponse("Added to watchlist successfully.")
    else:
        return HttpResponse("Invalid request method")

def filter_watchlist(request, user_id):
    user = User.objects.get(pk=user_id)  # 获取用户对象
    watchlist_items = WatchList.objects.filter(liker=user)  # 筛选用户的所有商品

    # 这里可以根据需要对watchlist_items进行进一步处理

    return render(request, 'watchlist.html', {'watchlist_items': watchlist_items})

"""



