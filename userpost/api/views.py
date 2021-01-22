from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from userpost.models import PassportDataModel
from userpost.api.serializers import PassportPostSerializer

@api_view(['POST',])
# @permission_classes((IsAuthenticated,))
def api_post_img_view(request):

    account = request.user

    user_post = PassportDataModel()

    if request.method == "POST":
        serializer = PassportPostSerializer(user_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            x = serializer.data

            # print(x['pass_img'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
