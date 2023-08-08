from django.shortcuts import render
import tensorflow as tf
import static.model.settings as settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.


def my_densenet():
    """
    创建并返回一个基于densenet的Model对象
    """
    # 获取densenet网络，使用在imagenet上训练的参数值，移除头部的全连接网络，池化层使用max_pooling
    densenet = tf.keras.applications.DenseNet121(
        include_top=False, weights='imagenet', pooling='max')
    # 冻结预训练的参数，在之后的模型训练中不会改变它们
    densenet.trainable = False
    # 构建模型
    model = tf.keras.Sequential([
        # 输入层，shape为(None,224,224,3)
        tf.keras.layers.Input((224, 224, 3)),
        # 输入到DenseNet121中
        densenet,
        # 将DenseNet121的输出展平，以作为全连接层的输入
        tf.keras.layers.Flatten(),
        # 添加BN层
        tf.keras.layers.BatchNormalization(),
        # 随机失活
        tf.keras.layers.Dropout(0.5),
        # 第一个全连接层，激活函数relu
        tf.keras.layers.Dense(512, activation=tf.nn.relu),
        # BN层
        tf.keras.layers.BatchNormalization(),
        # 随机失活
        tf.keras.layers.Dropout(0.5),
        # 第二个全连接层，激活函数relu
        tf.keras.layers.Dense(64, activation=tf.nn.relu),
        # BN层
        tf.keras.layers.BatchNormalization(),
        # 输出层，为了保证输出结果的稳定，这里就不添加Dropout层了
        tf.keras.layers.Dense(settings.CLASS_NUM, activation=tf.nn.softmax)
    ])

    return model


# 导入模型
model = my_densenet()
# 加载训练好的参数
model.load_weights(settings.MODEL_PATH)


@api_view(['POST'])
def petsClassify(request):
    """
    宠物图片分类接口，上传一张图片，返回此图片上的宠物是那种类别，概率多少
    """
    # 获取用户上传的图片
    img_str = request.FILES.get('file').read()
    # 进行数据预处理
    x = tf.image.decode_image(img_str, channels=3)
    x = tf.image.resize(x, (224, 224))
    x = x / 255.
    x = (x - tf.constant(settings.IMAGE_MEAN)) / \
        tf.constant(settings.IMAGE_STD)
    x = tf.reshape(x, (1, 224, 224, 3))
    # 预测
    y_pred = model(x)
    pet_cls_code = tf.argmax(y_pred, axis=1).numpy()[0]
    pet_cls_prob = float(y_pred.numpy()[0][pet_cls_code])
    pet_cls_prob = '{}%'.format(int(pet_cls_prob * 100))
    pet_class = settings.CODE_CLASS_MAP.get(pet_cls_code)
    # 将预测结果组织成json
    res = {
        'pet_cls': pet_class,
        'probability': pet_cls_prob,
    }
    # 返回json数据
    return Response(res)
