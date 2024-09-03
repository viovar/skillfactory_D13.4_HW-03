from celery import shared_task
from django.core.mail import send_mail
from .models import Post, Subscription
from django.utils import timezone

@shared_task
def send_notification_to_subscribers(news_id):
    try:
        news = Post.objects.get(pk=news_id)
        subscribers = Subscription.objects.all()  # Получаем всех подписчиков
        if subscribers:
            subject = "New post is released"
            message = f"New news/article is published: {news.title}. Look at the website."
            sender_email = "study.skill@yandex.com"  #  email сервера
            recipient_list = [subscriber.email for subscriber in subscribers]
            send_mail(subject, message, sender_email, recipient_list)
    except Post.DoesNotExist:
        pass


@shared_task
def send_weekly_newsletter():
    # Получение последних новостей (например, за последнюю неделю)
    last_week = timezone.now() - timezone.timedelta(weeks=1)
    latest_news = Post.objects.filter(created_at__gte=last_week, post_type='news')

    # Получение списка всех подписчиков
    subscribers = Subscription.objects.all()

    if subscribers:
        subject = 'Weekly Newsletter'

        for subscriber in subscribers:
            recipient = subscriber.email
            message = 'Here are the latest news from our website:\n\n'

            for news in latest_news:
                message += f"{news.title}\n{news.text}\n\n"

            send_mail(subject, message, 'study.skill@yandex.com', [recipient])



# @shared_task
# def text():
#     print('Hello')]

# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)

# @shared_task
# def complete_order(oid):
#     order=Order.objects.get(pk=oid)
#     order.complete=True
#     order.save()