$(document).ready(function () {
    getTasks(false);
});

$('#task-users').multiselect({
    templates: {
        li: '<li><a href="javascript:void(0);"><label class="pl-2"></label></a></li>'
    },
    nonSelectedText: 'Chưa chọn người thực hiện',
    buttonWidth: '100%',
    align: 'right'
});

$('#task-users-edit').multiselect({
    templates: {
        li: '<li><a href="javascript:void(0);"><label class="pl-2"></label></a></li>'
    },
    nonSelectedText: 'Chưa chọn người thực hiện',
    allSelectedText: 'Đã chọn toàn bộ',
    nSelectedText: 'Đã chọn',
    buttonWidth: '100%',
    align: 'right'
});

function getTasks(initial=true){
    $.ajax({
        type: 'GET',
        url: '/get-tasks/',
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status'] === 0) {
                let data = resp['data'];
                let tasks = data['tasks'];
                let displayTableList = [];
                for (let i = 0; i < tasks.length; ++i) {
                    displayTableList.push(dictTaskToList(tasks[i], i+1));

                }
                initTaskTable(displayTableList, initial);
            }
            else showNotification(resp['msg'],NOTIFICATION_ERROR);
        })
        .fail(() => {
            showNotification("Failed");
        });
}

function initTaskTable(dataSet, initial=true){
    let tbl=$('#tblTask');
    if (initial===false){
        // Khởi tạo DataTable
        tbl.html('');
        //  All DataString Tables: https://tablepress.org/extensions/change-datatables-strings/
        tbl.DataTable( {
            data: dataSet,
            columns: [
                { title: "#", "width": "5%" },
                { title: "Tên công việc" },
                { title: "Người quản lý" },
                { title: "Người thực hiện" },
                { title: "Ngày bắt đầu" },
                { title: "Hạn thực hiện" },
                { title: "Tình trạng", width: "10%" },
                { title: "" },
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

function dictTaskToList(dict, count) {
    let arr = [];
    arr.push( [count] );
    arr.push( [dict['title']] );

    let manager='<a href="/profile?u=' + dict['manager'] + '">' + dict['manager'] + '</a>';
    arr.push( [manager] );

    let users = '';
    for (let i in dict['users']) {
        if (users.length) users += ', ';
        let user = '<a href="/profile?u=' + dict['users'][i] + '">' + dict['users'][i] + '</a>';
        users += user;
    }
    arr.push( [users] );

    arr.push( [moment(dict['start_at']).format("DD/MM/yyyy")] );
    arr.push( [moment(dict['deadline']).format("DD/MM/yyyy")] );

    let btnStatus='';
    switch (dict['status']) {
        case 0:
            btnStatus = '<btn type="button" class="btn btn-sm btn-dark ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="0"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-pause-circle"></i> </span> </btn>';
            break;
        case 1:
            btnStatus = '<btn type="button" class="btn btn-sm btn-primary ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="1"><span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-pen"></i> </span>  </btn>';
            break;
        case 2:
            btnStatus = '<btn type="button" class="btn btn-sm btn-warning ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="2"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-search"></i> </span> </btn>';
            break;
        default:
            btnStatus = '<btn type="button" class="btn btn-sm btn-success ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="3"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-check-circle"></i> </span> </btn>';
    }
    arr.push( [btnStatus] );

    let btnInfo = '<a class="btn btn-sm btn-info float-right mr-0 mr-md-2" href="/task/' + dict['id'] + '"> <span data-toggle="tooltip" data-placement="bottom" title="Xem chi tiết"><i class="fas fa-info-circle"></i></span></a>';
    let btnEdit = '<a class="btn btn-sm btn-primary float-right mr-0 mr-md-2" data-toggle="modal" data-target="#modalEditTask" data-id="'+dict['id']+'" data-value="' + JSON.stringify(dict).replaceAll('"', "&quot;") + '"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa công việc"><i class="fas fa-edit"></i></span></a>';
    let btnDelete = '<a class="btn btn-sm btn-danger float-right mr-0 mr-md-2" data-toggle="modal" data-target="#modalDelete" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xóa công việc"><i class="fas fa-trash"></i></span></a>';
    arr.push(btnDelete + btnEdit + btnInfo);

    return arr;
}

function changeStatus(taskId, status) {
    $.ajax({
        type: 'POST',
        url: '/switch-status/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'task_id': taskId, status},
    })
        .done((resp) => {
            if(resp['status'] === 0) {
                getTasks();
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

function deleteTask(taskId) {
    $.ajax({
        type: 'POST',
        url: '/delete-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'task_id': taskId},
    })
        .done((resp) => {
            if(resp['status']===0){
                getTasks();
                showNotification("Xoá công việ̣c thành công", NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'], NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });

}

$('#btnSaveNewTask').on('click', function () {
    let data = {
        title: $('#task-title').val(),
        content: $('#task-content').val(),
        start_at: $('#task-start-at').val(),
        deadline: $('#task-deadline').val(),
        users: $('#task-users').val(),
    };
    $.ajax({
        type: 'POST',
        url: '/add-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status'] === 0){
                getTasks();
                showNotification("Tạo mới thành công", NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'], NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });
});

$('#modalChangeStatus').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let miniTaskId = button.data('id');
    let value = button.data('value');
    $('#statusType').val(value);
    $("select#statusType").change(function() {
        let status = $(this).children("option:selected").val();
        let changeStatusFunc= 'changeStatus(' + miniTaskId + ', ' + status + ');';
        $('#btn-change-status').attr('onclick', changeStatusFunc);
    });
});

$('#modalDelete').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let taskId = button.data('id');
    let deleteTaskFunc = 'deleteTask("'+taskId +'");';
    $('#btnDeleteTask').attr('onclick', deleteTaskFunc);

});

$('#modalEditTask').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let value = button.data('value');
    $("#task-id-edit").html(value.id);
    $("#task-title-edit").val(value.title);
    $("#task-content-edit").html(value.content);
    $('#task-users-edit').val(value.users);
    $('#task-users-edit').multiselect("refresh");
    $("#task-start-at-edit").val(moment(value.start_at).format('YYYY-MM-DD'));
    $("#task-deadline-edit").val(moment(value.deadline).format('YYYY-MM-DD'));
});

function editTask(taskId, title, content, start_at, deadline, users) {
    console.log(taskId)
    $.ajax({
        type: 'POST',
        url: '/edit-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'task_id': taskId, title, content, start_at, deadline, users},
    })
        .done((resp) => {
            if(resp['status'] === 0) {
                getTasks();
                showNotification("Chỉnh sửa công việ̣c thành công", NOTIFICATION_SUCCESS);
            }
            else{
                showNotification(resp['msg'], NOTIFICATION_ERROR);

            }
        })
        .fail(() => {
            showNotification("Failed");
        });
}

$('#btn-edit-task').on('click', () => {
    let taskId = $("#task-id-edit").html();
    let title = $("#task-title-edit").val();
    let content = $("#task-content-edit").val();
    let start_at = $("#task-start-at-edit").val();
    let deadline = $("#task-deadline-edit").val();
    let users = $("#task-users-edit").val();
    editTask(taskId, title ,content, start_at, deadline, users);
});

