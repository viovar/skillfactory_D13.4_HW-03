# from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Post, PostCategory, Subscription


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)



# @receiver(post_save, sender=Post)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новая статья в категории {instance.category}'
#
#     text_content = (
#         # f'Товар: {instance.name}\n'
#         # f'Цена: {instance.price}\n\n'
#         f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         # f'Товар: {instance.name}<br>'
#         # f'Цена: {instance.price}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на статью</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()