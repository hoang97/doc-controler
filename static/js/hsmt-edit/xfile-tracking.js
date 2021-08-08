function ReloadXfileTrackings(xfileId){
    $.ajax({
        type: 'GET',
        url: '/get-xfile-tracking',
        data: {
            'xfileId':xfileId,
        }
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                let displayTableList=[];
                for (let i in data){
                    displayTableList.push(dictTrackingToList(data[i]));
                }
                initTableXfileTracking(displayTableList);
            
            }
            else{
                showNotification(resp['msg']);
            }
    
        })
        .fail(() => {
            showNotification("Failed");
        });
}
function dictTrackingToList(dict){
    // date_action = models.DateTimeField()
    // content = models.TextField()
    // result = models.TextField()
    // user_action = models.TextField()
    let arr=[];
    arr.push( [displayDatetime(dict['date_action']) ] );
    arr.push( ([dict['content'] ]) );
    arr.push( ([dict['result'] ]) );
    arr.push( ([dict['user_action'] ]) );
    let btnSua='';
    let btnXoa='';
    if (dict['verified']){
        arr.push( ([ '<span class="text-lg text-success" data-toggle="tooltip" data-placement="bottom" title="Bản theo dõi đã xác minh"><i class="fas fa-check-circle"></i></span>' ]) );

    }
    else{
        arr.push( ([ '<span class="text-lg text-danger" data-toggle="tooltip" data-placement="bottom" title="Bản theo dõi chưa xác minh"><i class="fas fa-exclamation-circle"></i></span>' ]) );
        btnSua='<button type="button" class="btn btn-warning float-right" data-toggle="modal" data-target="#modalAddEditXfileTracking" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa bản ghi"><i class="fas fa-edit"></i></span></button>'
        btnXoa='<button type="button" class="btn btn-danger float-right" data-toggle="modal" data-target="#modalDeleteXTracking" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xoá bản ghi"<i class="fas fa-trash-alt"></i></span></button>'
    }
    arr.push(btnXoa+btnSua);
return arr;
}
initTableXfileTracking([],true);
function initTableXfileTracking(dataSet,initial=false){
    var tbl=$('#tblXfileTracking');
    if(initial==true){
        tbl.html('');
        tbl.DataTable({
            data: dataSet,
            columns: [
                // { title: "#","width": "5%" },
                { title: "Thời gian tiến hành" },
                { title: "Nội dung/Cách thức"},
                { title: "Kết quả/ Đánh giá"},
                { title: "Người thực hiện"},
                { title: "Xác minh" },
                { title: "","width": "15%" }

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

$('#btnAddEditXTracking').on('click',function(){
    let xfileId=$('#originalXfileId').val();
    data={
        'xfileId':xfileId,
        'trackingId':$('#trackingId').val(),
        'trackingContent':$('#trackingContent').val(),
        'trackingDatetime':standardDatetime($('#trackingDatetime').val()),
        'trackingResult':$('#trackingResult').val(),
        'trackingActor':$('#trackingActor').val(),
    }
    $.ajax({
        type: 'POST',
        url: '/add-edit-xfile-tracking',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                ReloadXfileTrackings(xfileId);
                $('#modalAddEditXfileTracking').modal('hide');
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


$('#modalDeleteXTracking').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var trackingId = button.data('id'); // Extract info from data-* attributes

    $('#deleteTrackingId').val(trackingId);
});

$('#modalAddEditXfileTracking').on('show.bs.modal', function (event) {
    // $('#cardNhatKy').hide();
    var button = $(event.relatedTarget); // Button that triggered the modal
    var trackingId = button.data('id'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn
    $('#trackingId').val(trackingId);
    if(trackingId!=''){
        // Có dữ liệu --> Get dữ liệu để chỉnh sửa
        $.ajax({
            type: 'GET',
            url: '/get-xfile-tracking-by-id',
            data: {
                'id':trackingId
            },
        })
            .done((resp) => {
                if(resp['status']===0){
                    let data=resp['data'];
                    // {"id": 1, "date_action": "2021-05-25T00:00:00Z", "content": "hehe", "result": "hehe", "user_action": "he", "xfile": 4}
                    $('#trackingContent').val(data['content']);
                    $('#trackingDatetime').val(displayDatetime(data['date_action']));
                    $('#trackingResult').val(data['result']);
                    $('#trackingActor').val(data['user_action']);
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
        $('#trackingId').val("");
        $('#trackingContent').val("");
        $('#trackingDatetime').val("");
        $('#trackingResult').val("");
        $('#trackingActor').val("");
    }
});

$('#btnDeleteXTracking').on('click',function(){
    let xfileId=$('#originalXfileId').val();
   let data={
    'trackingId':$('#deleteTrackingId').val()
    }
   $.ajax({
    type: 'POST',
    url: '/delete-xfile-tracking',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    data: data,
})
    .done((resp) => {
        if(resp['status']===0){
            ReloadXfileTrackings(xfileId);
            $('#modalDeleteXTracking').modal('hide');
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