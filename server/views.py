import uuid
import os
import pandas as pd
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from celery.result import AsyncResult

from server.serializers import UploadSerializer
from server.validators import validate_file
from server.tasks import fill_sales_data
from server.models import ErrorLog


class FileInputView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (FormParser, MultiPartParser,)

    @swagger_auto_schema(
        request_body=UploadSerializer,
        responses={200: 'OK'}
    )
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('sales_data')
        identifier = uuid.uuid4()
        with open(os.path.join('sales_data', f'{identifier}.xlsx'), 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        errors = validate_file(file_obj)
        if errors:
            ErrorLog.objects.create(
                uuid=identifier,
                error='\n'.join(errors)
            )
            return JsonResponse({"errors": errors}, status=404)
        task = fill_sales_data.delay(identifier)
        return JsonResponse({"task_id": task.task_id}, status=202)


class StatusCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id, *args, **kwargs):
        celery_task = AsyncResult(id=task_id, app=fill_sales_data)
        return JsonResponse({"status": celery_task.state})


class ResultView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id, *args, **kwargs):
        celery_task = AsyncResult(id=task_id, app=fill_sales_data)
        sales_dict = celery_task.get()
        identifier = list(sales_dict.keys())[0]
        df = pd.DataFrame(sales_dict[identifier])
        df.to_excel(os.path.join('sales_data', f'{identifier}_filled.xlsx'), index=False)
        with open(os.path.join('sales_data', f'{identifier}_filled.xlsx'), 'rb') as f:
            response = HttpResponse(
                f.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={identifier}.xlsx'
            return response
