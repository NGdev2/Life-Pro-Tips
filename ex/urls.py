from django.urls import path, include, re_path
from . import views
from .views import HomePageView, LoginView, RegistrationView, LogoutView
import debug_toolbar

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('__debug__/', include(debug_toolbar.urls)),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('registration', RegistrationView.as_view(), name="registration"),
    path('upvote/<int:tip_id>/', views.upvote_tip, name='upvote_tip'),
    path('downvote/<int:tip_id>/', views.downvote_tip, name='downvote_tip'),
    path('delete/<int:tip_id>/', views.delete_tip, name='delete_tip'),
    re_path(r'^.*$', views.redirect_to_home),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)