# python_web_sample_kit
Python Web Sample Kit
# <h3>How To Generate Access token and API Secret :</h3>
You can find your Merchant Id in Paykun Dashboard.

You can generate Or Regenerate Access token and API Secret from login into your paykun admin panel, Then Go To : Settings -> Security -> API Keys. There you will find the generate button if you have not generated api key before.

If you have generated api key before then you will see the date of the api key generate, since you will not be able to retrieve the old api key (For security reasons) we have provided the re-generate option, so you can re-generate api key in case you have lost the old one.

Note : Once you re-generate api key your old api key will stop working immediately. So be cautious while using this option.

# <h3>Prerequisite</h3>
    Merchant Id (Please read 'How To Generate Access token and API Secret :')
    Access Token (Please read 'How To Generate Access token and API Secret :')
    Encryption Key (Please read 'How To Generate Access token and API Secret :')
    Python 3.6.0, Django 1.10

# <h3>Set all the required credentials</h3>
    1. From the extracted zip open the file 'paykunCheckout/views.py'
    2. In views.py file find the method with the name 'payNow'
    3. In 'payNow' replace all the dummy detail with real one provided from Paykun
    4. Detail like order, customer, shipping, billing should be set by your own.
    
# <h3>How to run app</h3>
    1. Extract downloaded zip
    2. From command line navigate to the mysite directory in extracted directory
    3. Fire command 'python manage.py runserver
    4. Now open the given URL in Browser e.g 'http://127.0.0.1:8000/' and at the end of the url add 'payNow/'
    5. Now click on Paynow button and you would see Paykun checkout page
  
#<h3> In case of any query, please contact to support@paykun.com.</h3>