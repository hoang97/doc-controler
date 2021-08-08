const XFILE_STATUS=[
    [1,'Khởi tạo','secondary','Hồ sơ đang được khởi tạo bởi Trợ lý'],
    [2,'Đang kiểm định','info','Hồ sơ đang trong quá trình kiểm định'],
    [3,'Đang duyệt','warning','Hồ sơ đang chờ duyệt bởi Trưởng phòng'],
    [4,'Hoàn tất','success','Hồ sơ đã được duyệt'],
];

$(document).ready(function () {
    // $('#cardNhanXet').CardWidget('collapse');
    InitXfileData($('#xfileId').val());
    $('textarea').prop('readonly', true);

});


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
        url: '/get-xfile-by-id',
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
                        $('#divRightSideXfileCover').append($('<a>',{class:"btn btn-outline-info btn-sm", href:"/hsmt/detail?id="+data['history']}).append($('<i>',{class:"fas fa-directions"}).text(" Xem bản gốc")));
                    }
                    else  if (data['duplicate']){
                        tenDoiTuong+=" (Bản nháp)";
                        $('#divRightSideXfileCover').append($('<a>',{class:"btn btn-outline-info btn-sm", href:"/hsmt/detail?id="+data['duplicate']}).append($('<i>',{class:"fas fa-directions"}).text(" Xem bản gốc")));
                    }
                }
                
                $('#tenDoiTuong').text(tenDoiTuong);
                $('#date_created').text(displayDatetime(data['date_created']));
                $('#date_modified').text(displayDatetime(data['date_modified']));
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

function getListCheckerId(){
    var data=$('#selectCheckerInModal').select2('data');    
    var ret=[];
    for (let i in data){
        ret.push(data[i]['id']);
    }
    return ret;

}

function InitXfileRole(xfileId){
    $.ajax({
        type: 'POST',
        url: '/get-xfile-user-role',
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
                    if (i!=0)   {$('#txtEditors').append(',');}
                    $('#txtEditors').append($('<a>',{href:"/profile?u="+data['editors'][i]['username']}).text(data['editors'][i]['first_name']))
                }
                $('#txtCheckers').html('');

                for (let i in data['checkers']){
                    if (i!=0)   {$('#txtCheckers').append(',');}
                    $('#txtCheckers').append($('<a>',{href:"/profile?u="+data['checkers'][i]['username']}).text(data['checkers'][i]['first_name']))
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
