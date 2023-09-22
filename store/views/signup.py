import imp
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer, Otp, Sendmail
from django.views import View
import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

def send_email_to_user(username=None, otp=None, email=None):
    subject = 'Welcome to our E-Commerce Store'
    message = '''<h4>Hello {0}</h4>, 
                    <p>Greetings and welcome to our E-Commerce Store.
                    For sign up, you need to use OTP is {1}.
                    We are delighted to onboard you</p>'''.format(username.capitalize(),int(otp))
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(email_from, recipient_list)
    send_mail(subject, message, email_from, recipient_list, fail_silently=True)
    Sendmail.objects.create(send_to=email, subject=subject, message=message).save()

class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        confirm_password = postData.get ('confirmpassword')
        otp = postData.get ('otp')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': password
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if password != confirm_password:
            error_message = 'Password is not matching, please re-enter'

        if not error_message:
            print (first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            if not otp:
                new_otp = random.randrange(1000, 9999)
                try:
                    print(first_name, new_otp, email)
                    send_email_to_user(first_name, new_otp, email)
                except:
                    data = {
                        'error': 'Fail to send OTP to the registered email address',
                        'values': value
                    }
                    return render (request, 'signup.html', data)
                Otp.objects.create(email=email, otp=new_otp).save()
                data = {
                    'otp': True,
                    'error': 'OTP is sent to your registered email address, please enter otp',
                    'values': value
                }
                return render (request, 'signup.html', data)
            else:
                try:
                    otp_obj = Otp.objects.get(email=email)
                except:
                    pass
                if int(otp_obj.otp) != int(otp):
                    data = {
                        'otp': True,
                        'error': 'Please enter correct OTP',
                        'values': value
                    }
                    return render (request, 'signup.html', data)
                customer.register ()
                print (first_name, last_name, phone, email, password)
                return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
