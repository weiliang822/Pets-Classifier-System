from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Model, Photo
from rest_framework import viewsets, status
from django.http import HttpResponse
from django.http import Http404
from rest_framework.response import Response
from admini.serializer import UsersSerializer, ModelsSerializer, PhotosSerializer
from rest_framework.decorators import action
import os
from rest_framework.decorators import api_view
import zipfile


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    @action(detail=True, methods=['POST'], url_path='custom-update')
    def custom_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotosSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 删除本地照片文件
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)

        instance.model.photoCount -= 1
        instance.model.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModelsViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelsSerializer

    def create(self, request, *args, **kwargs):
        zipPath = request.data.get('photos')  # 提取照片列表
        model = Model(name=request.POST.get('name'), photoCount=0)
        model.save()
        savePath = model.name+'/'
        photoList = unzip(zipPath=zipPath, savePath=savePath, model=model)

        model.photoCount = len(photoList)
        model.save()

        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 获取图片列表
        photos = request.data.getlist('photos')

        instance.photoCount += len(photos)
        self.perform_update(serializer)
        # 创建并关联 Photo 模型实例
        for photo in photos:
            photoModel = Photo(path=(instance.name+'/'), model=instance)
            photoModel.image = photo
            photoModel.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 删除关联的照片对象及对应的文件
        for photo in instance.photos.all():
            # 获取照片文件的路径
            photo_path = photo.image.path

            # 删除照片文件
            if os.path.exists(photo_path):
                os.remove(photo_path)

            # 删除照片对象
            photo.delete()

        os.rmdir('media/'+instance.name)

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['POST'])
def uploadModel(request):
    # 获取上传的文件
    settingsFile = request.FILES.get('settingsFile')
    modelFile = request.FILES.get('modelFile')

    # 指定目标目录
    targetDirectory = 'static/model'

    # 检查目标目录中的文件是否存在
    settingsFilePath = os.path.join(targetDirectory, 'settings.py')
    modelFilePath = os.path.join(targetDirectory, 'model.h5')

    # 保存上传的文件到目标目录
    with open(settingsFilePath, 'wb') as destination:
        for chunk in settingsFile.chunks():
            destination.write(chunk)

    with open(modelFilePath, 'wb') as destination:
        for chunk in modelFile.chunks():
            destination.write(chunk)

    return Response('文件上传成功。')


@api_view(['GET'])
def downloadModel(request):
    # 指定目标目录
    targetDirectory = 'static/model'

    # 检查文件是否存在
    settingsFilePath = os.path.join(targetDirectory, 'settings.py')

    if not os.path.exists(settingsFilePath):
        raise Http404("文件不存在。")

    # 读取文件内容
    with open(settingsFilePath, 'rb') as settingsFile:
        settingsContent = settingsFile.read()

    # 构建响应
    response = Response(content_type='application/octet-stream')

    # 设置文件名
    response['settingsFile'] = 'attachment; filename="settings.py"'
    response.content = settingsContent

    return response


def unzip(zipPath, savePath, model):
    unzipPath = 'media/'+savePath
    file = zipfile.ZipFile(zipPath)
    file.extractall(unzipPath)
    file.close()
    photoList = []
    for root, dirs, files in os.walk(unzipPath):
        for file in files:
            photo = Photo(path=savePath, model=model)
            photo.image = savePath+file
            photo.save()
            photoList.append(photo)

    return photoList


@api_view(['POST'])
def downloadPhotos(request):
    ids = request.data.get('ids')
    ids = ids.split(',')
    zipPath = 'media/temp/photos.zip'
    with zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED) as zipFile:
        for id in ids:
            model = Model.objects.filter(id=int(id)).first()
            photos = model.photos.all()

            modelDirectory = os.path.join(model.name, '')
            print(modelDirectory)
            for photo in photos:
                zipFile.write(photo.image.path, os.path.join(
                    modelDirectory, photo.image.name))

    zipFile.close()

    with open(zipPath, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=photos.zip'

    # 删除临时文件
    os.remove(zipPath)

    return response
