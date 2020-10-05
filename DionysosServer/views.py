# Shortcuts
from django.shortcuts import get_object_or_404

# Decorators
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from oauth2_provider.decorators import protected_resource

# HTTP responses
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseBadRequest

# Validators and exceptions
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError


# Models
from .models import Table, Restaurant, Section, Category, FoodSection, Food, Order, User, UserProfile, OrderedFood
from oauth2_provider.models import AccessToken
# Authentication
from django.contrib.auth import authenticate, login, logout

# Stripe
import stripe 

# Utilities 
import json

stripe.api_key = 'sk_test_51HGhdZAGNFbVchRHoIFnNKCmNUJuydMkWrdfRmjj6p8z8z1tVKL4vdW2FBj7185uRTc9qj7kLRtQlKk1c07YZa3u00ZoWXSKgv'

def sit_to_table(request, table_id):
    table = get_object_or_404(Table, public_id=table_id)
    restaurant = get_object_or_404(Restaurant, pk=table.restaurant.id)
    restaurant_sections = Section.objects.filter(restaurant=restaurant)
    sections_json = []

    for section in restaurant_sections:
        section_dict = section.to_json()
        section_categories = Category.objects.filter(section=section)
        categories_json = []
        for category in section_categories:
            headers = []
            category_headers = Food.objects.filter(category=category)
            for header in category_headers:
                headers.append(header.to_json())
            food_sections = FoodSection.objects.filter(category=category)
            food_section_array = []
            for food_section in food_sections:
                food_array = []
                foods = Food.objects.filter(foodSection=food_section)
                for food in foods:
                    food_array.append(food.to_json())
                food_sections_json = food_section.to_json()
                food_sections_json["Food"] = food_array
                food_section_array.append(food_sections_json)
            category_json = category.to_json()
            category_json["Headers"] = headers
            category_json["FoodSections"] = food_section_array
            categories_json.append(category_json)

        section_dict["Category"] = categories_json
        sections_json.append(section_dict)
        
    restaurant_json = restaurant.to_json()
    restaurant_json["Sections"] = sections_json
    response = {
        "Table": table.to_json(),
        "Restaurant": restaurant_json
    }
    return JsonResponse(response)

@csrf_exempt
@protected_resource()
@require_http_methods(['POST'])
def create_order(request):
    if request.user.is_authenticated:
        try:
            foods = json.loads(request.POST["foods"])
            table_id = content["table"]
        except (KeyError, Exception):
            return JsonResponse({"message": 'Missing foods'} ,status=400)
        
        order = Order.objects.create(user=request.user, state=Order.OrderState.VALIDEE)
        ordered_foods = []
        amount = 0
        basket = []
        found_foods = []
        try: 
            for basket_food in foods:
                basket.append({"id": basket_food["id"], "quantity": basket_food["quantity"]})
                found_foods.append(get_object_or_404(Food, public_id=basket_food['id']))
            table = get_object_or_404(Table, public_id=table_id)
        except (KeyError, Http404):
            raise HttpResponseBadRequest()

        for basket_food, food in zip(basket, found_foods):
            ordered_food = OrderedFood(food=food, quantity=basket_food['quantity'], paid_price=food.price)
            ordered_food.save()
            ordered_foods.append(ordered_food)
            amount += food.price * basket_food['quantity']
        order.ordered_foods.set(ordered_foods)
        order.table = table
        order.restaurant = table.restaurant

        stripe_response = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency='eur',
            payment_method_types=['card'],
            receipt_email=request.user.username
        )
        order.stripe_id = stripe_response['id']
        order.save()
        return JsonResponse({"client_secret": stripe_response["client_secret"]})
    return HttpResponse(status=401)
    
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = 'whsec_3y0OMasjWixPROyIFAF9kY7yL5aB3LbR'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(['POST'])
def create_account(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['firstName'].strip()
        last_name = request.POST['lastName'].strip()

    except KeyError:
        return JsonResponse({"message": 'Required fields : email, password, password2, firstName, lastName', "error": "missingFields"} ,status=400)
    

    is_restaurateur = request.POST.get('Restaurateur')
    password_validator = RegexValidator("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#_?\-&])[A-Za-z\d@$!%_*#?&\-]{8,}$", message="Le mot de passe est invalide. Il doit contenir au moins 8 caractères dont un caractère spécial, une majuscule, une minuscule et un nombre.")
    try:
        password_validator.__call__(password)
    except ValidationError as e:
        return JsonResponse({"message": e.message, "error": "invalidPassword"}, status=400)

    email_validator = EmailValidator(message="L'email n'est pas valide.")
    try:
        email_validator.__call__(email)
    except ValidationError as e:
        return JsonResponse({"message": e.message, "error": "invalidEmail"}, status=400)
    
    if password != password2:
        return JsonResponse({"message": "Les mots de passe ne correspondent pas.", "error": "passwordsNotMatching"}, status=400)
    try:
        user = User.objects.create_user(email, email, password, first_name=first_name, last_name=last_name)
    except IntegrityError:
        return JsonResponse({"message": "L'email existe déjà dans la base de données.","error": "duplicatedEmail"}, status=400)
    
    name = f"{first_name} {last_name}"
    stripe_customer = stripe.Customer.create(email=email , name=name)

    user_profile = UserProfile(is_restaurateur=is_restaurateur if is_restaurateur else False, stripe_id=stripe_customer.id)
    user_profile.user = user
    user_profile.save()
    return JsonResponse({"message": "Success"}, status=200)

@protected_resource()
def get_user_info(request):
    response = {
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name
        }
    orders_array = []
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        orders_array.append(order.to_json())
    response["orders"] = orders_array
    return JsonResponse(response, status=200)

@protected_resource()
@require_http_methods(['GET'])
def stripe_create_ephemeral_key(request):
    try:
        API_VERSION = request.GET["API_VERSION"]
    except KeyError:
        return JsonResponse({"message": 'Required parameter : API_VERSION', "error": "missingParameter"} ,status=400)


    CUSTOMER_ID = request.user.userprofile.stripe_id
    key = stripe.EphemeralKey.create(customer=f'{CUSTOMER_ID}', stripe_version=f'{API_VERSION}')
    return JsonResponse(key, status=200)
