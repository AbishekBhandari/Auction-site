from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def listing(request, id):
    listingData = Listing.objects.filter(pk=id).first()
    if listingData is None:
        return HttpResponseRedirect(reverse("index"))
    else:
        isOwner = request.user == listingData.owner
        isListingInWatchList = request.user in listingData.watchlist.all()
        allComments = Comment.objects.filter(listing=listingData)
        return render(request, 'auctions/listing.html', {
            'listing': listingData,
            'isListingInWatchList': isListingInWatchList,
            "allcomments": allComments,
            "isOwner": isOwner,
        })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isListingInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    return render(request, 'auctions/listing.html', {
            'listing': listingData,
            'isListingInWatchList': isListingInWatchList,
            "allcomments": allComments,
            "isOwner": isOwner,
        })

def addBid(request, id):
    newBid = request.POST["newBid"]
    listingData = Listing.objects.get(pk=id)
    isListingInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    if int(newBid) > listingData.price.bid:
        updatedBid = Bid(user=request.user, bid=newBid)
        updatedBid.save()
        listingData.price = updatedBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid was updated successfully",
            "updated": True,
            "allcomments": allComments,
            "isListingInWatchList": isListingInWatchList,
            "isOwner": isOwner
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid  update failed",
            "updated": False,
            "allcomments": allComments,
            "isListingInWatchList": isListingInWatchList,
            "isOwner": isOwner
        })

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message =request.POST["newcomment"]
    newComment = Comment(
        author= currentUser,
        listing = listingData,
        message = message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))    

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingwatchlist.all()
    return render(request, 'auctions/watchlist.html', {
        "listings": listings
    })

def removefromwatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addtowatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : activeListings,
        "categories": allCategories
    })

def displayCategory(request):
    categoryFromForm = request.POST["category"]
    category = Category.objects.get(categoryName=categoryFromForm)
    activeListings = Listing.objects.filter(isActive=True, category=category)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : activeListings,
        "categories": allCategories
    })

def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, 'auctions/create.html', {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        currentUser = request.user
        categoryData = Category.objects.filter(categoryName=category).first()
        bid = Bid(bid=int(price), user=currentUser)
        bid.save()
        newListing = Listing(
            title = title,
            description = description,
            imageUrl = imageurl,
            price = bid,
            category = categoryData,
            owner = currentUser,
        )
        newListing.save()
        return HttpResponseRedirect(reverse("index"))

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
