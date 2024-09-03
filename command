cd ..
cd skillfactory_D4.7_HW-03
cd NewsPortal

python -m venv venv
venv\scripts\activate
pip install django

python -m pip install django_filter
pip install requests
pip install django-allauth==0.54.0
pip install django-extensions

pip install django-apscheduler

pip list


pip3 install celery
pip3 install redis
pip3 install -U "celery[redis]"

django-admin startproject NewsPortal
cd NewsPortal
python manage.py startapp news
python manage.py startapp accounts

pip install django-allauth


python manage.py makemigrations
python manage.py migrate
python manage.py runserver

python manage.py runapscheduler

python manage.py createsuperuser

pip3 install celery
Для запуска периодических задач на Windows запустите в разных окнах терминала:
celery -A NewsPortal worker -l INFO
и
celery -A NewsPortal beat -l INFO

python manage.py shell
from news.models import *
+ 1 создать двух пользователей (с помощью метода User.objects.create_user('username')).
u1 = User.objects.create_user(username='Max')
u1
u2 = User.objects.create_user(username='Sam')
u2
u3 = User.objects.create_user(username='Anna')
u4 = User.objects.create_user(username='Liza')

+ 2 Создать два объекта модели Author, связанные с пользователями
Author.objects.create(user=u1)
Author.objects.create(user=u2)
Author.objects.all()

+ 3 Добавить 4 категории в модель Category.
Category.objects.create(name='IT')
Category.objects.create(name='SCIENCE')
Category.objects.create(name='SPORT')
Category.objects.create(name='PEOPLE')
Вызываем авторов
author = Author.objects.get(id=1)
author2 = Author.objects.get(id=2)

+4Добавить 2 статьи и 1 новость
Post.objects.create(author=author, categoryType='NW', title='Sensation!', text='blahblahblah')
Post.objects.create(author=author, categoryType='AR', title='Sporty AI', text='AI makes sport easy for everyone')
Post.objects.create(author=author2, categoryType='AR', title='Nerds', text='Nerds in science')

+5 Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
>>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=4))
>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=1))
>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=2))
>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=3))


+6 Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=1).user, text='no way')
Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.objects.get(id=2).user, text='LOL')
Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.objects.get(id=1).user, text='interesting...')
Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.objects.get(id=2).user, text='greate post')
Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.objects.get(id=2).user, text='Hello world')
Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=User.objects.get(id=3), text='nteresting')
Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=User.objects.get(id=4), text='It is really nice')

+7 Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).dislike()
Comment.objects.get(id=1).rating
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=5).dislike()
Comment.objects.get(id=6).like()
Comment.objects.get(id=7).like()
Post.objects.get(id=1).like()
Post.objects.get(id=1).like()
Post.objects.get(id=2).like()
Post.objects.get(id=3).like()
Post.objects.get(id=1).dislike()

+8 Обновить рейтинги пользователей
Author.objects.get(id=1)
a = Author.objects.get(id=1)
a.update_rating()
a.rating
b = Author.objects.get(id=2)
b.update_rating()
b.rating

+9 Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта)
a = Author.objects.order_by('-rating')[:1]
a
a = Author.objects.order_by('-rating')
a
for i in a:
    i.rating
    i.user.username

превью:
Post.objects.get(id=1).preview()
Post.objects.get(id=2).preview()
Post.objects.get(id=3).preview()

+10 Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
bestPost = Post.objects.order_by('-rating')[:1]
bestPost

for i in bestPost:
    i.dateCreation
    i.author.user
    i.rating
    i.title
    i.preview()

+11 Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
bestPostCom = Comment.objects.filter(commentPost=3)
bestPostCom

for k in bestPostCom:
    k.dateCreation
    k.commentUser
    k.rating
    k.text
