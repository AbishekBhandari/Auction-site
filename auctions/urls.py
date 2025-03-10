from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('create/', views.createListing, name="create"),
    path('displayCategory/', views.displayCategory, name="displayCategory"),
    path('listing/<int:id>', views.listing, name="listing"),
    path('removefromwatchlist/<int:id>', views.removefromwatchlist, name="removefromwatchlist"),
    path('addtowatchlist/<int:id>', views.addtowatchlist, name="addtowatchlist"),
    path('watchlist/', views.watchlist, name="watchlist"),
    path('addcomment/<int:id>', views.addComment, name="addcomment"),
    path('addBid/<int:id>', views.addBid, name="addBid"),
    path('closeAuction/<int:id>', views.closeAuction, name="closeAuction"),
]

