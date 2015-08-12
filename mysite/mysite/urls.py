from django.conf.urls import include, url
from django.contrib import admin

#'root' project folder, need to point the root urlconfig to the project module 

urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
]