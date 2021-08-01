from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
@login_required
def index(request):
    return render(request, 'notifications/test.html')

@login_required
def get_notifications(request):
    data = {}
    notification_objs = request.user.notification_set.select_related('log')
    data['num'] = notification_objs.filter(seen=False).count()
    notifications = {}
    for notification in notification_objs.order_by('-log__timestamp')[:3:-1]:
        notifications[str(notification.id)] = {
            'seen': notification.seen,
            'message': str(notification.log),
            'timestamp': datetime.strftime(notification.log.timestamp, '%b %d, %Y, %I:%M %p'),
            'target_url': notification.log.get_target_url(),
            'notification_id': notification.id
        }
    data['notifications'] = notifications
    return JsonResponse(data)