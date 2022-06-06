from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Field , FileHoSo, Action, Comment, NopHoSo, StatusHoSo, CauHoiPublic, CauHoi
from authentication.models import User

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

class FieldSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, field):
        request =self.context['request']
        name = field.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)

    class Meta:
        model = Field
        fields = ["id", "title", "image", "created_date", "category"]


class FileSerializer(ModelSerializer):
    class Meta:
        model = FileHoSo
        fields = ["id", "title", "hoso","image", "description", "created_date", "update_date", "field"]

class FileDetailSerializer(ModelSerializer):
    hoso =SerializerMethodField()
    def get_hoso(self, field):
        request =self.context['request']
        name = field.hoso.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)
        
    class Meta:
        model = FileSerializer.Meta.model
        fields =  FileSerializer.Meta.fields

class MyNopDonSerializer(ModelSerializer):
    class Meta:
        model = NopHoSo
        fields = ["id", "fullname", "cmnd","ngaythangnamsinh", "sonha","tonha","huyennha", "tinhnha","sdt", "email", "title", "hoso", "description","category", "field", "hosoduocky", "status"]

    def create(seft, validated_data):
        hoso = NopHoSo.objects.create(**validated_data)
        return hoso


class StatusHoSoSerializer(ModelSerializer):
    hosonop = MyNopDonSerializer()
    class Meta:
        model = StatusHoSo
        fields = ["id", "user", "hosonop", "status", "created_date"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id" , "first_name", "last_name", "username", "password", "email", "phone", "created_at"]
        extra_kwargs = {
            'password' : {'write_only': 'true'}
        }

    def create(self, validated_data):
        user=User(**validated_data)
        user.set_password(user.password)
        user.save()

        return user


class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "type", "created_date"]

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'update_date']


class CauHoiPublicSerializer(ModelSerializer):
    class Meta:
        model = CauHoiPublic
        fields = ['id', 'title','content', 'contentTL']


class CauHoiSerializer(ModelSerializer):
    class Meta:
        model= CauHoi
        fields = ['email','content', 'type']

    def create(seft, validated_data):
        cauhoi = CauHoi.objects.create(**validated_data)
        return cauhoi