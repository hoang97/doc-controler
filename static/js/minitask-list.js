$(document).ready(function () {
   getMiniTasks(false);
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

$('#mini-task-users').multiselect({
    templates: {
        li: '<li><a href="javascript:void(0);"><label class="pl-2"></label></a></li>'
    },
    nonSelectedText: 'Chưa chọn người thực hiện',
    allSelectedText: 'Đã chọn toàn bộ',
    nSelectedText: 'Đã chọn',
    buttonWidth: '100%',
    align: 'right'
});

$('#mini-task-users-edit').multiselect({
    templates: {
        li: '<li><a href="javascript:void(0);"><label class="pl-2"></label></a></li>'
    },
    nonSelectedText: 'Chưa chọn người thực hiện',
    allSelectedText: 'Đã chọn toàn bộ',
    nSelectedText: 'Đã chọn',
    buttonWidth: '100%',
    align: 'right'
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

function initMiniTaskTable(dataSet, initial = true){
    let tbl = $('#tblTask');
    if (initial === false){
        // Khởi tạo DataTable
        tbl.html('');
        //  All DataString Tables: https://tablepress.org/extensions/change-datatables-strings/
        tbl.DataTable( {
            data: dataSet,
            columns: [
                { title: "#", "width": "5%" },
                { title: "Tên công việc" },
                { title: "Nội dung" },
                { title: "Người thực hiện" },
                { title: "Ngày bắt đầu" },
                { title: "Hạn thực hiện" },
                { title: "Tình trạng", width: "10%" },
                { title: "" },
            ],
            "language": DATATABLE_LANGUAGE
        } );
    }
    else {
        tbl.dataTable().fnClearTable();
        if (dataSet.length>0){
            tbl.dataTable().fnAddData(dataSet);
        }
    }
}

function dictMiniTaskToList(dict, count) {
    let arr = [];
    arr.push( [count] );
    arr.push( [dict['title']] );
    arr.push( [dict['content']] );

    let users = '';
    for (let i in dict['users']) {
        if (users.length) users += ', ';
        let user = '<a href="/profile?u=' + dict['users'][i] + '">' + dict['users'][i] + '</a>';
        users += user;
    }
    arr.push( [users] );

    arr.push( [moment(dict['start_at']).format("DD/MM/yyyy")] );
    arr.push( [moment(dict['deadline']).format("DD/MM/yyyy")] );

    let btnStatus = '';
    switch (dict['status']) {
        case 0:
            btnStatus = '<btn  type="button" class="btn btn-sm btn-dark ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="0"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-pause-circle"></i> </span> </btn>';
            break;
        case 1:
            btnStatus = '<btn  type="button" class="btn btn-sm btn-primary ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="1"><span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-pen"></i> </span>  </btn>';
            break;
        case 2:
            btnStatus = '<btn  type="button" class="btn btn-sm btn-danger ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="2"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-search"></i> </span> </btn>';
            break;
        default:
            btnStatus = '<btn  type="button" class="btn btn-sm btn-success ml-3" data-toggle="modal" data-target="#modalChangeStatus" data-id="'+dict['id']+'" data-value="3"> <span data-toggle="tooltip" data-placement="bottom" title="Bấm để chuyển trạng thái"> <i class="fas fa-check-circle"></i> </span> </btn>';
    }
    arr.push( [btnStatus] );

    let btnEdit = '<a class="btn btn-sm btn-primary float-right mr-2" data-toggle="modal" data-target="#modalEditMiniTask" data-id="'+dict['id']+'" data-value="' + JSON.stringify(dict).replaceAll('"', "&quot;") + '"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa nhiệm vụ"><i class="fas fa-edit"></i></span></a>';
    let btnDelete = '<a class="btn btn-sm btn-danger float-right" data-toggle="modal" data-target="#modalDeleteMiniTask" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xem nhiệm vụ"><i class="fas fa-trash"></i></span></a>';
    arr.push(btnDelete + btnEdit);
    return arr;
}

$('#btn-save-new-mini-task').on('click', function () {
    let data = {
        title: $('#mini-task-title').val(),
        content: $('#mini-task-content').val(),
        start_at: $('#mini-task-start-at').val(),
        deadline: $('#mini-task-deadline').val(),
        users: $('#mini-task-users').val(),
    };
    $.ajax({
        type: 'POST',
        url: '/add-mini-task/'+$(this).attr("data-id"),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if (resp['status'] === 0){
                getMiniTasks();
                showNotification("Tạo mới thành công", NOTIFICATION_SUCCESS);
            }
            else showNotification(resp['msg'], NOTIFICATION_ERROR);
        })
        .fail(() => {
            showNotification("Failed");
        });
});

function changeStatus(miniTaskId, status) {
    $.ajax({
        type: 'POST',
        url: '/switch-status-mini-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'mini_task_id': miniTaskId, status},
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

function editTask(taskId, title, content, start_at, deadline, users) {
    $.ajax({
        type: 'POST',
        url: '/edit-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'task_id': taskId, title, content, start_at, deadline, users},
    })
        .done((resp) => {
            if(resp['status'] === 0) {
                window.location.reload();
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

function editMiniTask(miniTaskId, title, content, start_at, deadline, users) {
    $.ajax({
        type: 'POST',
        url: '/edit-mini-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'mini_task_id': miniTaskId, title, content, start_at, deadline, users},
    })
        .done((resp) => {
            if(resp['status'] === 0) {
                getMiniTasks();
                showNotification("Chỉnh sửa nhiệm vụ thành công", NOTIFICATION_SUCCESS);
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
            if(resp['status']===0) {
                window.location = "/task/list";
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

function deleteMiniTask(miniTaskId) {
    $.ajax({
        type: 'POST',
        url: '/delete-mini-task/',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {'mini_task_id': miniTaskId},
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

$('#modalEditTask').on('show.bs.modal', function (event) {
    $("#task-title-edit").val($("#task-title").text());
    $("#task-content-edit").html($("#task-content").text());
    $('#task-users-edit').val(JSON.parse(($("#task-users").text().replaceAll('\'', '"'))));
    $('#task-users-edit').multiselect("refresh");
    $("#task-start-at-edit").val(moment($("#task-start-at").text()).format('YYYY-MM-DD'));
    $("#task-deadline-edit").val(moment($("#task-deadline").text()).format('YYYY-MM-DD'));
});

$('#btn-edit-task').on('click', () => {
    let taskId = $("#task-id").html();
    let title = $("#task-title-edit").val();
    let content = $("#task-content-edit").val();
    let start_at = $("#task-start-at-edit").val();
    let deadline = $("#task-deadline-edit").val();
    let users = $("#task-users-edit").val();
    editTask(taskId, title ,content, start_at, deadline, users);
});

$('#modalDeleteTask').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let taskId = button.data('id');
    let deleteTaskFunc = 'deleteTask("'+taskId +'");';
    $('#btn-delete-task').attr('onclick', deleteTaskFunc);
});

$('#modalEditMiniTask').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let value = button.data('value');
    $("#mini-task-id-edit").html(value.id);
    $("#mini-task-title-edit").val(value.title);
    $("#mini-task-content-edit").html(value.content);
    $('#mini-task-users-edit').val(value.users);
    $('#mini-task-users-edit').multiselect("refresh");
    $("#mini-task-start-at-edit").val(moment(value.start_at).format('YYYY-MM-DD'));
    $("#mini-task-deadline-edit").val(moment(value.deadline).format('YYYY-MM-DD'));
});

$('#btn-edit-mini-task').on('click', () => {
    let miniTaskId = $("#mini-task-id-edit").html();
    let title = $("#mini-task-title-edit").val();
    let content = $("#mini-task-content-edit").val();
    let start_at = $("#mini-task-start-at-edit").val();
    let deadline = $("#mini-task-deadline-edit").val();
    let users = $("#mini-task-users-edit").val();
    editMiniTask(miniTaskId, title ,content, start_at, deadline, users);
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

$('#modalDeleteMiniTask').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let miniTaskId = button.data('id');
    let deleteMiniTaskFunc = 'deleteMiniTask("'+miniTaskId +'");';
    $('#btn-delete-mini-task').attr('onclick', deleteMiniTaskFunc);
});
