from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.urls import reverse

# Create your views here.
@login_required
def index(request):
    return render(request, 'notifications/test.html')

@login_required
def get_notifications(request):
    all = request.GET.get('all', '')
    data = {}
    notification_objs = request.user.notification_set.select_related('log')
    data['num'] = notification_objs.filter(seen=False).count()
    if all:
        query = notification_objs.order_by('-log__timestamp')
    else:
        query = notification_objs.order_by('-log__timestamp')[:3]
    notifications = []
    for notification in query:
        actor_url = reverse('user-profile') + f'?u={notification.recipient.username}'
        target_url = reverse('hsmt-detail', args=[notification.log.target_id])
        notifications.append({
            'seen': notification.seen,
            'message': str(notification.log),
            'timestamp': datetime.strftime(notification.log.timestamp, '%b %d, %Y, %I:%M %p'),
            'actor_url': actor_url,
            'target_url': target_url,
            'notification_id': notification.id,
            'actor_name': notification.log.actor.first_name,
            'actor_username': notification.log.actor.username,
            
        })
    data['notifications'] = notifications
    return JsonResponse(data)