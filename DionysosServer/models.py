import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum

class Restaurant(models.Model):
    def __str__(self):
        return f"{self.name}, {self.id}, propriétaire : {self.owner.username}"

    def to_json(self):
        return {
            "id": self.public_id,
            "name": self.name,
            "profilePic": self.profilePic.url
        }

    def restaurant_profile_pic_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/restaurant_<id>/<filename>
        return 'restaurant/restaurant_{0}/{1}'.format(self.id, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    profilePic = models.ImageField(upload_to=restaurant_profile_pic_directory_path)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Table(models.Model):
    def __str__(self):
        return  f"{self.restaurant.name} : {self.name}, {self.id}"

    def to_json(self):
        return {
            "id": self.public_id,
            "name": self.name,
        }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Section(models.Model):
    def __str__(self):
        return  f"{self.restaurant.name} : {self.name}, {self.id}"

    def to_json(self):
        return {
            "id": self.public_id,
            "name": self.name,
        }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)

class Category(models.Model):
    def __str__(self):
        return  f"{self.section.restaurant.name } : {self.section.name} : {self.name}, {self.id}"

    def category_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/food_<id>/<filename>
        return 'category/category_{0}/{1}'.format(self.id, filename)

    def to_json(self):
        return {
            "id": self.public_id,
            "name": self.name,
            "image": self.image.url
        }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    image = models.ImageField(upload_to=category_directory_path)

class FoodSection(models.Model):
    def __str__(self):
        return  f"{self.category.section.restaurant.name } : {self.category.section.name} : {self.category.name} : {self.name}, {self.id}"

    def to_json(self):
        return {
            "id": self.public_id,
            "name": self.name
        }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)

class Food(models.Model):
    def __str__(self):
        if self.category:
            return  f"{self.category.section.restaurant.name} : {self.name} (Header : {self.category.name}), {self.id}"
        elif self.foodSection:
            return  f"{self.foodSection.category.section.restaurant.name} : {self.name}, {self.id}"
        else:
            return  f"{self.name}, {self.id}"

    def food_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/food_<id>/<filename>
        return 'food/food_{0}/{1}'.format(self.id, filename)

    def to_json(self):
        return {
            "id": self.public_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "ingredients": self.ingredients,
            "image": self.image.url
        }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    foodSection = models.ForeignKey(FoodSection, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=70)
    price = models.FloatField()
    description = models.CharField(max_length=1000)
    ingredients = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=food_directory_path)

class OrderedFood(models.Model):
    def __str__(self):
        return f"{self.id}, quantité: {self.quantity}, prix unitaire payé : {self.paid_price}"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    paid_price = models.FloatField()

class Order(models.Model):
    def __str__(self):
        sum = 0
        for food in self.ordered_foods.all():
            sum += food.paid_price * food.quantity
        return f"{self.state} - Commande {self.id}, ({self.ordered_foods.aggregate(Sum('quantity'))['quantity__sum']} produits, {sum}€), "

    class OrderState(models.TextChoices):
        VALIDEE = 'VA', _('Validée')
        PAYEE = 'PA', _('Payée')
        LIVREE = 'JR', _('Livrée')
        ANNULEE = 'AN', _('Annulée')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ordered_foods = models.ManyToManyField(OrderedFood)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_id = models.CharField(max_length=100)
    state = models.CharField(
        max_length=2,
        choices=OrderState.choices,
        default=OrderState.VALIDEE,
    )
    order_time = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    def __str__(self):
        return f"{self.user.username}, restaurateur = {self.is_restaurateur}"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_restaurateur = models.BooleanField(default=False)
