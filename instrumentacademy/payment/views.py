from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import CourseDetail
from django.shortcuts import render, get_object_or_404
from home.views import *
from django.urls import reverse


 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


from decimal import Decimal

@login_required
def homepage(request, course_id):
    # Retrieve the course details including its price based on the course_id
    # Replace this with your actual logic to fetch the course details
   
    try:
        course = CourseDetail.objects.get(id=course_id)
        currency = 'INR'
        amount = float(course.amount)  # Convert the Decimal amount to float

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount*100,
            currency=currency,
            payment_capture='0'
        ))

        # Get the order ID of the newly created order
        razorpay_order_id = razorpay_order['id']
        callback_url = f'/payment/paymenthandler/{course_id}/'
        order = Order.objects.create(
            user=request.user,  # Assuming you have a logged-in user
            razorpay_order_id=razorpay_order_id,
            amount=amount,
            currency=currency,
            payment_status='pending',  # You can set this to 'completed' when payment is successful
              # Assuming you have a Many-to-Many relationship with courses
        )
        order.items.set([course])

        # Create a context dictionary to pass data to the template
        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': callback_url,
            'course': course,
            'order':order
            
        }

        return render(request, 'student_template/payment.html', context=context)

    except CourseDetail.DoesNotExist:
        # Handle the case where the course with the given ID does not exist
        return render(request, 'course_not_found.html')
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request,course_id):
 
    # only accept POST request.
    if request.method == "POST":
        
        course = CourseDetail.objects.get(id=course_id)
        amt=course.amount
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result is not None:
            amount = int(amt*100)  # Rs. 200
            print(amount)
            # capture the payemt
            razorpay_client.payment.capture(payment_id, amount)

            # render success page on successful caputre of payment
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_id=payment_id
            order.payment_status = 'completed'
            order.save()
                # Handle the case where the order doesn't exist
            request.user.enrolled_courses.add(course)

            return redirect('/mylearning/')

            
        else:
            return JsonResponse({'status': 'invalid_signature'})
        
    else:
        return HttpResponseBadRequest()
    



   
from django.shortcuts import render
from .models import Order

@login_required
def learners_enrolled_through_payment(request, course_id):
    course_orders = Order.objects.filter(items__id=course_id)

    # Filter orders with 'completed' payment status (adjust this based on your logic)
    completed_orders = course_orders.filter(payment_status='completed')

    # Get the list of learners who have enrolled through payment for the course
    enrolled_learners = [order.user for order in completed_orders]

    # Pass the enrolled learners and their payment details to the template
    context = {
        'course_id': course_id,
        'enrolled_learners': enrolled_learners,
        'completed_orders': completed_orders,
    }

    return render(request, 'tutor_template/enrolled_course_detail.html', context)
