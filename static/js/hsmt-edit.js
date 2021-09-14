$(document).ready(function () {
    // $('#cardNhanXet').CardWidget('collapse');
    InitXfileData($('#xfileId').val());
    InitXfileContent($('#xfileId').val());
    InitFrontEndForUserGroup();
 });

function InitFrontEndForUserGroup() {
    // Khởi tạo các button send, sendback, edit, ... xfile
    xfileId = $('#xfileId').val()
    $.ajax({
        type: 'GET',
        url: `/api/hsmt/${xfileId}/perm/`,
        success: (resp) => {
            for (perm in resp) {
                if (resp[perm]) {
                    let btn = document.getElementById(`${perm}Btn`);
                    if (btn) btn.hidden = false;
                }
            }
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}

// For init DatetimePicker Input
$('.input-group.date').datetimepicker({
    format:'DD/MM/YYYY'
});


function getAllActiveInputData(){
    var map = {};
    $("textarea[type=text]:enabled").each(function() {
        // map[$(this).attr("id")] = [count,$(this).val()];
        map[$(this).attr("id")] = $(this).val();
    });
    $("input[type=text]:enabled").each(function() {
        // map[$(this).attr("id")] = [count,$(this).val()];
        map[$(this).attr("id")] = $(this).val();
    });
    // var debug='';
    // for (let key in map){
    //     debug+='"'+key+'",';
    // }
    // console.log(debug);
    return map;
}
function SaveXfile(xfileId){
    //btnLuuChiTiet
    tmp=getAllActiveInputData();

    let dataSource={
        'xfileId':xfileId,
        'xfileType':$('#xfileType').val(),
        'values':getAllActiveInputData()
    }
    let data={
        'data':JSON.stringify(dataSource)
    };
    //validation

    //endvalidation
    
    // let x=Object.keys(data).length;
    $.ajax({
        type: 'POST',
        url: '/edit-xfile-detail',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
    .done((resp) => {
        if(resp['status']===0){
            showNotification(msg="Chỉnh sửa thành công",NOTIFICATION_SUCCESS);
        }
        else{
            showNotification(msg=resp['msg'],NOTIFICATION_ERROR,NOTIFICATION_ERROR);
            $('#cardNotDetailDecrypted').show();
            $('#setXfilePassword').attr('onclick',"ConfirmXfilePwd('reConfirm');");
        
        }

    })
    .fail(() => {
        showNotification(msg="Failed",);
    });
}

function displayCalloutTargetType(elementId, data){
    let txt='';
    if (data.length<=0){
        txt='Không có dữ liệu';
    }
    else{
        for (let i in data){
            if (i!=0){
                txt+=',';
            }
            txt+=data[i]['name'];
        }
    }
   
    $('#'+elementId).html('');
    $('#'+elementId).text(txt);
}
function InitXfileData(xfileId,onlyXfileCover=false){
    $.ajax({
        type: 'GET',
        url: `/api/hsmt/${xfileId}/general/`,
        success: (data) => {
            $('#cardBodyXfileCoverLoading').hide();
            $('#cardBodyXfileCover').show();
            $('#btnEditXfile').attr('href','/hsmt/create-edit?id='+data['id']);
                
            let btnDuplicate=$('#btnDuplicate');
            btnDuplicate.html('')
            let tenDoiTuong= 'Mô tả';
            
            $('#tenDoiTuong').text(tenDoiTuong);
            $('#date_created').text(displayDatetime(data['date_created']));
            $('#version').text(data['version']);
            $('#department').text(data.department.name);
            let maSo= '123-56/QD';
            if (data['code'] ){
                maSo=data['code'];
            }
            $('#maSo').text(maSo);
            $('#xfileDescription').text(data['description']);
            $('#nguoiLap').html('')
            $('#nguoiLap').append($('<a>',{href:"/profile?u="+data['creator']['username']}).text(data['creator']['first_name']));
            // Display Targets
            const targets = {1:[], 2:[], 3:[]};
            data['targets'].forEach((target) => {
                targets[target.type].push(target) ;
            });
    
            displayCalloutTargetType('txtTargetDirection',targets[1]);
            displayCalloutTargetType('txtTargetGroup',targets[2]);
            displayCalloutTargetType('txtTargetArea',targets[3]);

            // Display Status
            $('#xfileStatus').html('').append(xfileStatusDisplay(data));
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    })
}

function InitXfileContent(xfileId) {
    $.ajax({
        type: 'GET',
        // url: `/api/hsmt/${xfileId}/content/`,
        url: `/api/hsmt/${xfileId}/general/`,
        success: (data) => {
            // Display Value - Entry
            // let values= JSON.parse(data['content']);
            let values = JSON.parse('{"1. T\u00ean g\u1ecdi v\u00e0 c\u00e1c t\u00ean g\u1ecdi kh\u00e1c": {"type": "string", "value": ""}, "2a. Th\u1eddi gian t\u1ed5 ch\u1ee9c th\u00e0nh l\u1eadp": {"type": "datetime", "value": ""}, "2b. Th\u1eddi gian xu\u1ea5t hi\u1ec7n tr\u00ean KGM": {"type": "datetime", "value": ""}, "3. M\u1ee5c ti\u00eau tr\u00ean m\u1ea1ng": {"type": "string", "value": ""}, "4. N\u1ec1n t\u1ea3ng \u1ee9ng d\u1ee5ng (b\u1ed5 sung)": {"type": "string", "value": ""}, "5. \u0110\u1ecba ch\u1ec9 v\u00e0 s\u1ed1 \u0111i\u1ec7n tho\u1ea1i": {"type": "string", "value": ""}, "6. T\u00f4n ch\u1ec9, m\u1ee5c \u0111\u00edch": {"type": "string", "value": ""}, "7. Qu\u00e1 tr\u00ecnh h\u00ecnh th\u00e0nh, ho\u1ea1t \u0111\u1ed9ng": {"type": "string", "value": ""}, "8. N\u1ed9i dung \u0111\u0103ng t\u1ea3i ch\u1ee7 y\u1ebfu": {"type": "string", "value": ""}}')

            $('#cardNotDetailDecrypted').hide();
            $('#setXfilePassword').attr('onclick',"");
            
            $('#cardDetailDecrypted').show();
            // showNotification(data['msg']);
            let newTag='';
            if (data['original']){
                if (data['history']){
                    newTag='<span class="badge badge-success">Mới</span>';
                }
                else if (data['duplicate']){
                    newTag='<span class="badge badge-success">Thay đổi</span>';
                }
            }
            else{
                if (data['history']){
                    newTag='<span class="badge badge-secondary">Cũ</span>';
                }
                else if (data['duplicate']){
                    newTag='<span class="badge badge-secondary">Thay đổi</span>';
                }
            }
            for (let i in values){
                let tag=$('#'+values[i][0]);
                tag.val(values[i][1]);
                if (values[i][2]){
                    if (tag.parent().find('label').length==0){
                        tag.parent().parent().find('label').append(newTag);
                    }
                    else{
                        tag.parent().find('label').append(newTag);
                    }
                }
            }  
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}


$('#xfile-note-tab').on('click',function(){
   ReloadNotes();
});
$('#xfile-role-tab').on('click',function(){
    //Display Xfile Roles
    InitXfileRole($('#xfileId').val());
 });
 $('#xfile-tracking-tab').on('click',function(){
    //Display Xfile Roles
   ReloadXfileTrackings($('#originalXfileId').val());
});
$('#xfile-update-tab').on('click',function(){
    //Display Xfile Roles
    ReloadXfileUpdates($('#originalXfileId').val());
});


function InitXfileRole(xfileId){
    $.ajax({
        type: 'GET',
        url: `/api/hsmt/${xfileId}/general/`,
        success: (data) => {
            $('#txtEditors').html('');
            for (let i in data['editors']){
                if (i!=0)   {$('#txtEditors').append(', ');}
                $('#txtEditors').append($('<a>',{href:"/profile?u="+data['editors'][i]['username']}).text(data['editors'][i]['first_name']))
            }
            
            $('#txtCheckers').html('');
            for (let i in data['checkers']){
                if (i!=0)   {$('#txtCheckers').append(', ');}
                $('#txtCheckers').append($('<a>',{href:"/profile?u="+data['checkers'][i]['username']}).text(data['checkers'][i]['first_name']))
            }

            $('#txtApprovers').html('');
            for (let i in data['approvers']){
                if (i!=0)   {$('#txtApprovers').append(', ');}
                $('#txtApprovers').append($('<a>',{href:"/profile?u="+data['approvers'][i]['username']}).text(data['approvers'][i]['first_name']))
            }
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
};

function standardDatetime(s){
    // It must be in YYYY-MM-DD HH:MM[:ss 
    s=s.split('/');
    s=s[2] +"-"+s[1] +"-"+s[0] ;
    return s;
}

// function ConfirmXfilePwd(isReConfirm=''){
//     let xfilePassword='';
//     xfilePassword=$('#xfilePassword').val();

//     if (xfilePassword ==''){
//         showNotification("Hãy nhập mật khẩu");
//         return;
//     }
//     $.ajax({
//         type: 'POST',
//         url: '/confirm-dp',
//         headers: {'X-CSRFToken': getCookie('csrftoken')},
//         data: {
//             'dp':xfilePassword,
//             'xfileId':$('#xfileId').val()
//         },
//     })
//         .done((resp) => {
//             if(resp['status']===0){
//                 // Xử lý giao diện
//                 if (isReConfirm == ''){
//                     InitXfileData($('#xfileId').val());
                    
//                 }
//                 else{
//                     $('#cardNotDetailDecrypted').hide();
//                     $('#setXfilePassword').attr('onclick',"")
//                 }
//                 // End - Xử lý giao diện
//                 showNotification(resp["data"],NOTIFICATION_SUCCESS);
//             }
//             else{
//                 showNotification(resp["msg"],NOTIFICATION_ERROR);
    
//             }
//         })
//         .fail(() => {
//             showNotification("Server không phản hồi",NOTIFICATION_ERROR);
//         });
// }

function submit_xfile(xfileId) {
    $.ajax({
        type: 'PUT',
        url: `/api/hsmt/${xfileId}/submit/`,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: (data) => {
            showNotification('Gửi HSMT thành công', 2);
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}

function check_xfile(xfileId) {
    $.ajax({
        type: 'PUT',
        url: `/api/hsmt/${xfileId}/check/`,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: (data) => {
            showNotification('Kiểm định HSMT thành công', 2);
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}

function approve_xfile(xfileId) {
    $.ajax({
        type: 'PUT',
        url: `/api/hsmt/${xfileId}/approve/`,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: (data) => {
            showNotification('Phê duyệt HSMT thành công', 2);
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}

function reject_check_xfile(xfileId) {
    $.ajax({
        type: 'PUT',
        url: `/api/hsmt/${xfileId}/reject-check/`,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: (data) => {
            showNotification('Đã yêu cầu sửa lại HSMT', 2);
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}

function reject_approve_xfile(xfileId) {
    $.ajax({
        type: 'PUT',
        url: `/api/hsmt/${xfileId}/reject-approve/`,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: (data) => {
            showNotification('Đã yêu cầu kiểm định lại HSMT', 2);
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}

function cancel_change_xfile(xfileId) {
    $.ajax({
        type: 'PUT',
        url: `/api/hsmt/${xfileId}/cancel-change/`,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: (data) => {
            showNotification('Đã hủy bản cập nhật HSMT', 2);
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}

function create_change_xfile(xfileId) {
    $.ajax({
        type: 'PUT',
        url: `/api/hsmt/${xfileId}/create-change/`,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        processData: false,
        data: $('#formCreateChangeXFile').serialize(),
        success: (data) => {
            showNotification('Đã tạo bản cập nhật HSMT', 2);
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
}