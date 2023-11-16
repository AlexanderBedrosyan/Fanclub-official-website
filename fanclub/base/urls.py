from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('initiatives/', views.initiatives, name='initiatives'),
    path('events/', views.events, name='events'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('store/', views.store, name='store'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('view_card/', views.view_card, name='view_card'),
    path('cards/', views.cards, name='cards'),
    path('add_new_card/<int:card_id>/', views.add_new_card, name='add_new_card'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)