"""
URL configuration for finalproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from email.policy import default

from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

# Swagger schema view for the API
schema_view = swagger_get_schema_view(openapi.Info(
    title="Nika Gabeskiria API Schema",
    default_version="1.0.0",
    description="API documentation for the Book API",
), public=True)

urlpatterns = [
    # Schema view URL for the API documentation
    path("api_schema/", get_schema_view(
        title="Nika Gabeskiria API Schema",
        description="API documentation for the Book API"
    ), name="api_schema"),

    # Swagger UI for the API documentation
    path("swagger/", schema_view.with_ui("swagger"), name="swagger"),

    # Admin URL
    path('admin/', admin.site.urls),

    # API routes for the Book app
    path('api/books/', include("books.urls")),  # Updated to point to the book URLs

    # User-related routes (assuming you still have a user-related API)
    path('api/user/', include("user.urls")),
]
