$(document).ready(function () {
    initXFileList();
    setCreateModalForm();
    setDeleteModalForm();
});

function filterXFileByType(xfiles, type_id) {
    let filtered_xfiles = [];
    xfiles.forEach(xfile => {
        if (xfile.type.id == type_id) {
            filtered_xfiles.push(xfile);
        }
    });
    return filtered_xfiles;
};

function initXFileTableByType(type, data) {
    let xfileTableElement=$('#tbl'+type.id);
    let xfileTabElement=$('#tab'+type.id);
    let t = xfileTableElement.DataTable({
        // 'processing': true,
        data: filterXFileByType(data, type.id),
        columns: [
            // Index column
            { width: "2rem", title: "#", searchable: false, orderable: false, data: "id" },
            // Data columns
            { width: "10%", title: "Mã số", render: rendererForSingleColumn('code', 'id', '/hsmt/edit-detail/?id=<>') },
            { width: "10%", title: "Ngày tạo", data: "date_created", render: (data) => {return displayDatetime(data)} },
            { width: "25%", title: "Người chỉnh sửa", render: rendererForArrayColumn('editors', 'first_name', 'username', '/profile?u=<>') },
            { width: "20%", title: "Người kiểm định", render: rendererForArrayColumn('checkers', 'first_name', 'username', '/profile?u=<>') },
            { width: "10%", title: "Phòng", data: "department.name" },
            { width: "10%", title: "Trạng thái", data: xfileStatusDisplay },
            // Button columns
            { width: "8rem", title: "", searchable: false, orderable: false, render: rendererForButtonColumn('id', '/hsmt/edit-detail/?id=<>', '', '/api/hsmt/<>/general/')},
        ],
        order: [[ 2, 'des' ]],
        language: DATATABLE_LANGUAGE
    });
    t.on('order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
    xfileTabElement.on('shown.bs.tab', function(e){
        t.columns.adjust();
    });
}

function initXFileList() {
    $.ajax({
        type: 'GET',
        url: '/api/hsmt-type/',
        success: (typeData) => {
            $.ajax({
                type: 'GET',
                url: '/api/hsmt/',
                success: (xfileData) => {
                    typeData.forEach((type) => {
                        initXFileTableByType(type, xfileData);
                    })
                },
                error: (xhr, status, error) => {
                    showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
                }
            });
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status], 3);
        }
    });
};

// function initCreateModal() {
//     $("#inputEditorsCreate").val(null).trigger('change');
//     $("#inputCheckersCreate").val(null).trigger('change');
//     $("#inputApproversCreate").val(null).trigger('change');
// };