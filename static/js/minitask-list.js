
$(document).ready(function () {
   getMiniTasks(false);
});


function getMiniTasks(initial=true){
    $.ajax({
        type: 'GET',
        url: '/get-mini-tasks/' + document.getElementById('task-id').innerText,
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status'] === 0){
                let data=resp['data'];
                let tasks=data['mini-tasks'];
                let displayTableList=[];
                for (let i = 0; i < tasks.length; ++i) {
                    displayTableList.push(dictMiniTaskToList(tasks[i], i+1));

                }
                initMiniTaskTable(displayTableList, initial);
            }
            else{
                showNotification(resp['msg'],NOTIFICATION_ERROR);
            }

        })
        .fail(() => {
            showNotification("Failed");
        });
}

function initMiniTaskTable(dataSet, initial=true){
    let tbl=$('#tblTask');
    if (initial===false){
        // Khởi tạo DataTable
        tbl.html('');
        //  All DataString Tables: https://tablepress.org/extensions/change-datatables-strings/
        tbl.DataTable( {
            data: dataSet,
            columns: [
                { title: "#","width": "5%" },
                { title: "Tên công việc" },
                { title: "Nội dung" },
                { title: "Người thực hiện" },
                { title: "Ngày bắt đầu" },
                { title: "Hạn thực hiện" },
                { title: "Tình trạng" },
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

function dictMiniTaskToList(dict, count){
    let arr = [];
    arr.push( [count ] );
    arr.push( [dict['title'] ] );
    arr.push( [dict['content'] ] );

    let users = '';
    for (let i in dict['users']) {
        if (users.length) users += ', ';
        let user = '<a href="/profile?u=' + dict['users'][i] + '">' + dict['users'][i] + '</a>';
        users += user;
    }
    arr.push( [users] );

    arr.push( [displayDatetime(dict['start_at']) ] );
    arr.push( [displayDatetime(dict['deadline']) ] );

    let btnStatus='';
    switch (dict['status']) {
        case 0:
            btnStatus='<btn  type="button" class="btn btn-dark ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-pause-circle"></i> </span> </btn>';
            break;
        case 1:
            btnStatus='<btn  type="button" class="btn btn-primary ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'"><span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-pen"></i> </span>  </btn>';
            break;
        case 2:
            btnStatus='<btn  type="button" class="btn btn-danger ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-search"></i> </span> </btn>';
            break;
        default:
            btnStatus='<btn  type="button" class="btn btn-success ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-check-circle"></i> </span> </btn>';
    }
    arr.push( [btnStatus] );

    let btnEdit='<a  class="btn btn-primary float-right mr-2" target="_blank" href="/task/' + dict['id'] + '" > <span data-toggle="tooltip" data-placement="bottom" title="Xem chi tiết"><i class="fas fa-edit"></i></span></a>';
    let btnDelete='<a  class="btn btn-danger float-right" data-toggle="modal" data-target="#modalDelete" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xem chi tiết"><i class="fas fa-trash"></i></span></a>';
    arr.push(btnDelete + btnEdit);
    return arr;
}

$('#btnSaveNewTask').on('click', function () {
    let data = {
        title:$('#task-title').val(),
        content:$('#task-content').val(),
        start_at:$('#task-start-at').val(),
        deadline:$('#task-deadline').val(),
        users:$('#task-users').val(),
    };
    $.ajax({
        type: 'POST',
        url: '/add-mini-task/'+$(this).attr("data-id"),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                getMiniTasks();
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

function changeStatus(taskId, status) {
    $.ajax({
        type: 'POST',
        url: '/switch-status-mini-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'mini_task_id': taskId, status},
    })
        .done((resp) => {
            if(resp['status']===0) {
                getMiniTasks();
                showNotification("Đổi tình trạng nhiệm vụ thành công", NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'], NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });

}

function deleteMiniTask(taskId) {
    $.ajax({
        type: 'POST',
        url: '/delete-mini-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'mini_task_id': taskId},
    })
        .done((resp) => {
            if(resp['status']===0){
                getMiniTasks();
                showNotification("Xoá nhiệm vụ thành công", NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'], NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });

}


$('#modalChangeStatus').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let taskId = button.data('id');
    $("select#statusType").change(function(){
        let status = $(this).children("option:selected").val();
        let changeStatusFunc= 'changeStatus(' + taskId + ', ' + status + ');';
        $('#btnChangeStatus').attr('onclick', changeStatusFunc);
    });
});

$('#modalDelete').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let taskId = button.data('id');
    let deleteMiniTaskFunc = 'deleteMiniTask("'+taskId +'");';
    $('#btnDeleteMiniTask').attr('onclick', deleteMiniTaskFunc);

});