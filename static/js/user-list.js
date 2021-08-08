
$(document).ready(function () {
   getUsers(false);
});


function getUsers(initial=true){
    $.ajax({
        type: 'GET',
        url: '/get-users',
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                let users=data['users'];
                let owner_group=data['owner_group'];
                // [
                //     {"first_name": "Hoang Trong", "last_login": null, "date_joined": "2021-05-12T02:18:31.409Z", "username": "user3", "is_active": false, "groups": null},
                //     {...},
                // ]
                let displayTableList=[];
                let count=0;
                for (let i in users){
                    let isTP=false;
                    if ( owner_group.includes('Trưởng Phòng')){
                        isTP=true;
                    }
                    count+=1;
                    displayTableList.push(dictUserToList(users[i],isTP,count)); 
                }
                initUserTable(displayTableList,initial);
            }
            else{   
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }
            
        })
        .fail(() => {
            showNotification("Failed");
        });
}
function initUserTable(dataSet,initial=true){
    let tbl=$('#tblUser');
    if (initial==false){
        // Khởi tạo DataTable
        tbl.html('');
        //  All DataString Tables: https://tablepress.org/extensions/change-datatables-strings/
        tbl.DataTable( {
            data: dataSet,
            columns: [
                { title: "#","width": "5%" },
                { title: "Tài khoản" },
                { title: "Họ tên" },
                { title: "Ngày tham gia" },
                { title: "Lần cuối truy cập" },
                { title: "Trạng thái" },
                { title: "","width": "15%" },
                // { title: "Start date" },
                // { title: "Salary" }
            ],
            "language": DATATABLE_LANGUAGE
        } );
    }
    else{
        tbl.dataTable().fnClearTable();
        if (dataSet.length>0){
            tbl.dataTable().fnAddData(dataSet);
        }
    }
    
  
}
//     {"first_name": "Hoang Trong", "last_login": null, "date_joined": "2021-05-12T02:18:31.409Z", "username": "user3", "is_active": false, "groups": null},

function dictUserToList(dict,isTP=false,count){
    let arr=[];
    arr.push( [count ] );
    arr.push( [dict['username'] ] );
    arr.push( [dict['first_name'] ] );
    arr.push( [displayDatetime(dict['date_joined']) ] );
    arr.push( [displayDatetime(dict['last_login']) ] );
    // Display active of user
    // <btn class="btn btn-success ml-3">    <i class="fas fa-check-circle"></i>  </btn>
    // <btn class="btn btn-danger ml-3">   <i class="fas fa-times-circle"></i> </btn>
    let btnActive='';
    if (dict['is_active']==true){
        btnActive='<btn  type="button" class="btn btn-success ml-3" data-toggle="modal" data-target="#modalActivate" data-id="'+dict['id']+'"><span data-toggle="tooltip" data-placement="bottom" title="Bấm để huỷ kích hoạt">  <i class="fas fa-check-circle"></i></span>  </btn>';
    }
    else{
        btnActive='<btn  type="button" class="btn btn-danger ml-3" data-toggle="modal" data-target="#modalActivate" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để kích hoạt"> <i class="fas fa-times-circle"></i> </span> </btn>';
    }
    arr.push( [btnActive] );

    
        // <button type="button" class="btn btn-warning" data-toggle="modal" data-target="#modalAddTargetType" data-id="1" data-type="target-direction">Sửa</button>
        // <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#modalDelete" data-id="1" data-type="target-direction">Xoá</button>
    let btnXem='<a  class="btn btn-info float-right" target="_blank" href="/profile?u='+dict['username']+'" > <span data-toggle="tooltip" data-placement="bottom" title="Xem chi tiết"><i class="fas fa-info-circle"></i></span></a>';
    let btnXoa='';
    if (isTP==true){
        btnXoa='<button type="button" class="btn btn-danger float-right" data-toggle="modal" data-target="#modalDelete" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xoá bản ghi"<i class="fas fa-trash-alt"></i></span></button>'
    }
    // arr.push(btnSua+btnXoa);
    arr.push(btnXoa+btnXem);
    return arr;
}

$('#btnSaveNewUser').on('click',function(){
    var data={
        username:$('#username').val(),
        password:$('#password').val(),
        // phong:$('#phong').val(),
        fullname:$('#fullname').val(),
    };
    $.ajax({
        type: 'POST',
        url: '/register-api',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                getUsers();
                showNotification("Tạo mới thành công",NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });
    
});
function ActivateUser(userId){
    $.ajax({
        type: 'POST',
        url: '/activate-user',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'userId':userId},
    })
        .done((resp) => {
            if(resp['status']===0){
                getUsers();
                showNotification("Kích hoạt/Huỷ kích hoạt thành công",NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });
    
}
function DeleteUser(userId){
    $.ajax({
        type: 'POST',
        url: '/delete-user',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'userId':userId},
    })
        .done((resp) => {
            if(resp['status']===0){
                getUsers();
                showNotification("Xoá người dùng thành công",NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });
    
}
const BTN_ACTIVE_TEXT='Kích hoạt';
const BTN_DEACTIVE_TEXT='Huỷ kích hoạt';
$('#modalActivate').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var userId = button.data('id'); // Extract info from data-* attributes

    let activateUserFunc='ActivateUser("'+userId +'");';
    $('#btnActivateUser').attr('onclick',activateUserFunc);
    let isActive=true;
    if (button.attr('class').includes('btn-danger')){
        isActive=false;
    }
    manageModalActivateUI(isActive);
});
function manageModalActivateUI(isActive){
    let btnActive=$('#btnActivateUser');
    if (isActive==true){
        //ĐAng active ==> Modal Huỷ Active
        btnActive.text(BTN_DEACTIVE_TEXT);
        btnActive.attr("class","btn btn-danger");
        $('#activateModalLabel').text(BTN_DEACTIVE_TEXT.toLowerCase());
        $('#activateModalBody').text(BTN_DEACTIVE_TEXT.toLowerCase());
    }
    else{
        //Vice 
        btnActive.text(BTN_ACTIVE_TEXT);
        btnActive.attr("class","btn btn-success");
        $('#activateModalLabel').text(BTN_ACTIVE_TEXT.toLowerCase());
        $('#activateModalBody').text(BTN_ACTIVE_TEXT.toLowerCase());
    }
}
$('#modalDelete').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var userId = button.data('id'); // Extract info from data-* attributes
    let deleteUserFunc='DeleteUser("'+userId +'");';
    $('#btnDeleteUser').attr('onclick',deleteUserFunc);

});