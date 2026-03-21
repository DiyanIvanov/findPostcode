from rest_framework import generics, views, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.models import Postcode
from api.serializers import PostcodeSerializer, BatchSerializer


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


class PostcodeBatchView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = BatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        postcodes = serializer.validated_data['postcodes']

        results = []

        for postcode in postcodes:
            # replace with your actual lookup logic
            obj = Postcode.objects.filter(postcode=postcode).first()

            if obj:
                results.append(PostcodeSerializer(obj).data)
            else:
                results.append({
                    "postcode": postcode,
                    "error": "Not found"
                })

        return Response(results, status=status.HTTP_200_OK)

