from rest_framework import generics
from rest_framework.exceptions import NotFound

from api.models import Postcode
from api.serializers import PostcodeSerializer

# Create your views here.
class PostcodeViewSet(generics.ListAPIView):
    queryset = Postcode.objects.all()
    serializer_class = PostcodeSerializer


class PostcodeView(generics.RetrieveAPIView):
    http_method_names = ['get']
    serializer_class = PostcodeSerializer

    def get_object(self):
        postcode = self.kwargs['postcode']
        postcode = postcode.upper().replace('+', ' ')

        try:
            return Postcode.objects.get(postcode=postcode)
        except Postcode.DoesNotExist:
            raise NotFound(f'Postcode {postcode} not found')
