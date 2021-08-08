
const XFILE_TYPE=[
    [1,'Webpage'],
    [2,'Organization'],
    [3,'Person']
];
const XFILE_STATUS=[
    [1,'Khởi tạo','secondary','Hồ sơ đang được khởi tạo bởi Trợ lý'],
    [2,'Đang kiểm định','info','Hồ sơ đang trong quá trình kiểm định'],
    [3,'Đang duyệt','warning','Hồ sơ đang chờ duyệt bởi Trưởng phòng'],
    [4,'Hoàn tất','success','Hồ sơ đã được duyệt'],
];

$(document).ready(function () {
   getXfiles(initial=true);

});


function getXfiles(initial=false){
    $.ajax({
        type: 'GET',
        url: '/get-xfiles',
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
        // [
        //     {"id": 1, "name": "hstm1", "date_created": "2021-05-10T09:39:38.480Z", "date_modified": null, "edit_note": null, "status": 1, "xfile_type": 1, "user_id": null, "department_id": null},
        //      {"id": 2, "name": "hstm2", "date_created": "2021-05-10T02:40:51.453Z", "date_modified": null, "edit_note": null, "status": 1, "xfile_type": 1, "user_id": null, "department_id": null}
        // ]
                let displayTableList=[[],[],[]];
                let count=[0,0,0];
                for (let i in data){
                    for (let j in XFILE_TYPE){
                        if(data[i]['xfile_type']==XFILE_TYPE[j][0]){
                            count[j]+=1;
                            displayTableList[j].push(dictXfileToList(data[i],count[j]));
                            break;
                        }
                    }
                    
                }
                initXfileTable(displayTableList,initial);
            }
            else{   
                alert("Lỗi status");
            }
            
        })
        .fail(() => {
            alert("Failed");
        });
}
function initXfileTable(dataSet,initial=false){
    for (let i in XFILE_TYPE){
        let xfileTableElement=$('#tbl'+XFILE_TYPE[i][1]);
        if(initial==true){
            xfileTableElement.html('');
            //  All DataString Tables: https://tablepress.org/extensions/change-datatables-strings/
            xfileTableElement.DataTable( {
                data: dataSet[i],
                columns: [
                    { title: "#","width": "5%" },
                    { title: "Tên Hồ sơ","width": "20%" },
                    { title: "Ngày tạo" },
                    { title: "Ngày sửa" },
                    // { title: "Người tạo",'overflow': 'hidden','text-overflow': 'ellipsis' },
                    { title: "Người chỉnh sửa","width": "15%" },
                    { title: "Người kiểm định","width": "15%" },
                    { title: "Phòng" },
                    { title: "Trạng thái" },
                    { title: "","width": "12%" },
                    // { title: "Start date" },
                    // { title: "Salary" }
                ],
                "language": DATATABLE_LANGUAGE
            } );
        }
        else
        {
            xfileTableElement.dataTable().fnClearTable();
            if (dataSet[i].length>0){
                xfileTableElement.dataTable().fnAddData(dataSet[i]);
            }
        }
     
    }
   
}

function dictXfileToList(dict,count){
    
    let arr=[];
    arr.push( [ count] );
    let hrefXfile='';
    if(dict['ct']){
        hrefXfile= '/hsmt/detail'+"?id="+dict['id'];
    } else {
        hrefXfile= '/hsmt/edit-detail'+"?id="+dict['id'];
    }
    let nameATag='<a href="'+hrefXfile+'">'+dict['name']+' </a>'

    //Push to Datatables
    arr.push( [ nameATag] );
    arr.push( [displayDatetime(dict['date_created']) ] );
    arr.push( [displayDatetime(dict['date_modified']) ] );
    let txtEditors='';
    let txtCheckers='';
    let requestUser=$('#request-username').val();
    let requestEditorUser=$('#request-username').val();

    for (let i in dict['editors']){
        if (i!=0)   {txtEditors+=',';}
        txtEditors+='<a href="/profile?u='+dict['editors'][i]['username']+'"> '+dict['editors'][i]['first_name']+'</a>';
        if (requestEditorUser==dict['editors'][i]['username']){
            requestEditorUser=true;
        }
    }


    for (let i in dict['checkers']){
        if (i!=0)   {txtCheckers+=',';}
        txtCheckers+='<a href="/profile?u='+dict['checkers'][i]['username']+'"> '+dict['checkers'][i]['first_name']+'</a>';
        if (requestUser==dict['checkers'][i]['username']){
            requestUser=true;
        }
    }
    arr.push( [txtEditors] );

    arr.push( [txtCheckers] );

    arr.push( [dict['department']] );

    for (let i in XFILE_STATUS){
        if (XFILE_STATUS[i][0]==dict['status']){
            let spanTag='<span class="badge badge-'+XFILE_STATUS[i][2]+' "  data-toggle="tooltip" data-placement="bottom" title="'+XFILE_STATUS[i][3]+'">'+XFILE_STATUS[i][1]+'</span>';
            arr.push([spanTag]);
            break;
        }
    }
    
   
    
        // <button type="button" class="btn btn-warning" data-toggle="modal" data-target="#modalAddTargetType" data-id="1" data-type="target-direction">Sửa</button>
        // <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#modalDelete" data-id="1" data-type="target-direction">Xoá</button>
    
    let btnDetail='<a  class="btn btn-warning float-right" href="'+hrefXfile+'"> <span data-toggle="tooltip" data-placement="bottom" title="Chỉnh sửa nội dung HSMT"><i class="fas fa-edit"></i></span></a>'
    let btnDuplicate='';
    let btnXoa = '';
    if (dict['duplicate']){
        btnDuplicate='<a  class="btn bg-purple float-right" href="/hsmt/edit-detail?id='+dict['duplicate']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xem bản sao của HSMT"><i class="far fa-copy"></i></span></a>'
    }
    if (requestUser==true){
        btnDetail='<a  class="btn btn-info float-right" href="'+hrefXfile+'"> <span data-toggle="tooltip" data-placement="bottom" title="Kiểm định HSMT"><i class="fas fa-search"></i></span></a>'
    }
    if (requestEditorUser==true){
        btnXoa='<button type="button" class="btn btn-danger float-right" data-toggle="modal" data-target="#modalDelete" id="rowDelete-'+dict['id']+'" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xoá bản ghi"<i class="fas fa-trash-alt"></i></span></button>'
    }
    // let btnXoa='<button type="button" class="btn btn-danger" data-toggle="modal" data-target="#modalDelete" id="rowDelete-'+dict['id']+'" data-id="'+dict['id']+'"> <span data-toggle="tooltip" data-placement="bottom" title="Xoá bản ghi"<i class="fas fa-trash-alt"></i></span></button>'
    // arr.push(btnSua+btnXoa);
    arr.push(btnXoa+btnDetail+btnDuplicate);
    return arr;
}
$('#modalDelete').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var XfileId = button.data('id'); // Extract info from data-* attributes
    // Đặt option = 0: Chọn... --> Validate yêu cầu người dùng phải chọn Loại mục tiêu
    // var xfileStatusId = button.data('typestatus');
    let deleteQuery='DeleteXfile("'+XfileId+'");';
    $('#btnDelete').attr('onclick',deleteQuery);
    
});

function DeleteXfile(XfileId){
    let data={
        'id':XfileId
    }
    $.ajax({
        type: 'POST',
        url: '/delete-xfile-by-id',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                // getTargetTypes(XfileId);
                getXfiles();
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