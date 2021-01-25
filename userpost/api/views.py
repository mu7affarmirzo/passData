from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.conf import settings


from userpost.models import PassportDataModel
from userpost.api.serializers import PassportPostSerializer
from media_cdn.static.detectall.detect import callMy


@api_view(['POST',])
# @permission_classes((IsAuthenticated,))
def api_post_img_view(request):

    account = request.user

    user_post = PassportDataModel()

    if request.method == "POST":
        serializer = PassportPostSerializer(user_post, data=request.data)
        # user_post.location_f()
        if serializer.is_valid():
            serializer.save()
            x = serializer.data
            myData = callMy()
            y = {
                "id": 18,
                "pass_img": "/media/passportsrc/0293c7f2fe0e4c66a87ba56fbb9f7c1b.jpg",
                "text": "there are some text babe"
            }
            print(x['pass_img'])
            user_post.delete()

            return Response(myData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
