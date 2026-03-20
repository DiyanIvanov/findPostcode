from rest_framework import generics

from api.models import Postcode
from api.serializers import PostcodeSerializer

# Create your views here.
class PostcodeViewSet(generics.ListAPIView):
    queryset = Postcode.objects.all()
    serializer_class = PostcodeSerializer


class PostcodeView(generics.RetrieveAPIView):
    
    queryset = Postcode.objects.all()
