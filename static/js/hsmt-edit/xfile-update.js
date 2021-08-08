function ReloadXfileUpdates(xfileId){
    $.ajax({
        type: 'GET',
        url: '/get-xfile-update',
        data: {
            'xfileId':xfileId,
        }
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                let displayTableList=[];
                for (let i in data){
                    displayTableList.push(dictUpdateToList(data[i]));
                }
                initTableXfileUpdate(displayTableList);
            
            }
            else{
                showNotification(resp['msg']);
            }
        })
        .fail(() => {
            showNotification("Failed");
        });
}
function dictUpdateToList(dict){

    let arr=[];
    arr.push( [displayDatetime(dict['date_created']) ] );
    arr.push( ([dict['content'] ]) );
    arr.push( ([dict['editor'] ]) );
    arr.push( ([dict['checker'] ]) );
    arr.push( ([dict['approver'] ]) );
    let btnSua='';
    let btnXoa='';
    if (dict['verified']){
        arr.push( ([ '<span class="text-lg text-success" data-toggle="tooltip" data-placement="bottom" title="Bản cập nhật đã xác minh"><i class="fas fa-check-circle"></i></span>' ]) );

    }
    else{
        arr.push( ([ '<span class="text-lg text-danger" data-toggle="tooltip" data-placement="bottom" title="Bản cập nhật chưa xác minh"><i class="fas fa-exclamation-circle"></i></span>' ]) );
        btnSua='<button type="button" class="btn btn-warning float-right" data-toggle="modal" data-target="#modalAddEditXfileUpdate" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa bản ghi"><i class="fas fa-edit"></i></span></button>'
        btnXoa='<button type="button" class="btn btn-danger float-right" data-toggle="modal" data-target="#modalDeleteXUpdate" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xoá bản ghi"<i class="fas fa-trash-alt"></i></span></button>'
    }

    arr.push(btnXoa+btnSua);
return arr;
}
initTableXfileUpdate([],true);
function initTableXfileUpdate(dataSet,initial=false){
    var tbl=$('#tblXfileUpdate');
    if(initial==true){
        tbl.html('');
        tbl.DataTable({
            data: dataSet,
            columns: [
                // { title: "#","width": "5%" },
                { title: "Thời gian cập nhật" },
                { title: "Nội dung"},
                { title: "Người cập nhật"},
                { title: "Người thẩm định"},
                { title: "Người duyệt"},
                { title: "Xác minh"},
                { title: "","width": "10%" }
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

$('#btnAddEditXUpdate').on('click',function(){
    let xfileId=$('#originalXfileId').val();
    data={
        'xfileId':xfileId,
        'updateId':$('#updateId').val(),
        'updateContent':$('#updateContent').val(),

    }
    $.ajax({
        type: 'POST',
        url: '/add-edit-xfile-update',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                ReloadXfileUpdates(xfileId);
                $('#modalAddEditXfileUpdate').modal('hide');
                showNotification("Thêm mớI/ Sửa thành công");
            }
            else{
                showNotification(resp['msg']);
            }
    
        })
        .fail(() => {
            showNotification("Failed");
        });
});


$('#modalDeleteXUpdate').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var updateId = button.data('id'); // Extract info from data-* attributes

    $('#deleteUpdateId').val(updateId);
});

$('#modalAddEditXfileUpdate').on('show.bs.modal', function (event) {
    // $('#cardNhatKy').hide();
    var button = $(event.relatedTarget); // Button that triggered the modal
    var updateId = button.data('id'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn
    $('#updateId').val(updateId);
    if(updateId!=''){
        // Có dữ liệu --> Get dữ liệu để chỉnh sửa
        $.ajax({
            type: 'GET',
            url: '/get-xfile-update-by-id',
            data: {
                'id':updateId
            },
        })
            .done((resp) => {
                if(resp['status']===0){
                    let data=resp['data'];
                    // {"id": 1, "date_action": "2021-05-25T00:00:00Z", "content": "hehe", "result": "hehe", "user_action": "he", "xfile": 4}
                    $('#updateContent').val(data['content']);

                    }
                else{
                    showNotification(resp['msg']);
                }
              
                
            })
            .fail(() => {
                showNotification("Failed");
            });
    }
    else{
        $('#updateId').val("");
        $('#updateContent').val("");

    }
});

$('#btnDeleteXUpdate').on('click',function(){
    let xfileId=$('#originalXfileId').val();
   let data={
    'updateId':$('#deleteUpdateId').val()
    }
   $.ajax({
    type: 'POST',
    url: '/delete-xfile-update',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    data: data,
})
    .done((resp) => {
        if(resp['status']===0){
            ReloadXfileUpdates(xfileId);
            $('#modalDeleteXUpdate').modal('hide');
            showNotification("Xoá thành công");
        }
        else{
            showNotification(resp["msg"]);

        }
    })
    .fail(() => {
        showNotification("Failed");
    });
});