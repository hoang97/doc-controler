const TARGET_TYPES=[
    {id: '1', name:'hướng'},
    {id: '2', name:'nhóm mục tiêu'},
    {id: '3', name:'địa bàn'},
];

$(document).ready(function () {
    initTargetList();
    setCreateModalForm();
    setDeleteModalForm();
    setEditModalForm(initEditModalValue);
});

function initTargetList() {
    $.ajax({
        type: 'GET',
        url: '/api/target/',
        success: (targetData) => {
            TARGET_TYPES.forEach((type) => {
                initTargetTableByType(type, targetData);
            })

        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3)
        }
    });
};

function filterTargetByType(targets, type_id) {
    filtered_targets = []
    targets.forEach(target => {
        if (target.type == type_id) {
            filtered_targets.push(target)
        }
    })
    return filtered_targets
}

function initTargetTableByType(type, data) {
    let targetTableElement=$('#tbl'+type.id);
    let targetTabElement=$('#tab'+type.id);
    let t = targetTableElement.DataTable({
        processing : true,
        data: filterTargetByType(data, type.id),
        columns: [
            // Index column
            { width: "2rem", title: "#", searchable: false, orderable: false,  data: "id" },
            // Data columns
            { width: "30%", title: "Tên", data: "name" },
            { width: "50%", title: "Mô tả", data: "description" },
            // Button columns
            { width: "8rem", title: "", searchable: false, orderable: false, render: rendererForButtonColumn('id', '', '/api/target/<>/', '/api/target/<>/', 'tbl'+type.id)},
        ],
        language: DATATABLE_LANGUAGE,
        order: [[ 1, 'asc' ]],
    });
    t.on('order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
    targetTabElement.on('shown.bs.tab', function(e){
        t.columns.adjust();
    });
}

function initEditModalValue(data){
    $('#inputTypeEdit').val(data.type);
    $('#inputNameEdit').val(data.name);
    $('#inputDescriptionEdit').val(data.description);
}