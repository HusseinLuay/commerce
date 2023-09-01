from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create" , views.create_Listing , name="create_Listing"),
    path("specific_category" , views.specific_category , name="specific_category"),
    path("showitem/<int:id>" , views.show_item , name="showitem"),
    path('watchlist' , views.watchlist , name="watchlist"),
    path('removewatchlist/<int:id>' , views.removewatchlist , name="removewatchlist"),
    path('addwatchlist/<int:id>' , views.addwatchlist , name="addwatchlist"),
    path('addbid/<int:id>' , views.add_bid , name="add_bid") , 
    path('close_Auction/<int:id>' , views.close_Auction , name="close_Auction") ,
    path('coomment/<int:id>' , views.comment , name="comment")
]
