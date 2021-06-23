from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Profile, City, Penetration, Comment, UserComment
from .forms import UserForm, ProfileForm, Add_nuwsForm, Add_citeForm, PenetrationForm, EditPenetrationForm, CommentForm, UserCommentForm, DeleteCommentForm, DeleteUserCommentForm, EditCommentForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import cv2


def get_news(request):
	res = News.objects.all()
	res = res.filter(active=True)
	res = list(reversed(res))
	page_obj = [res[0], res[1], res[2]]
	return page_obj







def show_main(request):
	islogin = request.user.is_authenticated
	if request.method == "GET":
		news = get_news(request)
		context = {'newses': news, 'islogin': islogin}
		return render(request, 'main_page.html', context)

def show_map(request):
	islogin = request.user.is_authenticated
	if request.method == "GET":
		news = get_news(request)
		context = {'newses': news, 'islogin': islogin}
		return render(request, 'map_page.html', context)


def show_info(request):
	islogin = request.user.is_authenticated
	if request.method == "GET":
		news = get_news(request)
		context = {'newses': news, 'islogin': islogin}
		return render(request, 'info_page.html', context)


def show_news(request):
	islogin = request.user.is_authenticated
	if request.method == "GET":
		res = News.objects.all()
		res = res.filter(active=True)
		res = list(reversed(res))
		paginator = Paginator(res, 3)
		page_num = request.GET.get('page')
		news = paginator.get_page(page_num)

		context = {'newses': news, 'paginator': paginator,'islogin': islogin}
		return render(request, 'news_page.html', context)

def show_one_news(request, news_id):
	islogin = request.user.is_authenticated
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
		'news_text':news_text,
		'user':user, 
		'comments': comments, 
		'comment_form': comment_form,
	}
	return render(request, 'one_news_page.html', context)

def delete_comment(request, comment_id, news_id):
	comment_to_delete = get_object_or_404(Comment, id=comment_id)
	name = comment_to_delete.name
	if request.method == 'POST':
		form = DeleteCommentForm(request.POST, instance=comment_to_delete)

		if form.is_valid():
			comment_to_delete.delete()
			return redirect(f"/marupik/news/{news_id}/") 

	else:
		form = DeleteCommentForm(instance=comment_to_delete)

	context = {'form': form, 'name': name,}
	return render(request, 'delete_comment_page.html', context)

def edit_comment(request, comment_id, news_id):
	islogin = request.user.is_authenticated
	res = get_object_or_404(News, pk=news_id)
	news_text = res.text.split("\r\n")
	user = request.user.username

	comments = res.comments.filter(active=True)


	comment_to_edit = get_object_or_404(Comment, id=comment_id)
	if request.method == 'POST':
		edit_comment_form = EditCommentForm(request.POST, instance=comment_to_edit)
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
		'news_text':news_text,
		'user':user, 
		'comments': comments, 
		'comment_form': comment_form,
		'edit_comment_form':edit_comment_form,
		'comment_id': comment_id,
	}
	return render(request, 'edit_comment_page.html', context)




def add_nuws(request):
	islogin = request.user.is_authenticated
	news = get_news(request)

	if request.method=="POST":
		news_form = Add_nuwsForm(request.POST, request.FILES)
		if news_form.is_valid():
			new = news_form.save(commit=False)
			new.author = request.user.username
			new.save()
			news_form.save()
			return redirect("/marupik/news")
	else:
		news_form = Add_nuwsForm()


	role = request.user.profile.role 



	context = {'newses': news,'islogin': islogin, 'news_form': news_form, 'role': role}
	return render(request, 'add_nuws_page.html', context)

def edit_nuws(request, news_id):
	islogin = request.user.is_authenticated
	news = get_news(request)
	res = get_object_or_404(News, pk=news_id)

	if request.method=="POST":
		news_form = Add_nuwsForm(request.POST, request.FILES, instance=res)
		if news_form.is_valid():
			news_form.save()
			return redirect("/marupik/news")
	else:
		news_form = Add_nuwsForm(instance=res)



	author = res.author
	user = request.user 
	image = res.image.url

	context = {'newses': news,'islogin': islogin, 'news_form': news_form, 'author': author, 'user': user, 'image': image}
	return render(request, 'edit_nuws_page.html', context)





def register(request):
	islogin = request.user.is_authenticated
	news = get_news(request)
	err = ''
	if request.method=="POST":
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

	context = {'newses': news, 'error': error,'islogin': islogin, 'user_form': user_form}
	return render(request,'register_page.html',context)

def logout_user(request):
	logout(request)
	return redirect("/marupik/main")

def login_user(request):
	islogin = request.user.is_authenticated
	news = get_news(request)
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
	context = {'newses': news, 'error':err, 'islogin': islogin, 'form': form}
	
	return render(request,'login_page.html', context)


def upgrade_profile(request):
	islogin = request.user.is_authenticated
	news = get_news(request)
	err = ''
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES,instance=request.user.profile)
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
				'error': error}
	return render(request, 'upgrade_profile_page.html', context)



def profile(request):
	islogin = request.user.is_authenticated
	news = get_news(request)
	if request.method == "GET":
		username = request.user.username
		user_image = request.user.profile.user_image.path
		full_info = request.user.profile.info.split("\r\n")
		role = request.user.profile.role
		admin = request.user.profile.admin
		userid = request.user.pk

		if username != "Kikono":
			img = cv2.imread(user_image)
			if img.shape[1] != img.shape[0]:
				img = cv2.resize(img, (img.shape[0], img.shape[0]))
				cv2.imwrite(user_image, img)

		user_image = request.user.profile.user_image.url

		if role == 'Президент':
			role_color = "rgb(200, 0, 200)"
		elif role == 'ФБР' or role == 'Глава ФБР':
			role_color = "blue"
		elif role == 'Мэр':
			role_color = "brown"
		elif role == 'Журналист':
			role_color = "rgb(0, 200, 100)"
		else:
			role_color = "black"

		your_city_name = ''
		your_city_id = 3
		if role == 'Мэр':
			cities = City.objects.all()
			cities = cities.filter(active=True)
			cities = list(reversed(cities))
			for city in cities:
				if city.mayor == username:
					your_city_name = city.title
					your_city_id == city.pk

		context = {
					'newses': news,
					'islogin': islogin,
					'user_image': user_image,
					'username': username,
					'full_info': full_info,
					'role':role,
					'admin': admin,
					'role_color': role_color,
					'your_city_id': your_city_id,
					'your_city_name': your_city_name,
					'userid': userid,
					}
		return render(request, 'profile_page.html', context)

def another_profile(request, user_id):
	islogin = request.user.is_authenticated
	news = get_news(request)

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
			new_comment.userid = user_id
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
				'role':role,
				'admin': admin,
				'role_color': role_color,
				'comments': comments, 
				'comment_form': comment_form,
				'user': user,
				}

	return render(request, 'another_profile_page.html', context)


def delete_user_comment(request, comment_id, user_id):
	comment_to_delete = get_object_or_404(UserComment, id=comment_id)
	name = comment_to_delete.name
	if request.method == 'POST':
		form = DeleteUserCommentForm(request.POST, instance=comment_to_delete)

		if form.is_valid():
			comment_to_delete.delete()
			return redirect(f"/marupik/news/{user_id}/") 

	else:
		form = DeleteUserCommentForm(instance=comment_to_delete)

	context = {'form': form, 'name': name,}
	return render(request, 'delete_user_comment_page.html', context)



def all_profile(request):
	islogin = request.user.is_authenticated
	news = get_news(request)

	users = User.objects.all()

	context = {
				'newses': news,
				'islogin': islogin,
				'users': users,
				}

	return render(request, 'all_profile_page.html', context)




def show_cities(request):
	islogin = request.user.is_authenticated
	news = get_news(request)

	if request.method == "GET":
		city = City.objects.all()
		city = city.filter(active=True)
		city = list(reversed(city))
		paginator = Paginator(city, 4)
		page_num = request.GET.get('page')
		cities = paginator.get_page(page_num)

		for city in cities:
			city_image = city.image.path
			
			
			img = cv2.imread(city_image)
			if img.shape[1] != 300 and img.shape[0] != 300:
				img = cv2.resize(img, (300, 300))
				cv2.imwrite(city_image, img)


	context = {
				'newses': news,
				'cities': cities, 
				'paginator': paginator,
				'islogin': islogin,
				}

	return render(request, 'cities_page.html', context)



def show_one_city(request, city_id):
	islogin = request.user.is_authenticated

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
		img = cv2.imread(city_image)
		if img.shape[1] != 640 or img.shape[0] != 400:
			img = cv2.resize(img, (640, 400))
			cv2.imwrite(city_image, img)


	context = {
			'islogin': islogin, 
			'city': city,
			'text':text,
			'author': author,
			'mayor': mayor,
			'user': user,

			}
	return render(request, 'one_city_page.html', context)



def add_cite(request):
	islogin = request.user.is_authenticated
	news = get_news(request)

	if request.method=="POST":
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
	user = request.user


	context = {'newses': news,'islogin': islogin, 'city_form': city_form, 'role': role}
	return render(request, 'add_cite_page.html', context)

def edit_cite(request, city_id):
	islogin = request.user.is_authenticated
	city = get_object_or_404(City, pk=city_id)

	if request.method=="POST":
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

	

	context = {'islogin': islogin, 'city_form': city_form, 'author': author, 'mayor': mayor, 'user': user, 'image': image, 'city': city}
	return render(request, 'edit_cite_page.html', context)








def show_forms(request):
	islogin = request.user.is_authenticated
	news = get_news(request)

	if request.method == "GET":
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
				'user': user
				}

	return render(request, 'forms_page.html', context)





def show_one_form(request, form_id):
	islogin = request.user.is_authenticated
	news = get_news(request)
	form = get_object_or_404(Penetration, pk=form_id)
	description = form.description_yourself.split("\r\n")

	if request.method=="POST":
		penetration_form = EditPenetrationForm(request.POST, request.FILES, instance = form)
		if penetration_form.is_valid():
			penetration_form.save()
			return redirect("/marupik/forms")
	else:
		penetration_form = EditPenetrationForm(instance = form)


	

	user = request.user
	context = {
			'newses': news,
			'islogin': islogin, 
			'form': form,
			'description': description,
			'user': user,
			'penetration_form': penetration_form,
			}

	return render(request, 'one_form_page.html', context)


def add_form(request):
	islogin = request.user.is_authenticated
	news = get_news(request)

	if request.method=="POST":
		penetration_form = PenetrationForm(request.POST, request.FILES)
		if penetration_form.is_valid():
			form = penetration_form.save(commit=False)
			form.site_username = request.user.username
			form.save() 
			penetration_form.save()
			return redirect("/marupik/forms")

	else:
		penetration_form = PenetrationForm()

	role = request.user.profile.role


	context = {'newses': news,'islogin': islogin, 'penetration_form': penetration_form, 'role': role}
	return render(request, 'add_form_page.html', context)


def edit_form(request, form_id):
	islogin = request.user.is_authenticated
	form = get_object_or_404(Penetration, pk=form_id)
	news = get_news(request)

	if request.method=="POST":
		penetration_form = PenetrationForm(request.POST, request.FILES, instance=form)
		if penetration_form.is_valid():
			form = penetration_form.save(commit=False)
			form.site_username = request.user.username
			form.save()
			penetration_form.save()
			return redirect(f"/marupik/one_form/{form_id}")
	else:
		penetration_form = PenetrationForm(instance=form)


	user = request.user

	

	context = {'newses': news, 'islogin': islogin, 'penetration_form': penetration_form, 'user': user, 'form': form}
	return render(request, 'edit_form_page.html', context)
