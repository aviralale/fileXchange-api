from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileListSerializer
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Folder
from django.core.files import File
import os
import zipfile
from django.conf import settings

class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request):
        try:
            data = request.data
            serializer = FileListSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'File is ready to share.',
                    'data' : serializer.data
                })
            return Response({
                'status': 'error',
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print("Error in file upload view", str(e))

class HandleFileDownload(APIView):
    def get(self, request, uid):
        folder = get_object_or_404(Folder, uid=uid)
        zip_file_path = os.path.join(settings.MEDIA_ROOT, 'zip', f'{uid}.zip')

        if not os.path.exists(zip_file_path):
            folder_files = folder.files_set.all()
            self.zip_files(folder_files, zip_file_path)

        return FileResponse(open(zip_file_path, 'rb'), as_attachment=True)

    def zip_files(self, files, zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for file in files:
                file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
                zip_file.write(file_path, os.path.basename(file_path))