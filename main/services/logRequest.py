from main.models import RequestLogsModel
import json


class LogRequest:

    @staticmethod
    def log_request(request, body=None):
        RequestLogsModel.objects.create(
            url=request.path,
            request_get_data=json.dumps(request.GET, ensure_ascii=False),
            request_post_data=json.dumps(request.POST, ensure_ascii=False),
            message=json.dumps(body, ensure_ascii=False)
        )

    @staticmethod
    def log_post(obj, path, message=None):
        RequestLogsModel.objects.create(
            url=path,
            request_get_data='',
            request_post_data=json.dumps(obj),
            message=message
        )