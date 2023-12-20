from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home.views import HandleFileUpload, HandleFileDownload

urlpatterns = [
    path('handle/',HandleFileUpload.as_view(), name='handle_file_upload'),
    path('download/<uuid:uid>/', HandleFileDownload.as_view(), name='handle_file_download'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)