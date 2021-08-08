const TARGET_TYPES=[
    ['1','target-direction'],
    ['2','target-group'],
    ['3','target-area'],
];
const selectTargetTypePrefix='#select-targettype-';
var isEditting=false;

$(document).ready(function () {
    for (let i in TARGET_TYPES){
        InitTargetTypes(TARGET_TYPES[i][0]);
    }
    if ($('#xfileId').val() !="" ) {
        isEditting=true;
        $('#divTargetTypes').attr('class','col-lg-6');
        InitXfile($('#xfileId').val());
    }

});
function resolveTargetTypeToString(targetType){
    for (let i in TARGET_TYPES){
        if (targetType==TARGET_TYPES[i][0]){
            return TARGET_TYPES[i][1];
        }
    }   
}
function displaySelect2Options(dataDisplay,targetType){
    
    let selectElement=$(selectTargetTypePrefix+targetType);
    selectElement.html('');
    for (let i=0;i<dataDisplay.length;i++){
        let newOption = new Option(dataDisplay[i].text, dataDisplay[i].id, false, false);
        selectElement.append(newOption).trigger('change');
    }
}
function InitTargetTypes(targetType){
    $.ajax({
        type: 'GET',
        url: '/get-target-type-by-type',
        data:{'targetType':targetType}
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                    // [
                    //  {"id": 1, "name": "dsa", "description": "das"}, 
                    //  {"id": 2, "name": "dsad", "description": "dsa"}
                    // ]
                   // {
                    //     id: 1,
                    //     text: 'Phạm Hoàng'
                    // },
                let dataDisplay=[];
                for (let i=0;i<data.length;i++){
                    // {"id": 1, "name": "dsa", "description": "das"}, 
                    dataDisplay.push({
                        id:data[i]['id'],
                        text: data[i]['name'],
                    });
                }   
                displaySelect2Options(dataDisplay,targetType);

            }
            else{   
                alert("Lỗi status");
            }
            
        })
        .fail(() => {
            alert("Failed");
        });
}   
$( "#btnSaveNewTargetType" ).on( "click", function() {
    // Validation
    var targetType=$('#targetType').val();
    if (targetType=='0'){
        $('#optTargetTypeFeedback').show();
        return; 
    }
    $('#optTargetTypeFeedback').hide();
    
    // End Validation
    let data={
        'target-type':targetType,
        'target-id':$('#targetTypeId').val(),
        'target-name':$('#targetTypeName').val(),
        'target-desc':$('#targetTypeDesc').val(),
    }
    $.ajax({
        type: 'POST',
        url: '/add-edit-target-type',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
    .done((resp) => {
        if(resp['status']===0){
            let data=resp['data'];
            let selectElement=$(selectTargetTypePrefix+targetType);
            let newOption = new Option(data['name'], data['id'], false, false);
            selectElement.append(newOption).trigger('change');

          

            showNotification(msg="Thêm mới hướng - nhóm - địa bàn thành công");
        }
        else{
            showNotification(msg="Lỗi status");

        }

    })
    .fail(() => {
        showNotification(msg="Failed");
    });
        $('#modalAddTargetType').modal('hide');

});

$('#btnCreateEdit').on('click', function (){
   //validation
    var xName = $('#xfileName').val();
    var xfileTypeError = $('#xfileType').val();

     if (xName==''){
        $('#nameError').show();        
         return;
     };
     $('#nameError').hide();	
     if (xfileTypeError == '0'){
        $('#xfileTypeError').show();        
        return;
    };
    $('#xfileTypeError').hide();
    let dataSource={
        'xfileType':$('#xfileType').val(),
        'xfileName':$('#xfileName').val(),
        'xfileDescription':$('#xfileDescription').val(),
        'xfileCode':$('#xfileCode').val(),
        'targetDirection':getIdFromSelect2(TARGET_TYPES[0][0]) ,
        'targetGroup': getIdFromSelect2(TARGET_TYPES[1][0]) ,
        'targetArea': getIdFromSelect2(TARGET_TYPES[2][0]) ,
    }
    if (isEditting==true){
        dataSource['xfileId']=$('#xfileId').val();
        dataSource['edit_note']=$('#edit_note').val();
    }
    let data={
        'data':JSON.stringify(dataSource)
    };
    

    $.ajax({
        type: 'POST',
        url: '/add-edit-hsmt',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
    .done((resp) => {
        if(resp['status']===0){
            if (isEditting==false){
                showNotification(msg="Thêm mới thành công");
                window.location.href="/hsmt/list";
            }
            else{
                showNotification(msg="Chỉnh sửa thành công");

            }
            
        }
        else{
            showNotification(msg="Lỗi status");

        }

    })
    .fail(() => {
        showNotification(msg="Failed");
    });


}); 
function getIdFromSelect2(targetType){
    let data=$(selectTargetTypePrefix+targetType).select2('data');
    let ret =[];
    for (let i in data){
        ret.push(data[i]['id']);
    }
    return ret;
}
function InitXfile(xfileId){
    $.ajax({
        type: 'GET',
        url: '/get-xfile-by-id',

        data: {
            'id':xfileId,
            'onlyXfileCover':1
        },
    })
        .done((resp) => {
            if(resp['status']===0){
                let data=resp['data'];
                // 'id':xfile.id,
                // 'name':xfile.name,
                // 'date_created':xfile.date_created,
                // 'date_modified':xfile.date_modified,
                // 'edit_note':xfile.edit_note,
                // "status":xfile.status,
                // 'values':values,
                // "xfile_type":xfile.xfile_type,
                // 'targetTypes':{
                //     'target-direction':[tmp for tmp in xfile.target_direction.all().values()],
                //     'target-group':[tmp for tmp in xfile.target_group.all().values()],
                //     'target-area':[tmp for tmp in xfile.target_area.all().values()]
                // }, 
                // 'user': User.objects.filter(username=xfile.user).values("username","first_name")[0]
                $('#xfileType').val(data['xfile_type']).prop( "disabled", true );;
                $('#xfileName').val(data['name']);
                $('#xfileCode').val(data['code']);
                $('#xfileDescription').val(data['description']);
                $('#date_created').val( displayDatetime(data['date_created']) );
                $('#edit_note').val(data['edit_note']);
                $('#user_creator').val(data['user']['first_name']);
                let targetTypes=data['targetTypes'];
                for (let i in TARGET_TYPES){
                    let targetType=targetTypes[TARGET_TYPES[i][1]]; //get targetTypes['target-direction']
                    let listValueForSelection=[];
                    for(let j in targetType){
                        listValueForSelection.push(targetType[j]['id']);
                    }
                    let selectElement=$(selectTargetTypePrefix+TARGET_TYPES[i][0]);
                    selectElement.val(listValueForSelection);
                    selectElement.trigger('change'); // Notify any JS components that the value changed
                }
            }
            else{
                showNotification(resp['msg']);
            }
            
            
        })
        .fail(() => {
            showNotification("Failed");
        });
}