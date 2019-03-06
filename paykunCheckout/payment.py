import Crypto
import os
import collections, string

from .crypto import AESCipher

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class Payment(object):

    gateway_url = "https://checkout.paykun.com/payment"
    gateway_url_dev = "https://sandbox.paykun.com/payment"
    page_title = "Processing Payment..."
    merchantId = None
    accessToken = None
    encryptionKey = None
    orderId = None
    purpose = None
    amount = None
    successUrl = None
    failureUrl = None
    country = None
    state = None
    city = None
    pinCode = None
    addressString = None
    billingCountry = None
    billingState = None
    billingCity = None
    billingPinCode = None
    billingAddressString = None
    twig = None
    isLive = None
    isPassedValidationForConstructor = False
    isPassedValidationForInitOrder = False
    isPassedValidationForCustomer = False
    isPassedValidationForShipping = False
    isPassedValidationForBilling = False
    isCustomRenderer = False
    udf_1 = False
    udf_2 = False
    udf_3 = False
    udf_4 = False
    udf_5 = False

    def __init__(self, mid, accessToken, encKey, isLive=True, isCustomTemplate=False):
        self.merchantId = mid
        self.accessToken = accessToken
        self.encryptionKey = bytes(encKey, 'utf8')
        self.isLive = isLive
        self.isPassedValidationForConstructor = True
        self.isCustomRenderer = isCustomTemplate


    def initOrder(self, orderId, purpose, amount, successUrl, failureUrl):
        self.orderId = orderId
        self.purpose = purpose
        self.amount = amount
        self.successUrl = successUrl
        self.failureUrl = failureUrl
        self.isPassedValidationForInitOrder = True


    def addCustomer(self, customerName, customerEmail, customerMoNo):
        self.customerName = customerName
        self.customerEmail = customerEmail
        self.customerMoNo = customerMoNo
        self.isPassedValidationForCustomer = True


    def addShippingAddress(self, country, state, city, pinCode, addressString):
        self.country = country
        self.state = state
        self.city = city
        self.pinCode = pinCode
        self.addressString = addressString
        self.isPassedValidationForShipping = True


    def addBillingAddress(self, country, state, city, pinCode, addressString):
        self.billingCountry = country
        self.billingState = state
        self.billingCity = city
        self.billingPinCode = pinCode
        self.billingAddressString = addressString
        self.isPassedValidationForBilling = True


    def submit(self):
        dataArray = {}
        dataArray["order_no"] = self.orderId
        dataArray["product_name"] = self.purpose
        dataArray["amount"] = self.amount
        dataArray["success_url"] = self.successUrl
        dataArray["failure_url"] = self.failureUrl
        dataArray["customer_name"] = self.customerName
        dataArray["customer_email"] = self.customerEmail
        dataArray["customer_phone"] = self.customerMoNo
        dataArray["shipping_address"] = self.addressString
        dataArray["shipping_city"] = self.city
        dataArray["shipping_state"] = self.state
        dataArray["shipping_country"] = self.country
        dataArray["shipping_zip"] = self.pinCode
        dataArray["billing_address"] = self.billingAddressString
        dataArray["billing_city"] = self.billingCity
        dataArray["billing_state"] = self.billingState
        dataArray["billing_country"] = self.billingCountry
        dataArray["billing_zip"] = self.billingPinCode
        dataArray["udf_1"] = self.udf_1 if self.udf_1 else ""
        dataArray["udf_2"] = self.udf_2 if self.udf_2 else ""
        dataArray["udf_3"] = self.udf_3 if self.udf_3 else ""
        dataArray["udf_4"] = self.udf_4 if self.udf_4 else ""
        dataArray["udf_5"] = self.udf_5 if self.udf_5 else ""
        encryptedData = self.encryptData(dataArray)
        return self.createForm(encryptedData)


    def encryptData(self, data):
        # data = list(filter(lambda d: d['type'] in keyValList, data))
        data = collections.OrderedDict(sorted(data.items()))
        # ksort(data);
        dataToPostToPG = []
        TEST = ""
        for key, value in data.items():
            if value is None and not string.strip(value):
                # JGJHG
                TEST = "123"
            else:
                dataToPostToPG.append(key + "::" + str(value))
        
        #print(";".join(dataToPostToPG))
        dataToPostToPG = ";".join(dataToPostToPG)
        # Encrypting String
        return AESCipher().encrypt(dataToPostToPG, self.encryptionKey)


    def createForm(self, encData):
        formData = {}
        formData["encrypted_request"] = encData
        formData["merchant_id"] = self.merchantId
        formData["access_token"] = self.accessToken
        if self.isLive:
            formData["gateway_url"] = self.gateway_url
        else:
            formData["gateway_url"] = self.gateway_url_dev
        formData["pageTitle"] = self.page_title
        return self.prepareCustomFormTemplate(formData)


    def prepareCustomFormTemplate(self, formData):
        #print(formData['merchant_id'])
        htmlEntity = """
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html lang="en">
                <head>
                    <title>{param4}</title>
                    <meta http-equiv="content-type" content="text/html;charset=utf-8">
                </head>
                <body>
                <div>
                    Processing your payment, please wait...
                </div>
                <form  action="{param5}" method="post" name="server_request" target="_top" >
                    <table width="80%" align="center" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                            <td><input type="hidden" name="encrypted_request" id="encrypted_request" value="{param1}" /></td>
                        </tr>
                        <tr>
                            <td><input type="hidden" name="merchant_id" id="merchant_id" value="{param2}" /></td>
                        </tr>
                        <tr>
                            <td><input type="hidden" name="access_token" id="access_token" value="{param3}"></td>
                        </tr>
                    </table>
                </form>
                </body>
                <script type="text/javascript">
                    document.server_request.submit();
                </script>
                </html>
            """.format(param1=formData['encrypted_request'].decode("utf-8"), param2=formData['merchant_id'], param3=formData['access_token'], param5=formData['gateway_url'], param4='Payment')
        return htmlEntity