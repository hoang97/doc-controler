
const XFILE_TYPES=[
    [1,'TM'],
    [2,'TC'],
    [3,'ĐT']
];
const NOTE_STATUS=[
    [0,'<i class="fas fa-exclamation-circle"></i>','danger','Nhận xét chưa được xử lý'],
    [1,'<i class="fas fa-check-circle"></i>','success','Nhận xét đã hoàn thành'],
];

$(document).ready(function () {
    getNotes(true);
});



$( "#btnSave" ).on( "click", function() {
    notestatus = isCheckBoxChecked("chkBoxNoteStatus");
    xfileIdInSelect2=$('#selectXfile').select2('data');
    if (xfileIdInSelect2.length<=0){
        showNotification("Hãy chọn HSMT");
        return;
    }
    xfileId=xfileIdInSelect2[0]['id'];
    let data={
        'noteId':$('#noteId').val(),
        'noteTitle':$('#noteTitle').val(),
        'noteContent':$('#noteContent').val(),
        'xfileId':xfileId,
        'noteStatus':notestatus,
        
    }

    $.ajax({
        type: 'POST',
        url: '/add-edit-note',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){

                getNotes();
                $('#modalAddEditNote').modal('hide');
                $('#cardNhatKy').hide();
            }
            else{
                alert("Lỗi status");
            }
    
        })
        .fail(() => {
            alert("Failed");
        });

});
function ClearModalAddNote(){
    $('#noteContent').val("");
}
$('#modalAddEditNote').on('show.bs.modal', function (event) {
    // $('#cardNhatKy').hide();
    var button = $(event.relatedTarget); // Button that triggered the modal
    var noteId = button.data('id'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn
    $('#noteId').val(noteId);
    if(noteId!=''){
        // Có dữ liệu --> Get dữ liệu để chỉnh sửa
        $('#cardNhatKy').hide();
        $('#cardInfo').show();
        $('#divSelectXfile').hide();
            $.ajax({
                type: 'GET',
                url: '/get-note-by-id',
                data: {
                    'id':noteId
                },
            })
                .done((resp) => {
                    if(resp['status']===0){
                        let data=resp['data'];
                        // // {"id": 1, "name": "dsa", "description": "das"}
                        $('#noteTitle').val(data['title']);

                        $('#noteContent').val(data['content']);
                        if(data['status']==true){
                            $('#chkBoxNoteStatus').prop('checked',true);
                        }
                        else{
                            $('#chkBoxNoteStatus').prop('checked',false);

                        }

                        $('#noteDateCreated').val(displayDatetime(data['date_created']));
                        $('#noteDateModified').val(displayDatetime(data['date_modified']));

    
                        $('#xfileName').val((data['xfile']['name']));

                        for (let i in XFILE_TYPES){
                            if (XFILE_TYPES[i][0]==data['xfile']['xfile_type']){
                                $('#xfileType').val((XFILE_TYPES[i][1]));
                                break;
                            }
                        } 
                        
                        // Xu ly Frontend
                        $('#cardInfo').show();
                        $('#cardNhatKy').show();
                        //Nếu người request = use rtạo note + và xfile đang cho phép chỉnh sửa --> Hiển thị nút chỉnh sửa
                        let requestUser=$('#request-username').val();
                        if (requestUser == data['user']['username'] &&  (data['xfile']['status'] ==2 ||  data['xfile']['status'] ==3) ){
                            $('#btnSave').show();
                        }
                        }
                    else{
                        alert("Lỗi status");
                    }
                    
                    
                })
                .fail(() => {
                    alert("Failed");
                });
    }
    else{
        ClearModalAddNote();
        $('#cardInfo').hide();
        $('#cardNhatKy').hide();
        $('#divSelectXfile').show();
        // Inithsmt(); 
        $('#btnSave').show();

    }
    InitXfileOptions();
});



function initTable(dataSet,initial=false){
    var tbl=  $('#tblNotes');;
    if(initial==true){
        tbl.html('');
        tbl.DataTable({
            data: dataSet,
            columns: [
                { title: "#","width": "5%" },
                { title: "Tiêu đề" },
                { title: "Tên hồ sơ","width": "20%"},
                { title: "Người nhận xét"},
                { title: "Trạng thái"},
                { title: "Ngày tạo" },
                { title: "Sửa lần cuối" },
                { title: "","width": "12%" },

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

function DeleteNote(noteId){
    let data={
        'note-id':noteId
    }
    $.ajax({
        type: 'POST',
        url: '/delete-note',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){

                getNotes();
            }
            else{
                alert("Lỗi status");

            }
        })
        .fail(() => {
            alert("Failed");
        });
}
$('#modalDelete').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var noteId = button.data('id'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn Loại mục tiêu
    let deleteQuery='DeleteNote("'+ noteId+'");';
    $('#btnDelete').attr('onclick',deleteQuery);
    
});

function getNotes(initial=false){
    $.ajax({
        type: 'GET',
        url: '/get-notes',
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                // [
                //     {"title": "", 
                //     "content": "hehe", 
                //     "user": {"username": "tp2", "first_name": "trunog phong 2"}, 
                //     "xfile": {"id": 10, "name": "tac chiem", "xfile_type": 2}, 
                //     "status": true, 
                //     "date_created": "2021-05-18T02:17:16.370Z", 
                //     "date_modified": null}
                // ]
                let displayTableList=[];
                let count=0;
                for (let i in data){
                    count+=1;
                    displayTableList.push(dictToList(data[i],count));
                }
                initTable(displayTableList,initial);
            }
            else{   
                alert("Lỗi status");
            }
            
        })
        .fail(() => {
            alert("Failed");
        });

}   



function dictToList(dict,count){
        // [
    //     {"title": "", 
    //     "content": "hehe", 
    //     "user": {"username": "tp2", "first_name": "trunog phong 2"}, 
    //     "xfile": {"id": 10, "name": "tac chiem", "xfile_type": 2}, 
    //     "status": true, 
    //     "date_created": "2021-05-18T02:17:16.370Z", 
    //     "date_modified": null}
    // ]
    let arr=[];
    arr.push( [count ] );
    
    arr.push( [dict['title'] ] );

    // arr.push( [dict['content'] ] );
    arr.push( ([dict['xfile']['name'] ]) );
    let userATag='<a href="/profile?u='+dict['user']['username']+'">'+dict['user']['first_name']+' </a>';
    arr.push( ([userATag ]) );
    // for (let i in XFILE_TYPES){
    //     if (XFILE_TYPES[i][0]==dict['xfile']['xfile_type']){
    //         arr.push([XFILE_TYPES[i][1]]);
    //         break;
    //     }
    // }
    
    for (let i in NOTE_STATUS){
        if (NOTE_STATUS[i][0]==dict['status']){
            let spanTag='<span class="text-lg text-'+NOTE_STATUS[i][2]+'"  data-toggle="tooltip" data-placement="bottom" title="'+NOTE_STATUS[i][3]+'">'+NOTE_STATUS[i][1]+'</span>';
            arr.push([spanTag]);
            break;
        }
    }
    // arr.push( ([dict['xfile_id'] ]) );

    arr.push( [displayDatetime(dict['date_created' ])] );
    arr.push( [displayDatetime(dict['date_modified'])] );

    let btnSua='';
    let btnXoa='';
    let requestUser=$('#request-username').val();
   if(!dict['status'] ){
        if (requestUser == dict['user']['username']){
            btnXoa='<button type="button" class="btn btn-danger float-right" data-toggle="modal" data-target="#modalDelete" id="rowDelete-'+dict['id']+'" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xoá bản ghi"<i class="fas fa-trash-alt"></i></span></button>';
        }
        btnSua='<button type="button" class="btn btn-warning float-right" data-toggle="modal" data-target="#modalAddEditNote" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa bản ghi"><i class="fas fa-edit"></i></span></button>';
       
    }
    arr.push(btnXoa+btnSua);
    return arr;
}


function InitXfileOptions(){
    $.ajax({
        type: 'GET',
        url: '/get-xfiles',
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];

                let dataDisplay=[];
                for (let i=0;i<data.length;i++){
                    // {"id": 1, "name": "dsa", "description": "das"}, 
                    dataDisplay.push({
                        id:data[i]['id'],
                        text: data[i]['name'],
                    });
                }   
                let selectElement=$('#selectXfile');
                selectElement.html('');
                for (let i=0;i<dataDisplay.length;i++){
                    let newOption = new Option(dataDisplay[i].text, dataDisplay[i].id, false, false);
                    selectElement.append(newOption).trigger('change');
                }
            }
            else{   
                alert("Lỗi status");
            }
            
        })
        .fail(() => {
            alert("Failed");
        });
};
    
