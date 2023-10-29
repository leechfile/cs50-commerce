from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import User,AuctionListing,Bid,Comment,WatchList
from .form import AuctionListingForm,BidForm,CommentForm,WatchListForm
from django.conf import settings
import os
import pdb

IMAGE_ROOT = settings.MEDIA_ROOT

def create_listing(request):
    """处理表单 以及上传的文件"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            # pdb.set_trace()
            form = AuctionListingForm(request.POST,request.FILES) #  new_listing.image_url = request.FILES
            if form.is_valid():
                # 保存商品到数据库
                new_listing = form.save(commit=False)
                new_listing.creator = request.user  # 关联创建者
                new_listing.save()
                return redirect('listing_detail',new_listing.pk)  # 重定向到新商品的详情页
        else:
            return redirect("index")
    else:
        form = AuctionListingForm()

    return render(request, 'auctions/create_listing.html', {'form': form})

# 使用login require 装饰,需要进行登录
def watch_list(request):
    """add table to the watch list """
    if request.method == 'POST':
        if 'name' in request.POST: # == 'btn-delete-item'
            # pdb.set_trace()
            # delete btn 传来的数据 删除这个数据
            auction_id = request.POST['auction_id']
            item = WatchList.objects.filter(liker=request.user,auction=auction_id)
            item.delete()
            data = request.POST.dict()
            data['status'] = 'success'
            return JsonResponse(data)

        elif 'auction_id' in request.POST:
            # 获取到user-id , auction - id  储存watch form
            # pdb.set_trace()
            watch_info = request.POST
            watch_form = WatchList()
            watch_form.liker = request.user
            watch_form.auction = AuctionListing.objects.get(pk=watch_info['auction_id'])
            watch_form.save()
            return redirect("listing_detail",watch_info['auction_id'])

    # 得到auction id
    auction_ids = WatchList.objects.filter(liker=request.user).values_list('auction',flat=True)
    # 得到 acution list 使用数据库的In方法 来筛选所有id在列表中的商品
    auction_list = AuctionListing.objects.filter(id__in=auction_ids) # [get_object_or_404(AuctionListing,id=wid) for wid in watch_id]
    context = {'auction_list':auction_list}
    return render(request,'auctions/watch_list.html',context)

def index(request):
    """重名函数 也可能会导致原本的变量名字被占用"""
    # 查询数据库获取所有活动商品列表
    active_listings = AuctionListing.objects.filter(is_active=True)
    # pdb.set_trace()

    return render(request, 'auctions/index.html', {'active_listings': active_listings })

def listing_detail(request, listing_id):
    """为每一个单独的商品简历 使用最高的进行排序 使用urls来传递图片的真实路径"""
    listing = get_object_or_404(AuctionListing, id=listing_id)

    # 完整的comments
    bids = Bid.objects.filter(listing=listing).order_by('-amount')
    comments = Comment.objects.filter(listing=listing).order_by('-timestamp')

    bid_form = BidForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'bid_button' in request.POST:  # 处理投标表单
            bid_form = BidForm(request.POST)
            new_bid = bid_form.save(commit=False)
            new_bid.bidder = request.user
            new_bid.listing = listing
            new_bid.save()

            # 获取最高的投标金额, 并且保存最高投标金额
            highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
            if highest_bid:
                listing.current_bid = highest_bid.amount
                listing.save()

        elif 'comment_button' in request.POST:  # 处理评论表单
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.commenter = request.user
                new_comment.listing = listing
                new_comment.save()
        return redirect('listing_detail', listing_id=listing_id)


    context = { 'listing': listing,
                'bids': bids,
                'bid_form': bid_form,
                'comment_form': comment_form,
                'comments': comments,
                # 'image_url':os.path.join(IMAGE_ROOT,listing.image_url),
                }

    return render(request, 'auctions/listing_detail.html', context)




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



