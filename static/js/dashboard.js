
const autoRefreshTime=60;//seconds
var unRead=0;

$(document).ready(function () {

  getNotifications();
  setInterval(getNotifications, autoRefreshTime * 1000);
});

var lastId=0;
function getNotifications(){
    $.ajax({
        type: 'GET',
        url: '/get-notifications',
        data:{'lastId':lastId}
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                if (data.length <=0){
                  return;
                }
                lastId=data[0]['id'];
                
                reloadNotification(data);
            }
            else{   
            }
            
        })
        .fail(() => {
            
        });

}   
function reloadNotification(dataSet){

    var notifyBox=$('#notificationBox');
    notifyBox.html('');
    notifyBox.append($('<a>',{href:"/profile?u="+$('#request-username').val()+'#tab=2', class:"dropdown-item dropdown-footer text-info text-bold"}).append($('<i>',{class:"far fa-bell"})).append(" Thông báo"));
    for (let i=0;i<dataSet.length;i++){
      let oneNotify=dataSet[i];
       // "content":notify.content,
          // "action_time":notify.log.action_time,
          // "content_type_id":notify.log.content_type_id,
          // "object_id":notify.log.object_id,
       let linkObj='/hsmt/edit-detail?id='+oneNotify['object_id'];
       if (oneNotify['read']==true){oneNotify["id"]='0';}
       let newRow=$('<div>',{class:"dropdown-item",onclick:'ReadNotification('+oneNotify["id"]+',"'+linkObj+'");'});
       
       let img=$('<img>',{src:"/static/img/avatar5.png",alt:"User Avatar" ,class:"img-size-50 mr-3 img-circle"});
       let body=$('<div>',{class:"media-body"});
      //  body.append($('<h3>',{class:"dropdown-item-title"}).text(oneNotify['actor_name']));
      let contentTag=$('<p>',{class:"text-sm"}).text(oneNotify['content']);
      if (oneNotify['read']==false){
        unRead+=1;
        contentTag.append($('<i>',{class:"fas fa-circle float-right text-info"}));
       }
       body.append(contentTag);
       
       
       body.append($('<p>',{class:"text-sm text-muted"}).append($('<i>',{class:"far fa-clock mr-1"})).append(displayDatetime(oneNotify['action_time'],'long')));
       
       newRow.append($('<div>',{class:"media"}).append(img).append(body));
       newRow.append('<div class="dropdown-divider"></div>');
       // Finally
       notifyBox.append(newRow);
    }
    //last butto
    $('#notificationBoxBadge').text(unRead.toString());

    notifyBox.append($('<a>',{href:"/profile?u="+$('#request-username').val()+'#tab=2', class:"dropdown-item dropdown-footer text-info text-bold"}).append($('<i>',{class:"fas fa-share"})).append(" Xem tất cả"));
};

function ReadNotification(id,redirectLink=''){
  if (id.toString()!='0'){
      $.ajax({
        type: 'GET',
        url: '/read-notification',
        data:{'id':id}
      });
  }
  if (redirectLink!=''){
    window.location.href=redirectLink;
  }
  
}
