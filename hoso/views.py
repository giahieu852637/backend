from .models import Category, Field, FileHoSo, Comment, NopHoSo, StatusHoSo, CauHoiPublic, CauHoi
from authentication.models import User
from .serializers import CategorySerializer, FieldSerializer, FileSerializer, FileDetailSerializer, UserSerializer, ActionSerializer, CommentSerializer, MyNopDonSerializer, StatusHoSoSerializer, StatusHoSoSerializer, CauHoiPublicSerializer, CauHoiSerializer
from .paginator import BasePaginator

from django.http import Http404
from django.conf import settings
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from .utils import Util
from django.core.files import File

import signpdf

class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class  = CategorySerializer


class FieldViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = FieldSerializer


    def get_queryset(self):
        fields = Field.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            fields = fields.filter(title__icontains=q)
        
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            fields = fields.filter(category_id=cate_id)
        return fields

    @action(methods=['get'], detail=True, url_path="files")
    def get_files(self, request, pk):
        files = Field.objects.get(pk=pk).files.filter(active=True)

        kw = request.query_params.get('kw')
        if kw is not None:
            files = files.filter(title__icontains=kw)

        return Response(FileSerializer(files, many=True).data, status=status.HTTP_200_OK)

class FileHoSoViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.RetrieveAPIView):
    queryset = FileHoSo.objects.filter(active=True)
    serializer_class  = FileDetailSerializer

    def get_queryset(self):
        hosos = FileHoSo.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            hosos = hosos.filter(title__icontains=q)
        
        field_id = self.request.query_params.get('field_id')
        if field_id is not None:
            hosos = hosos.filter(field_id=field_id)
        return hosos

    
 



class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class  = UserSerializer

    def get_permissions(self):
        if self.action in ['add_comment', 'take_action', 'get_current_user']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path="checkfile")
    def take_action(self, request, pk):
        content = request.data.get('content')
        try:
            action_type = int(request.data['type'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = Action.objects.create(type=action_type, creator= request.user, card=self.get_object())

            return Response(ActionSerializer(action).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
           c = Comment.objects.create(content=content, card=self.get_object(), creator= request.user)
           return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)




class NopHoSoViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = NopHoSo.objects.all()
    serializer_class  = MyNopDonSerializer
    pagination_class = BasePaginator
    permission_class  = [permissions.IsAuthenticated()]

    def get_permissions(self):
        if self.action in ['nop_hoso', 'ky_file', 'view_hoso']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

   

    @action(methods=['post'], detail=False, url_path="nop_hoso")
    def nop_hoso(self, request):
        serializer = MyNopDonSerializer(data=request.data)
        if serializer.is_valid():
            c = serializer.save(user=request.user)
            StatusHoSo.objects.create(user=request.user, hosonop=c)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path="ky")
    def ky_file(self, request, pk):
        files = NopHoSo.objects.get(pk=pk)
        temp = signpdf.sign_file(files.hoso.path, "000001", 100, 210, ('1'))
        files.hosoduocky = temp
        django_file = File(files.hosoduocky)
        print(django_file)
        files.hosoduocky.save('new', django_file)

        absurl = 'https://backend.justfreshmen.team/static/'+str(files.hosoduocky)

        email_body = 'Hi '+files.fullname + \
            'File bạn đã được ký. Dowload tại đây\n' + absurl
        data = {'email_body': email_body, 'to_email': files.email,
                'email_subject': 'File bạn đã được ký'}

        Util.send_email(data)


        return Response(MyNopDonSerializer(files).data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path="view")
    def view_hoso(self, request, pk):
        files = NopHoSo.objects.get(pk=pk)

        return Response(MyNopDonSerializer(files).data, status=status.HTTP_200_OK)

    


class StatusHoSoViewSet(viewsets.ViewSet):
    queryset = StatusHoSo.objects.all()
    serializer_class  = StatusHoSoSerializer

    def get_permissions(self):
        if self.action in ['getstatus_user']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='getstatus')
    def getstatus_user(self, request, format=None):
        statuss = StatusHoSo.objects.filter(user=request.user)
        serializer = StatusHoSoSerializer(statuss, many=True)
        return Response(serializer.data)


class CauHoiThuongGapViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CauHoiPublicSerializer
    def get_queryset(self):
        cauhoipublic = CauHoiPublic.objects.all()

        q = self.request.query_params.get('q')
        if q is not None:
            cauhoipublic = cauhoipublic.filter(title__icontains=q)
        return cauhoipublic


class CauHoiViewSet(viewsets.ViewSet):
    queryset = CauHoi.objects.all()
    serializer_class  = CauHoiSerializer

    def get_permissions(self):
        if self.action in ['add_question', 'views']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path="add_question")
    def add_question(self, request):
        serializer = CauHoiSerializer(data=request.data)
        if serializer.is_valid():
            c = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False, url_path='views')
    def views(self, request, format=None):
        cauhois = CauHoi.objects.filter(user=request.user)
        serializer = CauHoiSerializer(cauhois, many=True)
        return Response(serializer.data)