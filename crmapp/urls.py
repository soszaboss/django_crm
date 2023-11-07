from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    # path("login/", views.login_user, "login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("delete/<int:pk>", views.delete_user, name="delete"),
    path("update/<int:pk>", views.update, name="update"),
    path("new record/", views.new_record, name="add_record"),
    path("record/<int:pk>", views.record, name="record")

]