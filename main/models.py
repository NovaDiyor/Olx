from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STATUS_CHOISES = (
        (1, 'admin'),
        (2, 'user')
    )
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOISES)
    number = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)


class Information(models.Model):
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='info/')
    description = models.TextField()
    google_play = models.CharField(max_length=255)
    appstore = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


class AdImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='ads/')


class Category(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='category/')

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubRegion(models.Model):
    district = models.CharField(max_length=210)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Ads(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(SubRegion, on_delete=models.CASCADE)
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    photo = models.ManyToManyField(AdImage)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status = models.IntegerField(choices=(
        (1, 'in admin'),
        (2, 'accepted'),
        (3, 'rejected'),
        (4, 'sold'),
    ), default=1)
    is_top = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class About(models.Model):
    image = models.ImageField(upload_to='about/')
    text = models.CharField(max_length=210)


class Wishlist(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    ip = models.TextField()
