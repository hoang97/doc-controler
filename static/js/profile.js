$(document).ready(function () {
    showProfileNotificationTab();
 });

function showProfileNotificationTab(){
    var url = window.location.href;
    if (!url.includes('#tab=2')){
        return;
    }
    $('#profile-notification-tab').trigger('click');
    
}
$('#btnChangePassword').on('click',function(){
    let oldPwd=$('#oldPassword').val();
    let newPwd=$('#newPassword').val();
    let reNewPwd=$('#reNewPassowrd').val();
    if (newPwd!=reNewPwd){
        showNotification('Mật khẩu mới không hớp',NOTIFICATION_ERROR);
        return;

    }
    let data={
        'oldPwd':oldPwd,
        'newPwd':newPwd
    }
    $.ajax({
        type: 'POST',
        url: '/change-password/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                showNotification("Đổi mật khẩu thành công",NOTIFICATION_SUCCESS);
                window.location.href='/';
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }
        })
        .fail(() => {
            showNotification("Failed");
        });
    
});

$('#profile-notification-tab').on('click',function(){
    reloadTabNotifications();
});
function reloadTabNotifications(){
    getAllNotifications()
        .then(data => {
            let tabNotify=$('#profile-notification');
            tabNotify.html('');
            for (let i=0;i<data['notifications'].length;i++){
                let onePost=displayOneNotify(data['notifications'][i]);
                tabNotify.append(onePost);
            } 
        })
        .catch(err => {
            showNotification('Server không phản hồi',NOTIFICATION_ERROR);
        })
}
function displayOneNotify(data){
    let postDiv=$('<div>',{class:"post"});
    let userBlockDiv=$('<div>',{class:"user-block"});
    let spanUsername=$('<span>',{class:"username"});
    spanUsername.append($('<a>',{href:data['actor_url']}).text(data['actor_name']));
    spanUsername.append($('<span>',{onclick:"deleteNotification("+data['notification_id']+");",class:"float-right btn-tool",'data-toggle':"tooltip", 'data-placement':"bottom", title:"Xoá thông báo này"}).append($('<i>',{class:"fas fa-times"})));
    spanUsername.append($('<span>',{onclick:"seenNotification("+data['notification_id']+");" ,class:"float-right btn-tool",'data-toggle':"tooltip", 'data-placement':"bottom", title:"Đánh dấu đã đọc"}).append($('<i>',{class:"fas fa-book-reader"})));
    if (!data['seen']){
        spanUsername.append($('<span>',{class:"float-right bg-info btn-tool "}).text("Mới"));
    }
    let spanTime=$('<span>',{class:"description"}).text(displayDatetime(data['timestamp'],'long') );

    userBlockDiv.append($('<img>',{class:"img-circle img-bordered-sm", src:"/static/img/avatar5.png", alt:"user image"}));
    userBlockDiv.append(spanUsername);
    userBlockDiv.append(spanTime);
    // #Nén data
    postDiv.append(userBlockDiv);
    postDiv.append($('<p>').text(data['message']));
    return postDiv;
}

notificationSocket.onmessage = (function() {
    // advance JS to extend function 'onmessage'
    var cached_func = notificationSocket.onmessage
    return function(e) {
        cached_func.apply(this, arguments);
        let data = JSON.parse(e.data);
        reloadTabNotifications(data);
    };
}());