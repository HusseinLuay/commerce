from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *




def index(request):
    active_lists = Auction_listings.objects.filter(is_active=True)
    category = Categories.objects.all()
    return render(request, "auctions/index.html" , {"active_listings":active_lists , "categories":category})

def specific_category(request):
    if request.method == "POST":
        s_c = request.POST['Category']
        specific_c = Categories.objects.get(Category_name = s_c )
        active_lists = Auction_listings.objects.filter(is_active=True , category = specific_c)
        all_categories = Categories.objects.all()
        return render(request, "auctions/index.html" , {"active_listings":active_lists , "categories":all_categories } )


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
    


def create_Listing(request):
    if request.method == "GET":
        allCatgories = Categories.objects.all()
        return render ( request , "auctions/create_listing.html" , {"all_categories" : allCatgories})
    if request.method =="POST":
        t = request.POST["title"]
        d = request.POST["desc"]
        i = request.POST["Img_URL"]
        p = float(request.POST["Product_Price"])
        c = request.POST["Category"]
        u = request.user

        thebid = bid(bid = float(p) , user = u )
        thebid.save()
        fetch_category = Categories.objects.get(Category_name = c )
        new_product = Auction_listings(product_title = t , description = d , image_url = i ,  price = thebid , category = fetch_category , owner = u)
        new_product.save()
        return HttpResponseRedirect( reverse("index"))
    

def show_item(request , id ):
    product_info = Auction_listings.objects.get(pk=id)
    iswatchlist = request.user in product_info.watchlist.all()
    Allcomments = comments.objects.filter(product = product_info)
    isowner = request.user.username == product_info.owner.username
    return render (request , "auctions/show_item.html" , {"product_information" : product_info , "watchlist":iswatchlist , "comments":Allcomments , "isOwner":isowner})

def watchlist(request):
    user = request.user 
    products = user.watchlist.all() #here we mean the "related name in many to mant relationship" by watchlist 
    return render ( request , "auctions/watchlist.html" , {"active_listings":products})

def addwatchlist(request , id ):
    product_info = Auction_listings.objects.get(pk=id)
    user = request.user 
    product_info.watchlist.add(user)
    return HttpResponseRedirect(reverse("showitem", args=(id, ) ))

def removewatchlist(request , id ):
    product_info = Auction_listings.objects.get(pk=id)
    user = request.user 
    product_info.watchlist.remove(user)
    return HttpResponseRedirect(reverse("showitem" , args=(id, ) ))

def comment(request , id ) :
    product_info = Auction_listings.objects.get(pk=id)
    user = request.user 
    comment = request.POST['comment']
    add_comment = comments(current_user = user , product = product_info , comment = comment)
    add_comment.save()
    return HttpResponseRedirect(reverse("showitem" , args=(id, ) ))

def add_bid(request , id ) :
    newBid = float(request.POST['new_bid'])
    product_info = Auction_listings.objects.get(pk=id)

    iswatchlist = request.user in product_info.watchlist.all()
    Allcomments = comments.objects.filter(product = product_info)

    if newBid > product_info.price.bid:
        updateBid = bid(user = request.user , bid = newBid)
        updateBid.save()
        product_info.price = updateBid
        product_info.save()
        return render ( request , "auctions/show_item.html" , {"product_information":product_info , "message" :"congralations ! , The buying has been completed" , "update" : True , "watchlist":iswatchlist , "comments":Allcomments})
    else :
         return render ( request , "auctions/show_item.html" , {"product_information":product_info , "message" :"sorry ! , The buying failed" , "update" : False , "watchlist":iswatchlist , "comments":Allcomments})


def close_Auction(request,id):
    product_info = Auction_listings.objects.get(pk=id)
    product_info.is_active = False
    product_info.save()
    iswatchlist = request.user in product_info.watchlist.all()
    Allcomments = comments.objects.filter(product = product_info)
    isowner = request.user.username == product_info.owner.username
    return render ( request , "auctions/show_item.html" , {"product_information":product_info , "message" :"Your auction is closed" , "update" : True , "watchlist":iswatchlist , "comments":Allcomments , "isOwner":isowner})



