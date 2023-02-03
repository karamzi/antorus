from main.models import RequestLogsModel
import json


class LogRequest:

    @staticmethod
    def log_request(request, message=None):
        print('----------------------------REQUSET-------------------------')
        print(request.body)
        print('----------------------------REQUSET-------------------------')
        RequestLogsModel.objects.create(
            url=request.path,
            request_get_data=json.dumps(request.GET),
            request_post_data=json.dumps(request.POST),
            message=message
        )

    @staticmethod
    def log_post(obj, path, message=None):
        RequestLogsModel.objects.create(
            url=path,
            request_get_data='',
            request_post_data=json.dumps(obj),
            message=message
        )