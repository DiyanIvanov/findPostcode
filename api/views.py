from rest_framework import generics, views, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api import serializers
from api.models import Postcode
from api.serializers import PostcodeSerializer, BatchSerializer
from drf_spectacular.utils import extend_schema


class PostcodeView(generics.RetrieveAPIView):
    """
    Retrieve details for a single UK postcode.

    Returns the following geographic data:
    - Area and district information
    - Latitude and longitude coordinates
    - Eastings and northings (British National Grid)

    Example: `/api/postcode/SW1A1AA/`

    Requires authentication: `Authorization: Token <token_key>`
    """
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
    """
    Retrieve details for multiple UK postcodes in a single request.

    Accepts a POST request with a list of postcodes and returns geographic
    data for each one. Invalid or unknown postcodes are returned with an
    error message rather than failing the entire request.

    Example request:
    ```json
    {
        "postcodes": ["SW1A 1AA", "EC1A 1BB"]
    }
    ```

    Requires authentication: `Authorization: Token <token_key>`
    """
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    @extend_schema(request=BatchSerializer)
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
