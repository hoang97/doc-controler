const XFILE_STATUS=[
    [0,'Khởi tạo','secondary','Hồ sơ đang được khởi tạo bởi Trợ lý'],
    [1,'Đang sửa đổi','info','Hồ sơ đang quá trình sửa đổi'],
    [2,'Đang kiểm định','primary','Hồ sơ đang trong quá trình kiểm định'],
    [3,'Đang duyệt','warning','Hồ sơ đang chờ duyệt bởi Trưởng phòng'],
    [4,'Hoàn tất','success','Hồ sơ đã được duyệt'],
];

$(document).ready(function () {
    // $('#cardNhanXet').CardWidget('collapse');
    InitXfileData($('#xfileId').val());
    InitFrontEndForUserGroup();
 });

function InitFrontEndForUserGroup(){
    let group=$('#template_user_group').val();
    //0:troly,05:checker,1:truongphong
    let xfile_status=$('#template_xfile_status').val();
    //0:closed, 1:init, 2:checking, 3 approving, 4: DONE
    //Button Sửa HSMT
    if (group=='0' && xfile_status=='1' ){
        //Chỉ TroLy mớI đưỢc thực hiện
        $('#btnEditXfile').attr('class','btn btn-outline-info btn-sm');
        $('#btnLuuChiTiet').prop('disabled', false);
        $('#btnThemMoiTracking').show();
        $('#btnThemMoiUpdate').show();
    }
    else {
        $('#btnEditXfile').attr('class','btn btn-outline-info btn-sm disabled');
        $('#btnLuuChiTiet').prop('disabled', true);

    }
    //Button Thêm nhận xét
    if ((group=='1' && xfile_status=='3') ||(group=='05' && xfile_status=='2')) {
        $('#btnAddNote').prop('disabled', false);
    }
    else{
        $('#btnAddNote').prop('disabled', true);
    }
    //Modal Gửi HSMT
    let sendXfileStatus= $('#sendXfileStatus');
    let sendBackXfileStatus=$("#sendBackXfileStatus");
    let bodyPtag=  $('#modalSendXfileErrorPtag');
    let bodyBackPtag=$('#modalSendBackXfileErrorPtag');
    let btnSend=$('#btnSendXfileModal');
    let btnSendBack=$('#btnSendBackXfileModal');
    if (group=='0'){
        $('#btnYeuCauSuaLai').hide();
        $('#btnAddNote').hide();
        if  (xfile_status=='1'){
            $('#divSelectCheckerInModal').show();
            sendXfileStatus.val('11');
        }
        else{
            if (xfile_status== '4'){
                // #HSMT hoan tất 
                $('#btnGuiHSMT').hide();
                $('#btnDuplicate').show();
            }
            bodyPtag.text('Hồ sơ không trong trạng thái cho phép chỉnh sửa');
            btnSend.hide();
        }
    }
    else if(group=='05'){
        btnSend.text('Gửi phê duyệt');
        if ( xfile_status=='2'){
            bodyPtag.text('Xác nhận gửi HSMT cho trưởng phòng  duyệt?');
            bodyBackPtag.text("Yêu cầu chỉnh sửa lại?")

            sendXfileStatus.val('21');
            sendBackXfileStatus.val("20");
        }
        else{
            let tmp='Hồ sơ không trong trạng thái kiểm định!';
            bodyPtag.text(tmp);
            bodyBackPtag.text(tmp);
            btnSend.hide();
            btnSendBack.hide() ;
        }
        
    }
    else if(group=='1'){
        // /Trưởng phòng
        btnSend.text('Duyệt');
        btnSendBack.text('Yêu cầu kiểm định lại');
        if ( xfile_status=='3'){
            bodyPtag.text('Xác nhận duyệt HSMT?');
            bodyBackPtag.text("Yêu cầu kiểm định lại?")
            sendXfileStatus.val('31');
            sendBackXfileStatus.val("30");
        }
        else if ( xfile_status=='4'){
            bodyPtag.text('Hồ sơ không trong trạng thái chờ duyệt!');
            bodyBackPtag.text("Yêu cầu kiểm định lại?")
            sendBackXfileStatus.val("30");
            btnSend.hide();       

        }
        else{
            let tmp='Hồ sơ không trong trạng thái chờ duyệt!';
            bodyPtag.text(tmp);
            bodyBackPtag.text(tmp);    
            btnSend.hide();       
            btnSendBack.hide() ;
        }
        
    }
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

function displayCalloutTargetType(elementId,data){
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
    let data={ 'id':xfileId};
    if (onlyXfileCover==true){
        data['onlyXfileCover']=onlyXfileCover
    }
    $.ajax({
        type: 'GET',
        url: '/get-xfile-by-id/',
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                
                $('#cardBodyXfileCoverLoading').hide();
                $('#cardBodyXfileCover').show();
                 // {    
                    // "id":"1"
                $('#btnEditXfile').attr('href','/hsmt/create-edit?id='+data['id']);
                //     "name": "das",
                //      "date_created": "2021-05-10T13:39:12.446Z", 
                //      "date_modified": null,
                //       "edit_note": null, 
                //       "status": 1,
                    //   "values": [
                    //       ["hoVaTen", "hehe"],
                    //     ["queQuan", "hehe"]
                    //     ]
                //         "targetTypes": {
                //             "target-direction": [{"id": 2, "name": "testt", "description": ""}],
                //             "target-group": [{"id": 2, "name": "das", "description": "das"}], 
                //             "target-area": [{"id": 1, "name": "test33", "description": ""}]
                //         }
                // }            
                let btnDuplicate=$('#btnDuplicate');
                btnDuplicate.html('')
                let tenDoiTuong=data['name'];
                if (data['original']){
                      if (data['duplicate']){
                        btnDuplicate.attr('onclick',"CreateDuplicate("+data['duplicate']+");");
                        btnDuplicate.append($('<i>',{class:"far fa-copy"})).append(" Xem bản nháp");
                    }
                    else{
                        btnDuplicate.attr({'data-toggle':"modal", 'data-target':"#modalCreateDuplicate"});
                        btnDuplicate.append($('<i>',{class:"far fa-copy"})).append(" Tạo bản nháp");
                    }
                }
                else{
                    $('#divRightSideXfileCover').html('');
                    if (data['history']){
                        btnDuplicate.hide();
                        tenDoiTuong+=" (Bản cũ gần nhất)";
                        $('#divRightSideXfileCover').append($('<a>',{class:"btn btn-outline-info btn-sm", href:"/hsmt/edit-detail?id="+data['history']}).append($('<i>',{class:"fas fa-directions"}).text(" Xem bản gốc")));
                    }
                    else  if (data['duplicate']){
                        tenDoiTuong+=" (Bản nháp)";
                        $('#divRightSideXfileCover').append($('<a>',{class:"btn btn-outline-info btn-sm", href:"/hsmt/edit-detail?id="+data['duplicate']}).append($('<i>',{class:"fas fa-directions"}).text(" Xem bản gốc")));
                    }
                }

                $('#tenDoiTuong').text(tenDoiTuong);
                $('#date_created').text(displayDatetime(data['date_created']));
                $('#version').text(data['version']);
                $('#department').text(data['department']);
                let maSo= '123-56/QD';
                if (data['code'] ){
                    maSo=data['code'];
                }
                $('#maSo').text(maSo);
                $('#xfileDescription').text(data['description']);
                $('#nguoiLap').html('')
                $('#nguoiLap').append($('<a>',{href:"/profile?u="+data['user']['username']}).text(data['user']['first_name']));
                // Display Target Types
                let targetTypes=data['targetTypes'];
     
                displayCalloutTargetType('txtTargetDirection',targetTypes['target-direction']);
                displayCalloutTargetType('txtTargetGroup',targetTypes['target-group']);
                displayCalloutTargetType('txtTargetArea',targetTypes['target-area']);

                // Display Status
                $('#xfileStatus').html('');
                for (let i in XFILE_STATUS){
                    if (XFILE_STATUS[i][0]==data['status']){
                        let spanTag='<span class="text-md badge badge-'+XFILE_STATUS[i][2]+'"  data-toggle="tooltip" data-placement="bottom" title="'+XFILE_STATUS[i][3]+'">'+XFILE_STATUS[i][1]+'</span>';
                        $('#xfileStatus').append(spanTag);
                        break;
                    }
                }
               
                // Display Value - Entry
                if (onlyXfileCover==false){
                    let values=data['values'];
                    if (data['isDecrypted']){

                        $('#cardNotDetailDecrypted').hide();
                        $('#setXfilePassword').attr('onclick',"");
                        
                        $('#cardDetailDecrypted').show();
                        showNotification(data['msg']);
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
                    }
                    else{
                        $('#cardNotDetailDecrypted').show();
                        $('#setXfilePassword').attr('onclick',"ConfirmXfilePwd();");
                        $('#cardDetailDecrypted').hide();
                        showNotification(data['msg']);
                    }   
                }
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }
        })
        .fail(() => {
            showNotification("Server không phản hồi",NOTIFICATION_ERROR);
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



$('#modalSendXfile').on('show.bs.modal', function (event) {
    if ($('#sendXfileStatus').val()=='11'){

        $.ajax({
            type: 'POST',
            url: '/get-xfile-user-role',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
    
            data: {
                'xfileId':$('#xfileId').val(),
                'fetchAllUsers':'1'
            },
        })
            .done((resp) => {
                if(resp['status']===0){
                    let data=resp['data'];
                    let allUsers=data['allUsers'];
                    let checkers=data['checkers'];
                    let count=0;
                    let selectElement=$('#selectCheckerInModal');
                    selectElement.html('');
                    for (let i=0;i<allUsers.length;i++){
                        let flag=false;
                        for (let j=0;j<data['editors'].length;j++){
                            if (allUsers[i]['id']==data['editors'][j]['id']){
                                // Loại bỏ các user  CREATOR và EDITOR
                                flag=true;
                                data['editors'].splice(j, 1); 
                                break;
                            }
                        }
                        if (flag==true){continue;}
                        count+=1;
                        let isSelected=false;
                        for (let j in checkers){
                            if (allUsers[i]['id']==checkers[j]['id']){
                                isSelected=true;
                                checkers.splice(j, 1); 
                                break;
                            }
                        }
                        let newOption = new Option(allUsers[i]['first_name'], allUsers[i]['id'], false, isSelected);
                        selectElement.append(newOption).trigger('change');
                    }
                
                    showNotification("Lấy được "+count+" người dùng cùng phòng");
    
                }
                else{
                    showNotification(resp['msg'],NOTIFICATION_ERROR);
                }
        
            })
            .fail(() => {
                showNotification("Server không phản hồi",NOTIFICATION_ERROR);
            });
    }
   
});
function getListCheckerId(){
    var data=$('#selectCheckerInModal').select2('data');    
    var ret=[];
    for (let i in data){
        ret.push(data[i]['id']);
    }
    return ret;

}
function SendXfile(type='forward'){
    var xfileId=$('#xfileId').val();
    
    var newStatus =$('#sendXfileStatus').val();
    if (type!='forward'){
        newStatus =$('#sendBackXfileStatus').val();
    }
    if (newStatus==""){
        return;
    }
    var data={
        'xfileId':xfileId,
        'new-status':newStatus,
    }
    if (newStatus=='11'){
        // Only Troly send to CHecker
        var listChecker=getListCheckerId();
        data['listChecker']=JSON.stringify(listChecker);
    }

    $.ajax({
        type: 'POST',
        url: '/send-xfile',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                if (resp['data']['new-xfile-id'] !=''){
                    window.location.href="/hsmt/edit-detail?id="+resp['data']['new-xfile-id'];
                    return;
                }
                InitXfileData(xfileId,true);
                let new_xfile_status='1';
                // ''' 10= CLOSED, 11= to Checker, 20 = back Editor, 21= to Approver, 30=back Checker, 31 = DONE '''
                // INIT=1, CHECKNG=2, APPROING=3, DONE=4
                switch(newStatus) {
                    case '11':
                        new_xfile_status='2';
                      break;
                    case '20':
                        new_xfile_status='1';
                      break;
                    case '21':
                        new_xfile_status='3';
                      break;
                    case '30':
                        new_xfile_status='2';
                      break;
                    case '31':
                        new_xfile_status='4';
                      break;
                    default:
                        new_xfile_status='1';
                  }
                $('#template_xfile_status').val(new_xfile_status);
                InitFrontEndForUserGroup();
                showNotification(resp['data']['msg']);
                $('#modalSendXfile').modal('hide');
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }
    
        })
        .fail(() => {
            showNotification("Server không phản hồi",NOTIFICATION_ERROR);
        });

};
function InitXfileRole(xfileId){
    $.ajax({
        type: 'POST',
        url: '/get-xfile-user-role/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {
            'xfileId':xfileId,
        }
    })
        .done((resp) => {

            if(resp['status']===0){
                let data=resp['data'];
                // dataEditors.push({'id':data['creator']['id'],'text':data['creator']['first_name']})
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
  
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }
    
        })
        .fail(() => {
            showNotification("Server không phản hồi",NOTIFICATION_ERROR);
        });
};

function standardDatetime(s){
    // It must be in YYYY-MM-DD HH:MM[:ss 
    s=s.split('/');
    s=s[2] +"-"+s[1] +"-"+s[0] ;
    return s;
}

function ConfirmXfilePwd(isReConfirm=''){
    let xfilePassword='';
    xfilePassword=$('#xfilePassword').val();

    if (xfilePassword ==''){
        showNotification("Hãy nhập mật khẩu");
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/confirm-dp',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {
            'dp':xfilePassword,
            'xfileId':$('#xfileId').val()
        },
    })
        .done((resp) => {
            if(resp['status']===0){
                // Xử lý giao diện
                if (isReConfirm == ''){
                    InitXfileData($('#xfileId').val());
                    
                }
                else{
                    $('#cardNotDetailDecrypted').hide();
                    $('#setXfilePassword').attr('onclick',"")
                }
                // End - Xử lý giao diện
                showNotification(resp["data"],NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp["msg"],NOTIFICATION_ERROR);
    
            }
        })
        .fail(() => {
            showNotification("Server không phản hồi",NOTIFICATION_ERROR);
        });
}
function CreateDuplicate(redirect=''){
    if (redirect!=''){
        window.location.href='/hsmt/edit-detail?id='+redirect;
        return;
    }
    let xfileId= $('#xfileId').val();
    $.ajax({
        type: 'POST',
        url: '/create-xfile-duplicate',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'xfileId':xfileId},
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                showNotification(data["msg"],NOTIFICATION_SUCCESS);
                let newId=data['new-xfile-id'];
                window.location.href='/hsmt/edit-detail?id='+newId;
            }
            else{
                showNotification(resp["msg"],NOTIFICATION_ERROR);
    
            }
        })
        .fail(() => {
            showNotification("Server không phản hồi",NOTIFICATION_ERROR);
        });
}