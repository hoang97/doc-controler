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
        return '';
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
    return cookieValue;
}
const DATATABLE_LANGUAGE={
    "lengthMenu": "Hiển thị _MENU_ bản ghi mỗi trang",
    "zeroRecords": "Không tìm thấy kết quả",
    // "info": "Hiển thị trang _PAGE_ / _PAGES_",
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