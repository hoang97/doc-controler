$(document).ready(function () {
    initXFileList();
});

function dotNotation(data, expr) {
    //examples: expr = 'a.b.c' => return data.a.b.c
    fields = expr.split('.')
    result = data
    for (i in fields) {
        field = fields[i]
        result = result[field]
    }
    return result
}

function rendererForSingleColumn(disp_field, url_field, url_example) {
    // Tạo Renderer để hiển thị dưới dạng link (item)
    // trong đó item là giá trị của data.disp_field
    // url_example có dạng /your/url/<>/to/item
    // trong đó <> là giá trị của data.url_field
    var disp_field=disp_field, url_field=url_field, url_example=url_example;
    return (data, type, row, meta) => {
        let disp = dotNotation(row, disp_field);
        let url = dotNotation(row, url_field);
        let url_components = url_example.split('<>');
        let full_url = url_components[0] + url + url_components[1];
        return '<a href="' + full_url + '">' + disp + '</a>'
    };
};

function rendererForArrayColumn(array_field, disp_field, url_field, url_example) {
    // Tạo Renderer để hiển thị dưới dạng các link (item, item, ...)
    // item là giá trị data.array_field.[].disp_field
    // url_example có dạng /your/url/<>/to/item 
    // trong đó <> là giá trị của data.array_field.[].url_field
    var disp_field=disp_field, url_field=url_field, url_example=url_example;
    return (data, type, row, meta) => {
        let arr = dotNotation(row, array_field);
        let result = '';
        arr.forEach((data, index) => {
            let disp = dotNotation(data, disp_field);
            let url = dotNotation(data, url_field);
            let url_components = url_example.split('<>');
            let full_url = url_components[0] + url + url_components[1];
            if (index>0) {result += ', '};
            result += '<a href="' + full_url + '">' + disp + '</a>';
        });
        return result;
    };
}

function statusDisplay(data) {
    // Khởi tạo hình ảnh cho status tương ứng
    status = data['status']
    return '<span \
        class="badge badge-'+XFILE_STATUS[status][2]+'" \
        data-toggle="tooltip" data-placement="bottom" \
        title="'+XFILE_STATUS[status][3]+'">'+
        XFILE_STATUS[status][1]+'</span>';
}

function filterXFileByType(xfiles, type_id) {
    filtered_xfiles = []
    xfiles.forEach(xfile => {
        if (xfile.type.id == type_id) {
            filtered_xfiles.push(xfile)
        }
    })
    return filtered_xfiles
}

function initXFileTableByType(type, data) {
    let xfileTableElement=$('#tbl'+type.id);
    let xfileTabElement=$('#tab'+type.id);
    let t = xfileTableElement.DataTable({
        'processing': true,
        'data': filterXFileByType(data, type.id),
        'columns': [
            { "width": "3em", title: "#", "searchable": false, "orderable": false, "targets": 0, "data": "id" },
            { "width": "10%", title: "Mã số", "render": rendererForSingleColumn('code', 'id', '/hsmt/edit-detail/?id=<>') },
            { "width": "15%", title: "Ngày tạo", "data": "date_created" },
            // { title: "Ngày sửa", "data": "changes.0.date_edited" },
            { "width": "25%", title: "Người chỉnh sửa", "render": rendererForArrayColumn('editors', 'first_name', 'username', '/profile?u=<>') },
            { "width": "25%", title: "Người kiểm định", "render": rendererForArrayColumn('checkers', 'first_name', 'username', '/profile?u=<>') },
            { "width": "10%", title: "Phòng", "data": "department.name" },
            { "width": "12%", title: "Trạng thái", "data": statusDisplay },
        ],
        "order": [[ 2, 'des' ]],
        "language": DATATABLE_LANGUAGE
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
                        initXFileTableByType(type, xfileData)
                    })
                },
                error: (xhr, status, error) => {
                    showNotification(HTML_CODE_MESSAGE[xhr.status])
                }
            })
        },
        error: (xhr, status, error) => {
            showNotification(HTML_CODE_MESSAGE[xhr.status])
        }
    })
}