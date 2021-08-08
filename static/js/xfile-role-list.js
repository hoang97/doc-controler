
const XFILE_TYPES=[
    [1,'TM'],
    [2,'TC'],
    [3,'ĐT']
];
const XFILE_STATUS=[
    [1,'Khởi tạo','secondary','Hồ sơ đang được khởi tạo bởi Trợ lý'],
    [2,'Đang kiểm định','info','Hồ sơ đang trong quá trình kiểm định'],
    [3,'Đang duyệt','warning','Hồ sơ đang chờ duyệt bởi Trưởng phòng'],
    [4,'Hoàn tất','success','Hồ sơ đã được duyệt'],
];

$(document).ready(function () {
    getXfileRoles(true);
});



function getlistIdFromSelect2(elementId){
    var data=$('#'+elementId).select2('data');    
    var ret=[];
    for (let i in data){
        ret.push(data[i]['id']);
    }
    return ret;

}
$( "#btnSave" ).on( "click", function() {
    // Validation
    var listCheckerId=getlistIdFromSelect2('selectChecker');
    var listEditorId=getlistIdFromSelect2('selectEditor');


    let data={
        'xfileId':$('#xfileId').val(),
        'listCheckerId':listCheckerId,
        'listEditorId':listEditorId
    }

    $.ajax({
        type: 'POST',
        url: '/set-xfile-role',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'data':JSON.stringify(data)},
    })
        .done((resp) => {
            if(resp['status']===0){

                getXfileRoles();
                $('#modalEditXfileRole').modal('hide');
                showNotification("Done");

            }
            else{
                showNotification(resp['msg']);
                $('#modalEditXfileRole').modal('hide');
            }
    
        })
        .fail(() => {
            showNotification("Failed");
        });

});

$('#modalEditXfileRole').on('show.bs.modal', function (event) {
    // $('#cardNhatKy').hide();
    var button = $(event.relatedTarget); // Button that triggered the modal
    var xfileId = button.data('xfile-id'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn
    $('#xfileId').val(xfileId);
    if(xfileId!='' || xfileId != undefined){
        // Có dữ liệu --> Get dữ liệu để chỉnh sửa
            $.ajax({
                type: 'POST',
                url: '/get-xfile-user-role',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                data: {
                    'xfileId':xfileId,
                    'fetchAllUsers':'1'
                },
            })
                .done((resp) => {
                    if(resp['status']===0){
                        let data=resp['data'];
                        let allUsers=data['allUsers'];
                        let checkers=data['checkers'];
                        let editors=data['editors'];

                        let selectCheckerElement=$('#selectChecker');
                        let selectEditorElement=$('#selectEditor');

                        selectCheckerElement.html('');
                        selectEditorElement.html('');

                        for (let i=0;i<allUsers.length;i++){
                            let isEditor=false;
                            let isChecker=false;

                            //Viết dữ liêu jvaof SelectEditor
                            for (let j in editors){
                                if (allUsers[i]['id']==editors[j]['id']){
                                    // Viết dữ liêu  SelectEditor
                                    //Hàm kiểm soát
                                    isEditor=true;
                                    editors.splice(j, 1); 
                                    break;
                                }
                            }
                            // Viết dữ liệu vào Select Checker
                            if (isEditor==false){
                                // Nếu đã là Editor ==> Không cầN kiểm tra Checker
                                for (let j in checkers){
                                    if (allUsers[i]['id']==checkers[j]['id']){
    
                                        //Hàm kiểm soát
                                        isChecker=true;
                                        checkers.splice(j, 1); 
                                        break;
                                    }
                                }
                            }
                           
                            if (isEditor==true){

                                let newOption = new Option(allUsers[i]['first_name'], allUsers[i]['id'], false, true);
                                selectEditorElement.append(newOption).trigger('change');
                            }
                            else if (isChecker==true){

                                let newOption = new Option(allUsers[i]['first_name'], allUsers[i]['id'], false, true);
                                selectCheckerElement.append(newOption).trigger('change');
                            }
                            else {
                                let newOption1 = new Option(allUsers[i]['first_name'], allUsers[i]['id'], false, false);
                                let newOption2 = new Option(allUsers[i]['first_name'], allUsers[i]['id'], false, false);


                                selectCheckerElement.append(newOption1).trigger('change');
                                selectEditorElement.append(newOption2).trigger('change');
                            }
                            
                        }
                        }
                    else{
                        showNotification("Lỗi status");
                    }
                    
                    
                })
                .fail(() => {
                    showNotification("Failed");
                });
    }
    else{

    }
});

function getXfileRoles(initial=false){
    $.ajax({
        type: 'GET',
        url: '/get-xfile-roles',
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];

                let displayTableList=[];
                let count=0;
                for (let i in data){
                    count+=1;
                    displayTableList.push(dictToList(data[i],count));
                }
                initTable(displayTableList,initial);
            }
            else{   
                showNotification("Lỗi status");
            }
            
        })
        .fail(() => {
            showNotification("Failed");
        });

}   



function initTable(dataSet,initial=false){
    if(initial==true){
        $('#tblXfileRole').html('');
        $('#tblXfileRole').DataTable({
            data: dataSet,
            columns: [
                { title: "#","width": "5%" },
                { title: "Tên hồ sơ"},
                { title: "Kiểu hồ sơ"},
                { title: "Ngày tạo" },
                { title: "Người chỉnh sửa" ,"width": "15%"},

                { title: "Người kiểm định","width": "15%" },
                { title: "Trạng thái"},

                { title: "","width": "10%" },

            ],    
            "language": DATATABLE_LANGUAGE
        } );
    }
    else{
        $('#tblXfileRole').dataTable().fnClearTable();
        $('#tblXfileRole').dataTable().fnAddData(dataSet);
    }


}

function dictToList(dict,count){
// [
//     {"id": 11,
//      "xfile_type": 1, 
//      "name": 'tm', 
//      "date_created": "2021-05-19T03:35:12.244Z", 
//      "date_modified": null, "status": 2, 
//      "creator": 
//             {"id": 12, "first_name": "trunog phong 2", "username": "tp2", "is_active": true}, 
//      "editors": [], 
//      "checkers": [], 
//      "allUsers": 
//      [
//          {"id": 7, "first_name": "Hoang Trong", "username": "user3", "is_active": false}, 
//          {"id": 5, "first_name": "Kim 2", "username": "user2", "is_active": true}
//     ]
//     }, 
// ]
    let arr=[];
    arr.push( [count ] );
    let nameATag='<a target="_blank" href="/hsmt/edit-detail?id='+dict['id']+'">'+dict['name']+' </a>'
    arr.push( [ nameATag] );

    for (let i in XFILE_TYPES){
        if (XFILE_TYPES[i][0]==dict['xfile_type']){
            arr.push([XFILE_TYPES[i][1]]);
            break;
        }
    }
    


    // arr.push( ([dict['xfile_id'] ]) );

    arr.push( displayDatetime([dict['date_created'] ]) );
    // arr.push( [dict['creator']['first_name']] );
    //Column Editor

    let txtEditors='';
    let txtCheckers='';
    for (let i in dict['editors']){
        if (i!=0)   {txtEditors+=',';}
        txtEditors+='<a href="/profile?u='+dict['editors'][i]['username']+'"> '+dict['editors'][i]['first_name']+'</a>';
    }


    for (let i in dict['checkers']){
        if (i!=0)   {txtCheckers+=',';}
        txtCheckers+='<a href="/profile?u='+dict['checkers'][i]['username']+'"> '+dict['checkers'][i]['first_name']+'</a>';

    }
    arr.push( [txtEditors] );

    arr.push( [txtCheckers] );
    for (let i in XFILE_STATUS){
        if (XFILE_STATUS[i][0]==dict['status']){
            let spanTag='<span class="btn btn-'+XFILE_STATUS[i][2]+'"  data-toggle="tooltip" data-placement="bottom" title="'+XFILE_STATUS[i][3]+'">'+XFILE_STATUS[i][1]+'</span>';
            arr.push([spanTag]);
            break;
        }
    }
    // arr.push( displayDatetime([dict['date_modified'] ]) );
        // <button type="button" class="btn btn-warning" data-toggle="modal" data-target="#modalAddTargetType" data-id="1" data-type="target-direction">Sửa</button>
        // <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#modalDelete" data-id="1" data-type="target-direction">Xoá</button>
    let btnSua='<button type="button" class="btn btn-warning float-right" data-toggle="modal" data-target="#modalEditXfileRole" data-xfile-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa bản ghi"><i class="fas fa-edit"></i></span></button>'
    arr.push(btnSua);
    
    return arr;
}
$('#selectEditor').on('select2:select', function(e) {
    var userId=e.params.data.id; //This will give you the id of the selected attribute
    $("#selectChecker option[value='"+userId+"']").each(function() {
        $(this).remove();
    });
    $('#selectChecker').trigger('change');

  });
$('#selectEditor').on('select2:unselect', function(e) {
    var oppositeSelectElement=$('#selectChecker');
    let newOption = new Option(e.params.data.text, e.params.data.id, false, false);
    oppositeSelectElement.append(newOption).trigger('change');
});
$('#selectChecker').on('select2:select', function(e) {
    var userId=e.params.data.id; //This will give you the id of the selected attribute
    $("#selectEditor option[value='"+userId+"']").each(function() {
        $(this).remove();
    });
    $('#selectEditor').trigger('change');


  });
$('#selectChecker').on('select2:unselect', function(e) {
    var oppositeSelectElement=$('#selectEditor');
    let newOption = new Option(e.params.data.text, e.params.data.id, false, false);
    oppositeSelectElement.append(newOption).trigger('change');
});
