
$(document).ready(function () {
    getNotifications()
        .then(data => {
            reloadNotification(data);
        });
});

function seenNotification(notification_id) {
    // send 'seen' signal to websocket
    notificationSocket.send(JSON.stringify({
        action_type: 'seen.notification',
        notification_id: notification_id
    }));
}

function deleteNotification(notification_id) {
    // send 'delete' signal to websocket
    notificationSocket.send(JSON.stringify({
        action_type: 'delete.notification',
        notification_id: notification_id
    }));
}

const update_num_notification = (x) =>{
    let numNotifications = document.querySelector('#notificationBoxBadge');
    let num = +numNotifications.innerText;
    num += x;
    numNotifications.innerText = num;
    numNotifications.hidden = (num == 0);
};

function createOneNotification(data) {
    let seen = +!data['seen'];
    let notifyBox=$('#notificationBox');
    let newRow=$('<div>',{class:"dropdown-item"});
    
    let img=$('<img>',{src:"/static/img/avatar5.png",alt:"User Avatar" ,class:"img-size-50 mr-3 img-circle"});
    let body=$('<div>',{class:"media-body"});
    let contentTag=$('<p>',{class:"text-sm", id:data['notification_id']}).text(data['message']);
    // unseen notification has bold text
    if (data['seen']==false){
        contentTag[0].classList.add('text-bold')
    };
    body.append(contentTag);
    body.append($('<p>',{class:"text-sm text-muted"}).append($('<i>',{class:"far fa-clock mr-1"})).append(displayDatetime(data['timestamp'],'long')));
    newRow.append($('<div>',{class:"media"}).append(img).append(body));
    newRow.append('<div class="dropdown-divider"></div>');

    newRow[0].onclick = (e) => {
        // redirect to target_url when click
        seenNotification();
        window.location.href=data['target_url'];
    };
    notifyBox.append(newRow)
    update_num_notification(seen);
};

function reloadNotification(data){
    // create new notification box
    let notifyBox=$('#notificationBox');
    notifyBox.html('');
    notifyBox.append($('<a>',{href:"/profile?u="+$('#request-username').val()+'#tab=2', class:"dropdown-item dropdown-footer text-info text-bold"}).append($('<i>',{class:"far fa-bell"})).append(" Thông báo"));

    // Create 1 row for each notification
    for (let i in data['notifications']){
        createOneNotification(data['notifications'][i]);
    };

    notifyBox.append($('<a>',{href:"/profile?u="+$('#request-username').val()+'#tab=2', class:"dropdown-item dropdown-footer text-info text-bold"}).append($('<i>',{class:"fas fa-share"})).append(" Xem tất cả"));

    // update the real number of notifications
    let numNotifications = document.querySelector('#notificationBoxBadge');
    numNotifications.innerText = data['num'];
    update_num_notification(0);
};

notificationSocket.onopen = (e) =>{
    console.log('Notification Socket opened')
};

notificationSocket.onclose = (e) => {
    console.error('Notification Socket closed unexpectedly');
};

async function getData(url) {
    // fetch data from url
    const response = await fetch(url);
    return response.json(); // parses JSON response into native JavaScript objects
};

function getNotifications() {
    // get the last 3 notifications of current user
    return getData(notification_url)
};

function getAllNotifications() {
    // get all notifications of current user
    return getData(notification_url+'?all=true')
}

notificationSocket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    console.log(data['message_type']+ ' notification');
    
    getNotifications()
        .then(data => {
            reloadNotification(data);
        })
};
