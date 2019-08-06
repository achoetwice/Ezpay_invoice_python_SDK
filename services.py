from decimal import Decimal, ROUND_HALF_UP
import time, os, json
from .gateway_service import *
import requests

INVOICE_URL = os.getenv('INVOICE_URL')
INVOICE_MERCHANT_ID = os.getenv('INVOICE_MERCHANT_ID')
INVOICE_KEY = os.getenv('INVOICE_KEY')
INVOICE_IV = os.getenv('INVOICE_IV')

def CREATE_B2C_CREDITCARD_INVOICE(data):
    '''
    Accept invoice data
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

    # Get all required parameters
    try:
        MerchantOrderNo = data['MerchantOrderNo']
        Card4No = '信用卡末四碼: ' + data['Card4No']
        BuyerEmail = data['BuyerEmail']
        BuyerName = data['BuyerName']
        ItemUnit = data['ItemUnit']
        ItemName = data['ItemName']
        item_count = data['ItemCount']
        item_price = data['ItemPrice']
    except:
        return 'Lack of data'
    
    # Calculate all items and prices with TWD(int)
    origin_item_amt = int(item_count * item_price)
    tax_amt_raw = origin_item_amt*0.05
    tax_amt = int(Decimal(f'{tax_amt_raw}').quantize(Decimal('1.'), rounding=ROUND_HALF_UP))
    amt = origin_item_amt - tax_amt
    total_amt = amt + tax_amt
    
    # Pack up parameters
    order_params={
        'RespondType': 'JSON',
        'Version': '1.4',
        'TimeStamp': f'{int(time.time())}',
        'MerchantOrderNo': MerchantOrderNo,
        'Status': '1', # 1=即時開立
        # 'CreateStatusTime' 預設開立日期
        'Category': 'B2C',  # B2B or B2C
        'BuyerName': BuyerName,  # Customer name
        # 'BuyerAddress': data['customer_address']
        'BuyerEmail': BuyerEmail,  # Customer email
        'PrintFlag': 'Y', # Y=索取發票
        'ItemName': ItemName, # 單項：商品一  多項：商品一｜商品二｜...
        'ItemCount': item_count, # 商品數量，多項模式同itemname
        'ItemUnit': ItemUnit, #商品單位
        'ItemPrice': item_price, #商品單價
        'ItemAmt': origin_item_amt,#數量*單價
        'TaxType':'1', # 1=應稅
        'TaxRate':5, # 5為一般稅率
        'Amt': int(amt),# 銷售金額
        'TaxAmt': int(tax_amt), # 銷售金額的5%
        'TotalAmt': int(total_amt), # Amt + TaxAmt
        'Comment': Card4No#信用卡末四碼：1234
    }

    # AES encode
    key = INVOICE_KEY
    iv = INVOICE_IV
    AES_info_str = NEWEBPAY_AES(order_params, key, iv)

    # Call invoice api
    url = INVOICE_URL
    post_data = {
        'MerchantID_': INVOICE_MERCHANT_ID,
        'PostData_': AES_info_str
    }
    try:
        response = requests.post(url=url, data=post_data)
    except:
        response = None
    return response
