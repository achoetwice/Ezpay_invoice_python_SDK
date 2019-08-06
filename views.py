from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .services import *

# Create invoice via ezpay
class CreateB2CInvoice(APIView):
    def post(self, request):
        '''
        data = {
            'ItemCount':str
            'ItemPrice':str
            'MerchantOrderNo':str
            'BuyerName':str
            'BuyerEmail':str
            'ItemName':str
            'ItemUnit':str
            'Card4No':str
        }
        '''
        data = request.data
        response = CREATE_B2C_CREDITCARD_INVOICE(data)
        if not response:
            return Response({'code':'000', 'data':'Fail'})
        response = json.loads(response.content)
        return Response({'code':'000', 'data':response})