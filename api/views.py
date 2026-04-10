from rest_framework import generics, views, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import Postcode
from api.serializers import PostcodeSerializer, BatchSerializer


class PostcodeView(generics.RetrieveAPIView):
    http_method_names = ['get']
    serializer_class = PostcodeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        postcode = self.kwargs['postcode']
        postcode = postcode.upper().replace('+', ' ')

        try:
            return Postcode.objects.get(postcode=postcode)
        except Postcode.DoesNotExist:
            raise NotFound(f'Postcode {postcode} not found')


class PostcodeBatchView(views.APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        postcodes = serializer.validated_data['postcodes']

        queryset = Postcode.objects.filter(postcode__in=postcodes)

        results_map = {obj.postcode: obj for obj in queryset}
        result = [
            PostcodeSerializer(results_map[postcode]).data
            if postcode in results_map
            else {"postcode": postcode, "error": "Not found"}
            for postcode in postcodes
        ]


        return Response(result, status=status.HTTP_200_OK)
