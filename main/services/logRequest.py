from main.models import RequestLogsModel
import json


class LogRequest:

    @staticmethod
    def log(request, message=None):
        RequestLogsModel.objects.create(
            url=request.path,
            request_get_data=json.dumps(request.GET),
            request_post_data=json.dumps(request.POST),
            message=message
        )
