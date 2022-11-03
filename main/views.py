from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def page_404(request):
    return render(request, 'pages-404.html')


def sign_in(request):
    return render(request, 'sign-in.html')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_user(username=username, email=email, password=password, status=2)
        return redirect('dashboard')
    return render(request, 'sign-up.html')


def for_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user.count() > 0:
            usr = authenticate(username=username, password=password)
            if usr.status == 1:
                if usr is not None:
                    login(request, usr)
                    return redirect('dashboard')
                else:
                    return redirect('sign-in')
            return redirect('sign-up')
        else:
            return redirect('sign-in')
    else:
        return redirect('404')


def logout_view(request):
    logout(request)
    return redirect('sign-in')


@login_required(login_url='sign-in')
def reset(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_password = request.POST.get('new-password')
        prove = request.POST.get('new_password')
        usr = authenticate(username=user.username, password=password)
        if new_password == prove:
            usr.username = username
            usr.set_password(new_password)
            usr.save()
            return redirect('dashboard')
        return redirect('reset')
    return render(request, 'reset-password.html', {'admin': user})


@login_required(login_url='sign-in')
def dashboard_view(request):
    context = {
        'ads': Ads.objects.all(),
        'sold': Ads.objects.filter(status=4).count(),
        'rejected': Ads.objects.filter(status=3).count(),
        'visitors': User.objects.all().count(),
        'accepted': Ads.objects.filter(status=2).count(),
        'in_admin': Ads.objects.filter(status=1).count(),
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='sign-in')
def in_admin(request):
    return render(request, 'in-admin.html', {'for_admin': Ads.objects.filter(status=1)})


@login_required(login_url='sign-in')
def accepted(request):
    return render(request, 'accepted.html', {'accepted': Ads.objects.filter(status=2)})


@login_required(login_url='sign-in')
def rejected(request):
    return render(request, 'rejected.html', {'rejected': Ads.objects.filter(status=3)})


@login_required(login_url='sign-in')
def sold(request):
    return render(request, 'sold.html', {'sold': Ads.objects.filter(status=4)})


@login_required(login_url='sign-in')
def all_admin(request):
    return render(request, 'admins.html', {'admin': User.objects.filter(status=1)})


@login_required(login_url='sign-in')
def advertiser_view(request):
    return render(request, 'users.html', {'advertiser': User.objects.filter(status=2)})


@login_required(login_url='sign-in')
def information_view(request):
    context = {
        'info': Information.objects.all()
    }
    return render(request, "information.html", context)


@login_required(login_url='sign-in')
def category_view(request):
    context = {
        'category': Category.objects.all()
    }
    return render(request, "category.html", context)


@login_required(login_url='sign-in')
def region_view(request):
    context = {
        'region': Region.objects.all()
    }
    return render(request, "region.html", context)


@login_required(login_url='sign-in')
def subregion_view(request):
    context = {
        'sub': SubRegion.objects.all(),
        'region': Region.objects.all()
    }
    return render(request, "sub-region.html", context)


@login_required(login_url='sign-in')
def about_view(request):
    context = {
        'about': About.objects.all()
    }
    return render(request, "about.html", context)


@login_required(login_url='sign-in')
def subcategory_view(request):
    context = {
        'sub': Subcategory.objects.all(),
        "category": Category.objects.all()
    }
    return render(request, "sub-category.html", context)


@login_required(login_url='sign_in')
def single_user(request, pk):
    context = {
        "user": User.objects.get(id=pk),
        "ads": Ads.objects.filter(owner_id=pk)
    }
    return render(request, "single-user.html", context)


@login_required(login_url='sign_in')
def single_ads(request, pk):
    context = {
        "ads": Ads.objects.get(id=pk)
    }
    return render(request, "single-ads.html", context)


@login_required(login_url='sign_in')
def profile(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'profile.html', {'profile': user})


def reject(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.status = 3
    ads.save()
    return redirect('accepted')


def reject_in(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.status = 3
    ads.save()
    return redirect('in-admin')


def accept(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.status = 2
    ads.save()
    return redirect('rejected')


def accept_in(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.status = 2
    ads.save()
    return redirect('in-admin')


def sale(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.status = 4
    ads.save()
    return redirect('accepted')


def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('category')


def delete_region(request, pk):
    region = Region.objects.get(id=pk)
    region.delete()
    return redirect('region')


def delete_subregion(request, pk):
    region = SubRegion.objects.get(id=pk)
    region.delete()
    return redirect('subregion')


def delete_about(request, pk):
    about = About.objects.get(id=pk)
    about.delete()
    return redirect('about')


def delete_info(request, pk):
    info = Information.objects.get(id=pk)
    info.delete()
    return redirect('information')


def delete_sub(request, pk):
    sub = Subcategory.objects.get(id=pk)
    sub.delete()
    return redirect('sub-category')


def update_region(request, pk):
    region = Region.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        region.name = name
        region.save()
        return redirect('region')
    return render(request, 'update-region.html', {'region': Region.objects.get(id=pk)})


def update_sub(request, pk):
    sub = Subcategory.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        sub.name = name
        sub.category_id = category
        sub.save()
        return redirect('sub-category')
    return render(request, 'update-sub.html', {'sub': Subcategory.objects.get(id=pk), 'category': Category.objects.all()})


def up_subregion(request, pk):
    sub = SubRegion.objects.get(id=pk)
    if request.method == 'POST':
        district = request.POST.get('name')
        region = request.POST.get('region')
        sub.district = district
        sub.region_id = region
        sub.save()
        return redirect('subregion')
    return render(request, 'update-subregion.html', {'sub': SubRegion.objects.get(id=pk), 'region': Region.objects.all()})


def update_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('photo')
        category.name = name
        if image is None:
            category.photo = category.photo
        else:
            category.photo = image
        category.save()
        return redirect('category')
    return render(request, 'update-category.html', {'category': Category.objects.get(id=pk)})


def update_about(request, pk):
    about = About.objects.get(id=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        about.text = text
        about.photo = image
        about.save()
        return redirect('about')
    return render(request, 'update-about.html', {'about': About.objects.get(id=pk)})


def up_info(request, pk):
    info = Information.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get("logo")
        description = request.POST.get('description')
        google = request.POST.get('google')
        apple = request.POST.get('appstore')
        info.company_name = name
        if image is None:
            info.logo = info.logo
        else:
            info.logo = image
        info.description = description
        info.google_play = google
        info.appstore = apple
        info.save()
        return redirect('information')
    return render(request, 'update-info.html', {'info': Information.objects.get(id=pk)})


def add_info(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        logo = request.FILES.get("logo")
        description = request.POST.get("description")
        google = request.POST.get("google")
        appstore = request.POST.get("appstore")
        Information.objects.create(
            company_name=company_name,
            logo=logo,
            description=description,
            google_play=google,
            appstore=appstore,
        )
    return redirect("information")


def add_sub(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        Subcategory.objects.create(name=name, category_id=category)
    return redirect("sub-category")


def add_subregion(request):
    if request.method == "POST":
        name = request.POST.get("name")
        region = request.POST.get("region")
        SubRegion.objects.create(district=name, region_id=region)
    return redirect("subregion")


def add_region(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Region.objects.create(name=name)
    return redirect("region")


def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        Category.objects.create(name=name, photo=photo)
    return redirect("category")


def add_about(request):
    if request.method == "POST":
        text = request.POST.get("text")
        image = request.FILES.get("image")
        About.objects.create(text=text, image=image)
    return redirect("about")


def search(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        name = request.POST.get('name')
        if status == '1':
            context = {
                'status': status,
                'search': Ads.objects.filter(name__icontains=name)
            }
            return render(request, 'search.html', context)
        elif status == '2':
            context = {
                'status': status,
                'search_user': User.objects.filter(username__icontains=name)
            }
            return render(request, 'search.html', context)
        else:
            return redirect('dashboard')
    else:
        return render(request, 'search.html')


