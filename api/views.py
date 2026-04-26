from django.core.files.storage import default_storage
from rest_framework import generics, views, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.tasks import create_csv
from api.throttles import DailyThrottleRate, PerMinuteThrottleRate
from api.models import Postcode
from api.serializers import PostcodeSerializer, BatchSerializer
from drf_spectacular.utils import extend_schema
from celery.result import AsyncResult


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
    throttle_classes = [DailyThrottleRate, PerMinuteThrottleRate]

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
    serializer_class = BatchSerializer
    throttle_classes = [DailyThrottleRate, PerMinuteThrottleRate]

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


class RequestCSV(views.APIView):
    """
    Request a CSV export for a list of UK postcodes.

    Accepts a POST request with a list of postcodes and queues an async
    export task. Returns a task_id to poll for the export status.

    Example request:
    ```json
        {
            "postcodes": ["SW1A 1AA", "EC1A 1BB"]
        }
    ```

    Example response:
    ```json
        {
            "task_id": "f695a1e6-59ac-41ec-8020-30b14e085ef6",
            "status": "submitted"
        }
    ```

    Use the `task_id` to check export status at `/api/csv-status/<task_id>/`.

    Requires authentication: `Authorization: Token <token_key>`
    """
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]
    serializer_class = BatchSerializer
    throttle_classes = [DailyThrottleRate, PerMinuteThrottleRate]

    @extend_schema(request=BatchSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        postcodes = serializer.validated_data['postcodes']

        task = create_csv.delay(postcodes)
        result = {
            "task_id": task.id,
            "status": "submitted"
        }
        return Response(result, status=status.HTTP_200_OK)


class CheckCsvStatus(views.APIView):
    """
    Check the status of a CSV export task.

    Poll this endpoint with the task_id returned from the CSV export request.
    Returns a presigned download URL when the export is complete.

    Example response (complete):
    ```json
        {
            "status": "success",
            "url": "http://localhost:9000/find-postcode-csv-requests/abc-123.csv"
        }
    ```

    Example response (in progress):
    ```json
        {
            "task_id": "f695a1e6-59ac-41ec-8020-30b14e085ef6",
            "status": "PENDING"
        }
    ```

    Requires authentication: `Authorization: Token <token_key>`
    """
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    throttle_classes = [PerMinuteThrottleRate]

    def get(self, request, task_id):
        task = AsyncResult(task_id)

        if task.state == 'SUCCESS':
            filename = f'{task_id}.csv'
            url = default_storage.url(filename)
            return Response({'status': 'success', 'url': url}, status=status.HTTP_200_OK)

        return Response({
            "task_id": task_id,
            "status": task.status,
        })
