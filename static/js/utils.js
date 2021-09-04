$(function () {
    var url = window.location;
    // for single sidebar menu
    $('ul.nav-sidebar a').filter(function () {
        return this.href == url;
    }).addClass('active');

    // for sidebar menu and treeview
    $('ul.nav-treeview a').filter(function () {
        return this.href == url;
    }).parentsUntil(".nav-sidebar > .nav-treeview")
        .css({'display': 'block'})
        .addClass('menu-open').prev('a')
        .addClass('active');
});
const LOG_CONTENT_XFILE='9';
const LOG_CONTENT_NOTE='15';
const LOG_CONTENT_USER='4';
const LOG_CONTENT_TYPE=[
    [LOG_CONTENT_XFILE,'xfile'],
    [LOG_CONTENT_NOTE,'note'],
    [LOG_CONTENT_USER,'user'],
];
const NOTIFICATION_INFO=1;
const NOTIFICATION_SUCCESS=2;
const NOTIFICATION_ERROR=3;



function displayDatetime(s,type='short'){
    if (s=='' || s==null){
        return 'Không có';
    }
    let dtObj= new Date(s);
    if (type=='long'){
        dtObj=dtObj.toLocaleString('vi-VN');
    }
    else{
        dtObj=dtObj.toLocaleDateString('vi-VN');
    }
    return dtObj;
}
function showNotification(msg='',type=1){
    var color='blue';
    if (type==NOTIFICATION_SUCCESS){color='green'; }
    else if (type==NOTIFICATION_ERROR){color='red'; }
    $(document).Toasts('create', {
        title:'<i class="fas fa-square-full" style="color:'+color+';"></i> Thông báo' ,
        body: msg,
        autohide: true,
        delay: 3000
      })
};
function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    // console.log('Cookie: ' + cookieValue);
    return cookieValue;
}
const XFILE_STATUS=[
    [0,'Khởi tạo','secondary','Hồ sơ đang được khởi tạo bởi Trợ lý'],
    [1,'Đang sửa đổi','info','Hồ sơ đang quá trình sửa đổi'],
    [2,'Đang kiểm định','primary','Hồ sơ đang trong quá trình kiểm định'],
    [3,'Đang duyệt','warning','Hồ sơ đang chờ duyệt bởi Trưởng phòng'],
    [4,'Hoàn tất','success','Hồ sơ đã được duyệt'],
];
const HTML_CODE_MESSAGE={
    200: 'Lấy dữ liệu thành công',
    201: 'Khởi tạo thành công',
    204: 'Không có dữ liệu',
    400: 'Yêu cầu không hợp lệ',
    401: 'Yêu cầu chưa được xác thực',
    403: 'Không đủ quyền truy cập',
    404: 'Không tìm thấy dữ liệu',
    405: 'Không đủ quyển truy cập',
    406: 'Yêu cầu không hợp lệ',
    409: 'Dữ liệu đã bị thay đổi',
    415: 'Yêu cầu không hợp lệ',
    500: 'Lỗi máy chủ'
};
const DATATABLE_LANGUAGE={
    "lengthMenu": "Hiển thị _MENU_ bản ghi mỗi trang",
    "zeroRecords": "Không tìm thấy kết quả",
    "info":"Hiển thị bản ghi _START_-_END_/_TOTAL_",
    "infoEmpty": "Không có bản ghi nào!",
    "infoFiltered": "(Lọc từ tổng số _MAX_  bản ghi)",
    "search":           "Tìm kiếm:",
    "paginate": {
        "first":        '<i class="fas fa-angle-double-left"></i>',
        "previous":     '<i class="fas fa-angle-left"></i>',
        "next":         '<i class="fas fa-angle-right"></i>',
        "last":         '<i class="fas fa-angle-double-right"></i>'
    },
    "aria": {
        "sortAscending":    ": sắp xếp tăng dần",
        "sortDescending":   ": sắp xếp giảm dần"
    },
};
function isCheckBoxChecked(elementId) {
    var checkBox = document.getElementById(elementId);
    if (checkBox.checked == true){
      return 1;
    } else {
        return 0;
    }
  }

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
    // trong đó item là giá trị của row.disp_field
    // url_example có dạng /your/url/<>/to/item
    // trong đó <> là giá trị của row.url_field
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
    // item là giá trị row.array_field.[].disp_field
    // url_example có dạng /your/url/<>/to/item 
    // trong đó <> là giá trị của row.array_field.[].url_field
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

function rendererForButtonColumn(url_field='', url_detail='', url_edit='', url_delete='', tbl='') {
    // Tạo Renderer để hiển thị dưới dạng các button (btnDetail btnEdit btnDelete)
    // url_detail, url_edit, url_delete có dạng /your/url/<>/to/proccess 
    // trong đó <> là giá trị của row.url_field
    var url_detail=url_detail, url_edit=url_edit, url_delete=url_delete, url_field=url_field, tbl=tbl;
    return (data, type, row, meta) => {
        let url = dotNotation(row, url_field);
        let btnDetail = btnDetailDisplay(url_detail, url);
        let btnEdit = btnEditDisplay(url_edit, url, tbl);
        let btnDelete = btnDeleteDisplay(url_delete, url);
        return btnDelete + btnEdit + btnDetail;
    };
};

function xfileStatusDisplay(data) {
    // Khởi tạo hình ảnh cho status tương ứng
    let status = data['status']
    return '<span \
        class="badge badge-'+XFILE_STATUS[status][2]+'" \
        data-toggle="tooltip" data-placement="bottom" \
        title="'+XFILE_STATUS[status][3]+'">'+
        XFILE_STATUS[status][1]+'</span>';
};

function btnDetailDisplay(url_example, id) {
    // Tạo nút btnDetail là link dẫn đến trang xem chi tiết
    if (!url_example) return '';
    let url_components = url_example.split('<>');
    let full_url = url_components[0] + id + url_components[1];
    let btnDetail =  `<a class="btn btn-primary float-right mr-1 d-none d-md-block" href="${full_url}"> <span data-toggle="tooltip" data-placement="bottom" title="Chi tiết"><i class="fas fa-info-circle"></i></span></a>`
    let btnDetailMini = `<a class="btn btn-primary float-right mr-sm-1 btn-sm d-block d-md-none" href="${full_url}"> <span data-toggle="tooltip" data-placement="bottom" title="Chi tiết"><i class="fas fa-info-circle"></i></span></a>`
    return btnDetail + btnDetailMini;
};

function btnEditDisplay(url_example, id, tbl) {
    // Tạo nút btnEdit là link mở ra modalEdit
    if (!url_example) return '';
    let url_components = url_example.split('<>');
    let full_url = url_components[0] + id + url_components[1];
    let btnEdit =  `<button type="button" class="btn btn-warning float-right mr-1 d-none d-md-block" data-toggle="modal" data-target="#modalEdit" data-tbl="${tbl}" data-id="${id}" data-url=${full_url}> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa"><i class="fas fa-edit"></i></span></button>`;
    let btnEditMini = `<button type="button" class="btn btn-warning float-right mr-sm-1 btn-sm d-block d-md-none" data-toggle="modal" data-target="#modalEdit" data-tbl="${tbl}" data-id="${id}" data-url=${full_url}> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa"><i class="fas fa-edit"></i></span></button>`;
    return btnEdit + btnEditMini;
};

function btnDeleteDisplay(url_example, id) {
    // Tạo nút btnDelete là link mở ra modalDelete
    if (!url_example) return '';
    if (!url_example) return '';
    let url_components = url_example.split('<>');
    let full_url = url_components[0] + id + url_components[1];
    let btnDelete =  `<button type="button" class="btn btn-danger float-right mr-1 d-none d-md-block" data-toggle="modal" data-target="#modalDelete" data-url=${full_url}> <span data-toggle="tooltip" data-placement="bottom" title="Xóa"><i class="fas fa-trash-alt"></i></span></button>`;
    let btnDeleteMini = `<button type="button" class="btn btn-danger float-right mr-sm-1 btn-sm d-block d-md-none" data-toggle="modal" data-target="#modalDelete" data-url=${full_url}> <span data-toggle="tooltip" data-placement="bottom" title="Xóa"><i class="fas fa-trash-alt"></i></span></button>`;
    return btnDelete + btnDeleteMini;
};

function setCreateModalForm(custom_modal_func=null) {
    // Khởi tạo onsubmit handler cho createModal
    // Dùng hàm custom_modal_func để khởi tạo giá trị
    // Dữ liệu được truyền vào từ nút tạo mới (relatedTarget): url
    $('#modalCreate').on('show.bs.modal', (event) => {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let full_url = button.data('url'); // Extract info from data-* attributes
        let createForm = document.getElementById('modalCreateForm');
        createForm.reset();
        if (custom_modal_func != null) {custom_modal_func();}
        createForm.onsubmit = (event) => {  
            event.preventDefault();
            $.ajax({
                url: full_url,
                method: 'POST',
                data: $('#modalCreateForm').serialize(),
                processData: false,
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                success: () => {
                    showNotification('Tạo thành công', 2)
                },
                error: (xhr, status, error) => {
                    showNotification(HTML_CODE_MESSAGE[xhr.status], 3)
                }
            });
            $('#modalCreate').modal('hide');
        };
    });
}

function setDeleteModalForm() {
    // Khởi tạo onsubmit handler cho deleteModal
    // Dữ liệu được truyền vào từ nút xóa (relatedTarget): url
    $('#modalDelete').on('show.bs.modal', (event) => {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let full_url = button.data('url'); // Extract info from data-* attributes
        let deleteForm = document.getElementById('modalDeleteForm');
        deleteForm.reset();
        deleteForm.onsubmit = (event) => {  
            event.preventDefault();
            $.ajax({
                url: full_url,
                method: 'DELETE',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                success: () => {
                    showNotification('Xóa thành công', 2)
                },
                error: (xhr, status, error) => {
                    showNotification(HTML_CODE_MESSAGE[xhr.status], 3)
                }
            });
            $('#modalDelete').modal('hide');
        };
    });
}

function setEditModalForm(custom_modal_func) {
    // Khởi tạo onsubmit handler cho editModal
    // Lấy dữ liệu của row => dùng hàm custom_modal_func để khởi tạo giá trị
    // Dữ liệu được truyền vào từ nút sửa (relatedTarget): url, id, tbl
    $('#modalEdit').on('show.bs.modal', (event) => {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let full_url = button.data('url'); // Extract info from data-* attributes
        let item_id = button.data('id');
        let tbl_id = button.data('tbl');
        let editForm = document.getElementById('modalEditForm');
        editForm.reset();
        // Extract row info with given id
        row_data = $('#'+tbl_id).DataTable().rows((index, data, node) => {
            return data.id === item_id;
        }).data()[0];
        custom_modal_func(row_data);
        editForm.onsubmit = (event) => {  
            event.preventDefault();
            $.ajax({
                url: full_url,
                method: 'PUT',
                data: $('#modalEditForm').serialize(),
                processData: false,
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                success: () => {
                    showNotification('Sửa thành công', 2)
                },
                error: (xhr, status, error) => {
                    showNotification(HTML_CODE_MESSAGE[xhr.status], 3)
                }
            });
            $('#modalEdit').modal('hide');
        };
    });
}