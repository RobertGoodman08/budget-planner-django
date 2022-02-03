from users.views import register, user_login, user_logout
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', register,  name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),

]