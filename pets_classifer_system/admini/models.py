from django.db import models
import os


def getDynamicUploadPath(instance, filename):
    # 获取当前实例的path属性值
    uploadPath = instance.path

    # 生成动态的上传路径
    dynamicPath = os.path.join(uploadPath, filename)

    return dynamicPath


class Model(models.Model):
    name = models.CharField(max_length=100)  # 模型名称
    photoCount = models.IntegerField()       # 图片数

    def __str__(self):
        return self.name


class Photo(models.Model):
    model = models.ForeignKey(
        Model, on_delete=models.CASCADE, related_name='photos', null=True)  # 添加的外键字段
    path = models.CharField(max_length=100, default='')  # 图片路径
    image = models.ImageField(upload_to=getDynamicUploadPath)  # 图片字段，上传位置动态获取

    def __str__(self):
        return self.image.name
