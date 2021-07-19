from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Profile, City, Penetration, Comment, UserComment
from .forms import (
    UserForm,
    ProfileForm,
    Add_nuwsForm,
    Add_citeForm,
    PenetrationForm,
    EditPenetrationForm,
    CommentForm,
    UserCommentForm,
    DeleteCommentForm,
    DeleteUserCommentForm,
    EditCommentForm
)
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from PIL import Image
from django.http import JsonResponse
import json
import requests


def get_info(request):  # Функция для получение информации
    islogin = request.user.is_authenticated  # залогинен ли вользователь
    header_img, style_file = get_style(request)  # узнаём какая должна быть
    news = get_news(request)  # достаём новости для сайд бара
    return(islogin, header_img, style_file, news)


def discord(request):  # Функция коннекта к ДСу
    token = request.GET.get("code")
    r = requests.get("https://discord.com/api/users/@me", headers={
        "Authorization": f"{token}"
    })
    return(JsonResponse(r.json()))


def api(request):  # Функция для бота посути
    if("token" in request.headers):  # Проверка токена
        if(request.headers["Token"] not in ["test"]):
            return(JsonResponse({"error": "403"}))
    else:
        return(JsonResponse({"error": "403"}))
    if(request.headers["Rtype"] == "get"):  # Бот хочет получить данные?
        result = {'news': [], 'users': [], "citys": [], "error": 200}
        obj_news = get_news(request)
        for i in obj_news:  # Новости
            result['news'].append(
                {
                    "title": i.title,
                    "text": i.text,
                    "comments": [
                        {
                            "name": comment.name,
                            "userid": comment.userid,
                            "text": comment.body  # Коментарии
                        } for comment in i.comments.filter(active=True)
                    ]
                }
            )
        for i in Profile.objects.all():  # Профили
            result['users'].append(
                {
                    "username": i.user.username,
                    "info": i.info,
                    "role": i.role,
                    "isAdmin": i.admin,
                    # "discord": i.discord
                }
            )
        for i in City.objects.all():  # Города
            result["citys"].append(
                {
                    "title": i.title,
                    "smol_text": i.smol_text,
                    "text": i.text,
                    "author": i.author,
                    "mayor": i.mayor
                }
            )
        return(JsonResponse(result))

    elif(request.headers["Rtype"] == "post"):  # Бот хочет добавить данные?
        if("Add-discord" in request.headers and False):  # Данные о ДС
            # Но код отключен тк бд не может хранить дс
            json_data = json.loads(request.headers["Add-discord"])
            username = json_data["username"]
            discord_id = json_data["discord_id"]
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            if(profile is not None):  # Если профиль существет то присваиваем.
                profile.discord = discord_id  # см models.py 88-89
            else:
                return(JsonResponse({"error": 404}))
            return(JsonResponse({"error": 200}))
    return(JsonResponse({"error": 404}))


def get_client_ip(request):  # берём ip юзера
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_news(request):  # достаём список новостей из бд, для сайд бара
    res = News.objects.all()  # достаём все обьекты новостей
    res = res.filter(active=True)  # отбрасываем неактивные
    res = list(reversed(res))  # переворачиваем список, что бы новые шли первее
    page_obj = [res[0], res[1], res[2]]  # отбераем три новейшие
    return page_obj  # возвращаем новости для дальнейшего использования


def get_style(request):  # изменение темы
    img = 'image/logo.png'  # расположение логотипа сайта в директории static
    if('theme' in request.COOKIES):  # если в куки есть тема
        file = request.COOKIES['theme']  # записываем расположение файла темы
    else:
        file = 'css/purple_gold.css'  # иначе записываем стандартную тему
    return(img, file)  # возвращаем расположение файлов



#Обычные

def show_main(request):  # отображение главной страницы
    islogin, header_img, style_file, news = get_info(request)

    context = {  # контекст для шаблона
           'newses': news,
           'islogin': islogin,
           'header_img': header_img,
           'style_file': style_file
          }
    return render(request, 'primitive/main_page.html', context)  # отображение шаблона




def show_map(request):
    islogin, header_img, style_file, news = get_info(request)
    context = {
        'newses': news,
        'islogin': islogin,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'primitive/map_page.html', context)


def show_info(request):
    islogin, header_img, style_file, news = get_info(request)
    context = {
        'newses': news,
        'islogin': islogin,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'primitive/info_page.html', context)


def register(request):
    islogin, header_img, style_file, news = get_info(request)
    err = ''
    if(request.method == "POST"):
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect("/marupik/main")
        else:
            err = user_form.errors.as_data()
    else:
        user_form = UserCreationForm()

    err = str(err).split("'")
    error = []
    for i in err:
        res = i.split(".")
        for ii in res:
            if ii == '':
                error.append(i)

    context = {
        'newses': news,
        'error': error,
        'islogin': islogin,
        'user_form': user_form,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'primitive/register_page.html', context)


def logout_user(request):
    logout(request)
    return redirect("/marupik/main")


def login_user(request):
    islogin, header_img, style_file, news = get_info(request)
    err = ''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/marupik/main')
            else:
                err = "Пользователь с таким именем не существует"
        else:
            err = "Не верно указаны логин или пароль"

    form = AuthenticationForm()
    context = {
        'newses': news,
        'error': err,
        'islogin': islogin,
        'form': form,
        'header_img': header_img,
        'style_file': style_file
    }

    return render(request, 'primitive/login_page.html', context)



def all_profile(request):
    islogin, header_img, style_file, news = get_info(request)

    users = User.objects.all()
    context = {
                'newses': news,
                'islogin': islogin,
                'users': users,
                'header_img': header_img,
                'style_file': style_file,
                }

    return render(request, 'primitive/all_profile_page.html', context)










#Новости


def show_news(request):
    islogin = request.user.is_authenticated  # залогинен ли вользователь
    header_img, style_file = get_style(request)  # узнаём какая тема

    res = News.objects.all()
    res = res.filter(active=True)
    res = list(reversed(res))
    paginator = Paginator(res, 3)
    page_num = request.GET.get('page')
    news = paginator.get_page(page_num)

    context = {
        'newses': news,
        'paginator': paginator,
        'islogin': islogin,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'news/news_page.html', context)


def show_one_news(request, news_id):
    islogin, header_img, style_file, news = get_info(request)
    res = get_object_or_404(News, pk=news_id)
    news_text = res.text.split("\r\n")
    user = request.user.username

    comments = res.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user.username
            new_comment.role = request.user.profile.role
            new_comment.image = request.user.profile.user_image.url
            new_comment.userid = request.user.pk
            new_comment.news = res
            new_comment.save()
            return redirect(f"/news/{news_id}/")
    else:
        comment_form = CommentForm()

    context = {
        'news': res,
        'islogin': islogin,
        'news_text': news_text,
        'user': user,
        'comments': comments,
        'comment_form': comment_form,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'news/one_news_page.html', context)


def delete_news_comment(request, comment_id, news_id):
    islogin, header_img, style_file, news = get_info(request)
    comment_to_delete = get_object_or_404(Comment, id=comment_id)
    name = comment_to_delete.name
    if request.method == 'POST':
        form = DeleteCommentForm(request.POST, instance=comment_to_delete)

        if form.is_valid():
            comment_to_delete.delete()
            return redirect(f"/marupik/news/{news_id}/")

    else:
        form = DeleteCommentForm(instance=comment_to_delete)

    context = {
        'islogin': islogin,
        'form': form,
        'name': name,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'news/delete_news_comment_page.html', context)


def edit_news_comment(request, comment_id, news_id):
    islogin, header_img, style_file, news = get_info(request)
    res = get_object_or_404(News, pk=news_id)
    news_text = res.text.split("\r\n")
    user = request.user.username

    comments = res.comments.filter(active=True)

    comment_to_edit = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        edit_comment_form = EditCommentForm(
            request.POST,
            instance=comment_to_edit
        )
        if edit_comment_form.is_valid():
            edit_comment_form.save()
            return redirect(f"/marupik/news/{news_id}/")
        else:
            err = edit_comment_form.errors.as_data()
            print(err)
    else:
        comment_form = CommentForm()
        edit_comment_form = EditCommentForm(instance=comment_to_edit)

    context = {
        'news': res,
        'islogin': islogin,
        'news_text': news_text,
        'user': user,
        'comments': comments,
        'comment_form': comment_form,
        'edit_comment_form': edit_comment_form,
        'comment_id': comment_id,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'news/edit_news_comment_page.html', context)


def add_news(request):
    islogin, header_img, style_file, news = get_info(request)

    if(request.method == "POST"):
        news_form = Add_nuwsForm(request.POST, request.FILES)
        if(news_form.is_valid()):
            new = news_form.save(commit=False)
            new.author = request.user.username
            new.save()
            news_form.save()
            return redirect("/marupik/news")
    else:
        news_form = Add_nuwsForm()

    role = request.user.profile.role

    context = {
        'newses': news,
        'islogin': islogin,
        'news_form': news_form,
        'role': role,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'news/add_news_page.html', context)


def edit_news(request, news_id):
    islogin, header_img, style_file, news = get_info(request)
    res = get_object_or_404(News, pk=news_id)

    if(request.method == "POST"):
        news_form = Add_nuwsForm(request.POST, request.FILES, instance=res)
        if news_form.is_valid():
            news_form.save()
            return redirect("/marupik/news")
    else:
        news_form = Add_nuwsForm(instance=res)

    author = res.author
    user = request.user
    image = res.image.url

    context = {
        'newses': news,
        'islogin': islogin,
        'news_form': news_form,
        'author': author,
        'user': user,
        'image': image,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'news/edit_news_page.html', context)














# Профиль



def upgrade_profile(request):
    islogin, header_img, style_file, news = get_info(request)
    err = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            profile_form.save()
            return redirect('/marupik/profile')
        else:
            err = user_form.errors.as_data()
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        err = user_form.errors.as_data()

    err = str(err).split("'")
    error = []
    for i in err:
        res = i.split(".")
        for ii in res:
            if ii == '':
                error.append(i)

    user_image = request.user.profile.user_image.url

    context = {
        'newses': news,
        'user_image': user_image,
        'islogin': islogin,
        'user_form': user_form,
        'profile_form': profile_form,
        'error': error,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'profile/upgrade_profile_page.html', context)


def profile(request):
    islogin, header_img, style_file, news = get_info(request)

    username = request.user.username
    user_image = request.user.profile.user_image.path
    full_info = request.user.profile.info.split("\r\n")
    role = request.user.profile.role
    admin = request.user.profile.admin
    userid = request.user.pk

    if username != 'Kikono':
        user_image = user_image.replace("\\", "/")
        img = Image.open(user_image)
        width = img.size[0]
        height = img.size[1]
        if width != height:
            newsize = (width, width)
            img = img.resize(newsize)
            width = img.size[0]
            height = img.size[1]
            img.save(user_image, format="png")

    user_image = request.user.profile.user_image.url

    if(role == 'Мэр'):
        cities = City.objects.all()
        cities = cities.filter(active=True)
        cities = list(reversed(cities))
        for city in cities:
            if city.mayor == username:
                your_city_name = city.title
                your_city_id = city.pk
    else:
        your_city_name = None
        your_city_id = None

    if role == 'Президент':
        role_color = "rgb(200, 0, 200)"
    elif role == 'ФБР' or role == 'Глава ФБР':
        role_color = "blue"
    elif role == 'Мэр':
        role_color = "brown"
    elif role == 'Журналист':
        role_color = "rgb(0, 200, 100)"
    elif style_file == 'css/dark1.css':
        role_color = "white"
    else:
        role_color = "black"

    context = {
        'newses': news,
        'islogin': islogin,
        'user_image': user_image,
        'username': username,
        'full_info': full_info,
        'role': role,
        'admin': admin,
        'your_city_id': your_city_id,
        'your_city_name': your_city_name,
        'userid': userid,
        'role_color': role_color,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'profile/profile_page.html', context)


def another_profile(request, user_id):
    islogin, header_img, style_file, news = get_info(request)

    user = get_object_or_404(User, pk=user_id)

    username = user.username
    user_image = user.profile.user_image.url
    full_info = user.profile.info.split("\r\n")
    role = user.profile.role
    admin = user.profile.admin

    if role == 'Президент':
        role_color = "rgb(200, 0, 200)"
    elif role == 'ФБР' or role == 'Глава ФБР':
        role_color = "blue"
    elif role == 'Мэр':
        role_color = "brown"
    elif role == 'Журналист':
        role_color = "rgb(0, 200, 100)"
    elif style_file == 'css/dark1.css':
        role_color = "white"
    else:
        role_color = "black"

    comments = user.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = UserCommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user.username
            new_comment.role = request.user.profile.role
            new_comment.image = request.user.profile.user_image.url
            new_comment.user = user
            new_comment.userid = request.user.pk
            new_comment.save()
            return redirect(f"/profile/{user_id}/")
    else:
        comment_form = UserCommentForm()

    context = {
        'newses': news,
        'islogin': islogin,
        'user_image': user_image,
        'username': username,
        'full_info': full_info,
        'role': role,
        'admin': admin,
        'comments': comments,
        'comment_form': comment_form,
        'user': user,
        'role_color': role_color,
        'header_img': header_img,
        'style_file': style_file
    }

    return render(request, 'profile/another_profile_page.html', context)


def delete_user_comment(request, comment_id, user_id):
    islogin, header_img, style_file, news = get_info(request)

    comment_to_delete = get_object_or_404(UserComment, id=comment_id)
    name = comment_to_delete.name
    if request.method == 'POST':
        form = DeleteUserCommentForm(request.POST, instance=comment_to_delete)

        if form.is_valid():
            comment_to_delete.delete()
            return redirect(f"/marupik/profile/{user_id}/")

    else:
        form = DeleteUserCommentForm(instance=comment_to_delete)

    context = {
        'islogin': islogin,
        'form': form,
        'name': name,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'profile/delete_user_comment_page.html', context)






#Города


def show_cities(request):
    islogin, header_img, style_file, news = get_info(request)

    city = City.objects.all()
    city = city.filter(active=True)
    city = list(reversed(city))
    paginator = Paginator(city, 4)
    page_num = request.GET.get('page')
    cities = paginator.get_page(page_num)

    for city in cities:
        city_image = city.image.path

        city_image = city_image.replace("\\", "/")
        img = Image.open(city_image)
        width = img.size[0]
        height = img.size[1]
        if width != 300 and height != 300:
            newsize = (300, 300)
            img = img.resize(newsize)
            width = img.size[0]
            height = img.size[1]
            img.save(city_image, format="png")

    context = {
                'newses': news,
                'cities': cities,
                'paginator': paginator,
                'islogin': islogin,
                'header_img': header_img,
                'style_file': style_file
                }

    return render(request, 'city/cities_page.html', context)


def show_one_city(request, city_id):
    islogin, header_img, style_file, news = get_info(request)
    city = get_object_or_404(City, pk=city_id)
    text = city.text.split("\r\n")

    author = city.author
    mayor = city.mayor
    user = request.user

    images = [
        city.image1.path,
        city.image2.path,
        city.image3.path,
        city.image4.path,
        city.image5.path,
    ]

    for city_image in images:
        city_image = city_image.replace("\\", "/")
        img = Image.open(city_image)
        width = img.size[0]
        height = img.size[1]
        if width != 640 and height != 400:
            newsize = (640, 400)
            img = img.resize(newsize)
            width = img.size[0]
            height = img.size[1]
            img.save(city_image, format="png")

    context = {
        'islogin': islogin,
        'city': city,
        'text': text,
        'author': author,
        'mayor': mayor,
        'user': user,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'city/one_city_page.html', context)


def add_city(request):
    islogin, header_img, style_file, news = get_info(request)

    if(request.method == "POST"):
        city_form = Add_citeForm(request.POST, request.FILES)
        if city_form.is_valid():
            city = city_form.save(commit=False)
            city.author = request.user.username
            city.save()
            city_form.save()
            return redirect("/marupik/cities")
    else:
        city_form = Add_citeForm()

    role = request.user.profile.role

    context = {
        'newses': news,
        'islogin': islogin,
        'city_form': city_form,
        'role': role,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'city/city/add_city_page.html', context)


def edit_city(request, city_id):
    islogin, header_img, style_file, news = get_info(request)
    city = get_object_or_404(City, pk=city_id)

    if(request.method == "POST"):
        city_form = Add_citeForm(request.POST, request.FILES, instance=city)
        if city_form.is_valid():
            city = city_form.save(commit=False)
            city.author = request.user.username
            city.save()
            city_form.save()
            return redirect(f"/marupik/city/{city_id}")
    else:
        city_form = Add_citeForm(instance=city)

    author = city.author
    mayor = city.mayor
    user = request.user
    image = city.image.url

    context = {
        'islogin': islogin,
        'city_form': city_form,
        'author': author,
        'mayor': mayor,
        'user': user,
        'image': image,
        'city': city,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'city/edit_city_page.html', context)









#Форма регистрации

def show_forms(request):
    islogin, header_img, style_file, news = get_info(request)

    form = Penetration.objects.all()
    form = form.filter(status=False)
    paginator = Paginator(form, 9)
    page_num = request.GET.get('page')
    forms = paginator.get_page(page_num)

    user = request.user

    context = {
        'newses': news,
        'forms': forms,
        'paginator': paginator,
        'islogin': islogin,
        'user': user,
        'header_img': header_img,
        'style_file': style_file
    }

    return render(request, 'form/forms_page.html', context)


def show_one_form(request, form_id):
    islogin, header_img, style_file, news = get_info(request)
    form = get_object_or_404(Penetration, pk=form_id)
    description = form.description_yourself.split("\r\n")

    if(request.method == "POST"):
        penetration_form = EditPenetrationForm(
            request.POST,
            request.FILES,
            instance=form
        )
        if penetration_form.is_valid():
            penetration_form.save()
            return redirect("/marupik/forms")
    else:
        penetration_form = EditPenetrationForm(instance=form)

    user = request.user
    context = {
            'newses': news,
            'islogin': islogin,
            'form': form,
            'description': description,
            'user': user,
            'penetration_form': penetration_form,
            'header_img': header_img,
            'style_file': style_file
            }

    return render(request, 'form/one_form_page.html', context)


def add_form(request):
    islogin, header_img, style_file, news = get_info(request)

    if(request.method == "POST"):
        penetration_form = PenetrationForm(request.POST, request.FILES)
        if penetration_form.is_valid():
            form = penetration_form.save(commit=False)
            form.site_username = request.user.username
            form.save()
            penetration_form.save()
            return redirect("/marupik/forms")

    else:
        penetration_form = PenetrationForm()

    role = ''
    if islogin:
        role = request.user.profile.role

    context = {
        'newses': news,
        'islogin': islogin,
        'penetration_form': penetration_form,
        'role': role,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'form/add_form_page.html', context)


def edit_form(request, form_id):
    islogin, header_img, style_file, news = get_info(request)

    form = get_object_or_404(Penetration, pk=form_id)

    if(request.method == "POST"):
        penetration_form = PenetrationForm(
            request.POST,
            request.FILES,
            instance=form
        )
        if penetration_form.is_valid():
            form = penetration_form.save(commit=False)
            form.site_username = request.user.username
            form.save()
            penetration_form.save()
            return redirect(f"/marupik/form/{form_id}")
    else:
        penetration_form = PenetrationForm(instance=form)

    user = request.user

    context = {
        'newses': news,
        'islogin': islogin,
        'penetration_form': penetration_form,
        'user': user,
        'form': form,
        'header_img': header_img,
        'style_file': style_file
    }
    return render(request, 'form/edit_form_page.html', context)






#Тема


def colored_purpule_gold_theme(request):
    style_file = 'css/purple_gold.css'

    response = redirect("/marupik/main")
    response.set_cookie('theme', style_file)
    return response


def dark_theme(request):
    style_file = 'css/dark1.css'

    response = redirect("/marupik/main")
    response.set_cookie('theme', style_file)
    return response


def light_theme(request):
    style_file = 'css/light1.css'

    response = redirect("/marupik/main")
    response.set_cookie('theme', style_file)
    return response
