
$('#btnChangePassword').on('click',function(){
    
    let oldPassword = $('#oldPassword').val();
    let newPassword = $('#newPassword').val();
    let reNewPassowrd = $('#reNewPassowrd').val();
    if (newPassword.length < 8 || reNewPassowrd.length <8){
        showNotification('Mật khẩu mới  phải lớn hơn 8 ký tự',NOTIFICATION_ERROR);
        return;
    }
    if (reNewPassowrd != newPassword) {
        showNotification('Mật khẩu không khớp',NOTIFICATION_ERROR);
        return;
    }

    $.ajax({
        type: 'POST',
        url: '/change-dp',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: { 
            'oldPassword': oldPassword,
            'newPassword': newPassword
         }
    })
        .done(resp => {
            if (resp['status']===0) {
                showNotification(resp['data'],"Đổi mật khẩu thành công");
            } 
            else {
                showNotification(resp['msg'],NOTIFICATION_ERROR);
                // $('#oldPassword').val('');
                // $('#newPassword').val('');
                // $('#reNewPassowrd').val('');
            }
        })
        .fail(() => {
            showNotification("Không thể đổi mật khẩu",NOTIFICATION_ERROR);
        });
});
