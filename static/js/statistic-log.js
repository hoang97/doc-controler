
$(document).ready(function () {
    getLogs(true);
});


function getLogs(initial=false){
    $.ajax({
        type: 'GET',
        url: '/get-logs',
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];

                let displayTableList=[];
                let count=0;
                for (let i in data){
                    count+=1;
                    displayTableList.push(dictToList(data[i],count));
                }
                initTable(displayTableList,initial);
            }
            else{   
                alert("Lỗi status");
            }
            
        })
        .fail(() => {
            alert("Failed");
        });

}   

function initTable(dataSet,initial=false){
    var tbl=  $('#tblLogs');;
    if(initial==true){
        tbl.html('');
        tbl.DataTable({
            data: dataSet,
            columns: [
                { title: "#","width": "5%" },
                { title: "Nội dung" },
                { title: "Liên kết"},
                { title: "Thời gian"},
                { title: "Phòng" },
                { title: "Người thực hiện" },
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

function dictToList(dict,count){
    // "username":log.user.username,
    // "content":log.content,
    // "action_time":log.action_time,
    // "content_type_id":log.content_type_id,
    // "object_id":log.object_id,
    // "object_repr":log.object_repr,
    // "department":log.department.name,
    let arr=[];
    arr.push( [count ] );
    arr.push( [dict['content'] ] );
    let linkATag='';
    if (dict["object_id"]!=''){
        if (dict['content_type_id']==LOG_CONTENT_XFILE || dict['content_type_id']==LOG_CONTENT_NOTE){
            linkATag='<a href="/hsmt/edit-detail?id='+dict["object_id"]+'"> '+dict["object_repr"]+'</a>';
        }
        else if (dict['content_type_id']==LOG_CONTENT_USER){
            linkATag='<a href="/profile?u='+dict["object_id"]+'"> '+dict["object_repr"]+'</a>';
        }
    }
    
    arr.push([ linkATag ]);
    arr.push( [displayDatetime(dict['action_time' ],'long')] );

    arr.push( ([dict['department'] ]) );

    let actorATag='<a href="/profile?u='+dict["username"]+'"> '+dict["username"]+'</a>';
    arr.push( [actorATag] );

    return arr;
}


