from django.urls import path

from .views import home_view, about_view, contact_view, category_view, blog_detail_view, tags_view, search_view

urlpatterns = [
    path('', home_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('category/', category_view),
    path('blog/<int:pk>/', blog_detail_view),
    path('tags/<int:pk>/', tags_view),
    path('search/', search_view)
]
