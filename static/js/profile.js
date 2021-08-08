

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
        url: '/change-password',
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
    $.ajax({
        type: 'GET',
        url: '/get-notifications',
        data:{
            'all':true
        }
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                let tabNotify=$('#profile-notification');
                tabNotify.html('');
                for (let i=0;i<data.length;i++){
                    let onePost=displayOneNotify(data[i]);
                    tabNotify.append(onePost);
                }
            }
            else{   
            }
            
        })
        .fail(() => {
            
        });



    
}
function displayOneNotify(data){
//     <div class="post">
//     <div class="user-block">
//       <img class="img-circle img-bordered-sm" src="{% static 'img/avatar5.png' %}" alt="user image">
//       <span class="username">
//         <a href="#">Jonathan Burke Jr.</a>
//         <a href="#" class="float-right btn-tool"><i class="fas fa-times"></i></a>
//         <a href="#" class="float-right btn-tool" data-toggle="tooltip" data-placement="bottom" title="Đánh dấu đã đọc"><i class="fas fa-book-reader"></i></a>
//       </span>
//       <span class="description">Shared publicly - 7:30 PM today</span>
//     </div>
//     <!-- /.user-block -->
//     <p>
//       Lorem ips
//     </p>
//   </div>
    let postDiv=$('<div>',{class:"post"});
    let userBlockDiv=$('<div>',{class:"user-block"});
    let spanUsername=$('<span>',{class:"username"});
    spanUsername.append($('<a>',{href:"/profile?u="+data['actor_username']}).text(data['actor_name']));
    spanUsername.append($('<span>',{onclick:"DeleteNotificationInProfile("+data['id']+");",class:"float-right btn-tool",'data-toggle':"tooltip", 'data-placement':"bottom", title:"Xoá thông báo này"}).append($('<i>',{class:"fas fa-times"})));
    spanUsername.append($('<span>',{onclick:"ReadNotificationInProfile("+data['id']+");" ,class:"float-right btn-tool",'data-toggle':"tooltip", 'data-placement':"bottom", title:"Đánh dấu đã đọc"}).append($('<i>',{class:"fas fa-book-reader"})));
    if (!data['read']){
        spanUsername.append($('<span>',{class:"float-right bg-info btn-tool "}).text("Mới"));
    }
    let spanTime=$('<span>',{class:"description"}).text(displayDatetime(data['action_time'],'long') );

    userBlockDiv.append($('<img>',{class:"img-circle img-bordered-sm", src:"/static/img/avatar5.png", alt:"user image"}));
    userBlockDiv.append(spanUsername);
    userBlockDiv.append(spanTime);
    // #Nén data
    postDiv.append(userBlockDiv);
    postDiv.append($('<p>').text(data['content']));
    return postDiv;
}
function ReadNotificationInProfile(id){
    if (id.toString()!='0'){
        $.ajax({
          type: 'GET',
          url: '/read-notification',
          data:{'id':id}
        })
        .done((resp) => {
            if(resp['status']===0){
                showNotification(resp['data'],NOTIFICATION_SUCCESS);
                reloadTabNotifications();
            }
            else{   
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }
            
        })
        .fail(() => {
            showNotification('Server không phản hồi',NOTIFICATION_ERROR);
        });
    }
}
function DeleteNotificationInProfile(id){
    if (id.toString()!='0'){
        $.ajax({
          type: 'GET',
          url: '/delete-notification',
          data:{'id':id}
        })
        .done((resp) => {
            if(resp['status']===0){
                showNotification(resp['data'],NOTIFICATION_SUCCESS);
                reloadTabNotifications();
            }
            else{   
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }
            
        })
        .fail(() => {
            showNotification('Server không phản hồi',NOTIFICATION_ERROR);
        });
    }
}

