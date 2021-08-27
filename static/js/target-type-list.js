const TARGET_TYPES=[
    ['1','target-direction'],
    ['2','target-group'],
    ['3','target-area'],
];
$(document).ready(function () {
    for (let i in TARGET_TYPES){
        // ['1','target-direction']
        getTargetTypes(TARGET_TYPES[i][0],true);
    }

});
$( "#btnSave" ).on( "click", function() {
    // Validation
    if ($('#targetType').val()=='0'){
        $('#optTargetTypeFeedback').show();
        return; 
    }
    $('#optTargetTypeFeedback').hide();
    // End Validation
    if ($('#targetTypeName').val()==''){
        $('#optTargetNameFeedback').show();
        return; 
    }
    $('#optTargetNameFeedback').hide();
    let targetType=$('#targetType').val();
    let data={
        'target-type':targetType,
        'target-id':$('#targetTypeId').val(),
        'target-name':$('#targetTypeName').val(),
        'target-desc':$('#targetTypeDesc').val()
    }
    $.ajax({
        type: 'POST',
        url: '/add-edit-target-type',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                getTargetTypes(targetType);
                showNotification('Lưu thành công');
                
            }
            else{
                showNotification(resp['msg']);

            }
    
        })
        .fail(() => {
            showNotification("Failed");
        });
        $('#modalAddTargetType').modal('hide');

});

function resolveTargetTypeToString(targetType){
    for (let i in TARGET_TYPES){
        if (targetType==TARGET_TYPES[i][0]){
            return TARGET_TYPES[i][1];
        }
    }   
}
$('#modalAddTargetType').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var targetTypeId = button.data('id'); // Extract info from data-* attributes
    var targetType = button.data('type'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn Loại mục tiêu
    $('#targetType').val('0');
    $('#targetTypeId').val(targetTypeId);
    
    if(targetTypeId!=''){
        // Có dữ liệu --> Get dữ liệu để chỉnh sửa
        $.ajax({
            type: 'GET',
            url: '/get-target-type-by-id',
            data: {
                'type':targetType,
                'id':targetTypeId
            },
        })
            .done((resp) => {
                if(resp['status']===0){
                    let data=resp['data'];
                    // {"id": 1, "name": "dsa", "description": "das"}
                    $('#targetType').val(targetType);
                    $('#targetTypeName').val(data['name']);
                    $('#targetTypeDesc').val(data['description']);
                }
                else{
                    showNotification(resp['msg']);
                }
            })
            .fail(() => {
                showNotification("Failed");
            });
    }
});
function initTable(dataSet,targetType,initial=false){
    let tbl=$('#tbl-'+resolveTargetTypeToString(targetType));
    if (initial==true){
        tbl.html('');
        tbl.DataTable( {
            data: dataSet,
            columns: [
                { title: "#", "width": "5%" },
                { title: "Tên", "width": "20%"  },
                { title: "Mô tả", "width": "60%"  },
                { title: "" },
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

function DeleteTarget(targetType,targetTypeId){
    let data={
        'target-id':targetTypeId
    }
    $.ajax({
        type: 'POST',
        url: '/delete-target-type',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                getTargetTypes(targetType);
                showNotification('Xoá thành công');
            }
            else{
                showNotification(resp['msg']);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });
}
$('#modalDelete').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var targetTypeId = button.data('id'); // Extract info from data-* attributes
    var targetType = button.data('type'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn Loại mục tiêu
    
    let deleteQuery='DeleteTarget("'+targetType +'","' + targetTypeId+'");';
    $('#btnDelete').attr('onclick',deleteQuery);
    
});

function getTargetTypes(targetType,initial=false){
    
    $.ajax({
        type: 'GET',
        url: '/get-target-type-by-type',
        data:{'targetType':targetType}
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                    // [
                    //  {"id": 1, "name": "dsa", "description": "das"}, 
                    //  {"id": 2, "name": "dsad", "description": "dsa"}
                    // ]
                let displayTableList=[];
                let count=0;
                for (let i in data){
                    count+=1;
                    displayTableList.push(dictTargetTypeToList(data[i],targetType,count));
                }
                initTable(displayTableList,targetType,initial);
            }
            else{   
                showNotification(resp['msg']);
            }
            
        })
        .fail(() => {
            showNotification("Failed");
        });

}   
function dictTargetTypeToList(dict,targetType,count){
    let arr=[];
    arr.push( [count ] );
    arr.push( [dict['name'] ] );
    arr.push( [dict['description'] ] );
        // <button type="button" class="btn btn-warning" data-toggle="modal" data-target="#modalAddTargetType" data-id="1" data-type="target-direction">Sửa</button>
        // <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#modalDelete" data-id="1" data-type="target-direction">Xoá</button>
    let btnSua='<button type="button" class="btn btn-warning float-right" data-toggle="modal" data-target="#modalAddTargetType" data-id="'+dict['id']+'" data-type="'+targetType+'"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa bản ghi"><i class="fas fa-edit"></i></span></button>'
    let btnXoa='<button type="button" class="btn btn-danger float-right" data-toggle="modal" data-target="#modalDelete" id="row-'+targetType+'-' +dict['id']+'" data-id="'+dict['id']+'" data-type="'+targetType+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xoá bản ghi"<i class="fas fa-trash-alt"></i></span></button>'
    arr.push(btnXoa+btnSua);
    return arr;
}

$('#modalAddTargetType').on('hidden.bs.modal', function () {
    clear();
})
function clear() {
    $("#targetTypeName").val("");
    $("#targetTypeDesc").val("");
}
