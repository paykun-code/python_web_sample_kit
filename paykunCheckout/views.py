from django.http import HttpResponse
from .crypto import AESCipher
from .payment import Payment
from django.template import Context, Template

def index (request): 
	return HttpResponse(
		"""
		
		<form action="/payNow/1/" method="post" name="server_request" target="_top">
                            <table width="100%" align="center" border="0" cellpadding="4" cellspacing="5">
                                <tbody>
								
                                <tr>
                                    <td><input type="button" name="submit_data" id="submit_data" value="Paynow" onclick="doAction()"></td>
                                </tr>
                            </tbody></table>
                        </form>
		<script>
			function doAction() {
				window.location.href = "http://127.0.0.1:8000/payNow/1/";
			}
		</script>		
		"""
	)

def payNow(request, pay_id):
	
	payment = Payment('<merchantId>', '<accessToken>', '<encryptionKey>', True, True)
	
	payment.initOrder('<orderId>', '<Purpose or ProductName>', "<amount>", '<successUrl.example.com>',  '<failUrl.example.com>')
	
	payment.addCustomer('<customerName>', '<customerEmail>', '<customerContactNo>')
	
	payment.addShippingAddress('<country>', '<state>', '<city>', '<postalCode>', '<fullAddress>')
	
	payment.addBillingAddress('<country>', '<state>', '<city>', '<postalCode>', '<fullAddress>')
	
	formHtml = payment.submit()
	#print(formHtml)
	return HttpResponse(formHtml)
	
		

	
