# Author: harry.cai
# DATE: 2018/11/6
from django.utils.deprecation import MiddlewareMixin


class CORSMiddleWare(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        if request.method == "options":
            response['Access-Control-Allow-Headers'] = "Content-Type"
            response['Access-Control-Allow-Methods'] = "PUT,DELETE"
        return  response