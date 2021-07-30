from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, 'notifications/test.html')

@login_required
def get_notifications(request):
    data = {}
    data['num'] = request.user.notification_set.filter(seen=False).count()
    notifications = {}
    for notification in request.user.notification_set.all().order_by('-log__timestamp')[:3:-1]:
        notifications[str(notification.id)] = {
            'seen': notification.seen,
            'message': str(notification.log),
            'timestamp': str(notification.log.timestamp),
            'target_url': notification.log.get_target_url(),
            'notification_id': notification.id
        }
    data['notifications'] = notifications
    return JsonResponse(data)