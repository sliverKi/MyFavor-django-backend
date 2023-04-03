from django.shortcuts import render
from tokenize import generate_tokens
from django.conf import settings
from django.db import transaction
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import User, Report
from .serializers import (
    TinyUserSerializers,
    PrivateUserSerializer,
    ReportDetailSerializer,
    UserSerializer,
    PickSerializer,
)
from media.serializers import UserProfileSerializer
from idols.models import Idol

class NewUsers(APIView):
    def get(self, request):
        return Response({"email, password, nickname, age, pick 을 입력해주세요."})

    def post(self, request):

        password = request.data.get("password")

        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        print(password)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AllUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):  
        all_users = User.objects.all()  
        serializer = UserSerializer(
            all_users,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)

class MyPage(APIView):  
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        serializer = TinyUserSerializers(user)
        return Response(serializer.data)

    
    def put(self, request):
        user = request.user
        serializer = TinyUserSerializers(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = TinyUserSerializers(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


class UserDetail(APIView):  
    permission_classes = [IsAdminUser]  

    
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

   
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = TinyUserSerializers(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = TinyUserSerializers(user)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

  
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)



class EditPassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            if old_password != new_password:
                user.set_password(new_password)
                user.save()
                return Response({"비밀번호가 성공적으로 변경되었습니다."})
            else:
                return Response({"변경 될 비밀번호가 기존 비밀번호와 동일합니다."})
        else:
            raise ParseError("비밀번호를 다시 확인해주세요.")



class EditPick(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request):
        pick = request.user
        serializer = PickSerializer(pick)
        return Response(serializer.data)


    def put(self, request):
        pick = request.user

        serializer = PickSerializer(
            pick,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_pick = serializer.save()
            return Response(PickSerializer(updated_pick).data)



class AllReport(APIView):
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request):

        all_reports = Report.objects.all()
        serializer = ReportDetailSerializer(all_reports, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self,request):

        serializer = ReportDetailSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():

                report = serializer.save(
                    owner=request.user,
                )
                whoes = request.data.get("whoes")
      
                if request.user.pick.pk not in whoes:
                    raise ParseError("참여자는 본인의 아이돌만 선택 가능합니다.")
                if not whoes:
                    raise ParseError("제보할 아이돌을 알려 주세요.")
                if len(set(whoes)) != 1:
                    raise ParseError("한명의 아이돌만 제보가 가능합니다.")
                if not isinstance(whoes, list):
                    if whoes:
                        raise ParseError("who_pk must be a list")
                    else:
                        raise ParseError(
                            "whoes report? Who should be required. not null"
                        )
                try:
                    idol = Idol.objects.get(pk=whoes[0])
                    report.whoes.add(idol)

                except Idol.DoesNotExist:
                    raise ParseError("선택하신 아이돌이 없어요.")

                serializer = ReportDetailSerializer(
                    report,
                    context={"request": request},
                )
                return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ReportDetail(APIView):
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        report = self.get_object(pk)
        serializer = ReportDetailSerializer(report)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):

        if not request.user.is_admin:
            raise PermissionDenied("권한 없음")
        else:
            report = self.get_object(pk)
            serializer = ReportDetailSerializer(
                report,
                data=request.data,
                partial=True,
            )
        if serializer.is_valid():
            updated_report = serializer.save()
            return Response(
                ReportDetailSerializer(updated_report).data, status=HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reports = self.get_object(pk)

        if not request.user.is_admin:
            raise PermissionDenied

        reports.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class Login(APIView):  
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound
        
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하였습니다.")
        
        if user.check_password(password):
            login(request, user)
            serializer = TinyUserSerializers(user)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)



class Logout(APIView):  
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "See You Again~"}, status=HTTP_200_OK)

class UserPhotos(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)    
        except User.DoesNotExist:
            raise NotFound
    
    def post(self, request, pk):
        idol =self.get_object(pk)
        serializer=UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            photo=serializer.save(idol=idol)
            serializer=UserProfileSerializer(photo)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
