from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('process_register', views.process_register, name='process_register'),
    path('process_login', views.process_login, name='process_login'),
    path('quotes', views.quotes, name='quotes'),
    path('myaccount/<int:acct_id>', views.myaccount, name='myaccount'),
    path('process_edit_account', views.process_edit_account, name='process_edit_account'),
    path('process_quote_new', views.process_quote_new, name='process_quote_new'),
    path('process_quote_like/<int:quote_id>', views.process_quote_like, name='process_quote_like'),

    path('user/<int:user_id>', views.user, name='user'),

    path('quote/delete/<int:quote_id>', views.quote_delete, name='quote_delete'),



    path('logout', views.logout, name='logout'),
]