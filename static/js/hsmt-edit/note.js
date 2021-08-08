var listNotes=[];
var currentPage=1;
var recoredPerPage=5;
function ReloadNotes(){
    $.ajax({
        type: 'GET',
        url: '/get-notes',
        data: {
            'xfileId':$('#originalXfileId').val()
        },
    })
        .done((resp) => {
            if(resp['status']===0){
                listNotes=resp['data'];
                DisplayNotes(currentPage,recoredPerPage);
            }
            else{
                showNotification(resp['msg']);
            }
            
            
        })
        .fail(() => {
            showNotification("Failed");
        });
}
function DisplayNotes(page,pageSize){
    // [
                //     {"id": 7, 
                //     "title": "1", 
                //     "content": "h", 
                //     "user": {"username": "tp2", "first_name": "trunog phong 2"}, 
                //     "xfile": {"id": 8, "name": "test22", "xfile_type": 1}, 
                //     "status": false, 
                //     "date_created": 
                //     "2021-05-18T03:21:14.538Z",
                //     "date_modified": null
                //   }
                // ]
    let divNhanXet=$('#divNhanXet');
    divNhanXet.html('');
    if (listNotes.length>0){
        $('#divNhanXetFooter').show();
       
    }
    else{
        
        divNhanXet.append($('<p>',{ 'style':'text-align:center;'}).text('Không có nhận xét nào'));
        $('#divNhanXetFooter').hide();
    }
    let totalPage=Math.floor(listNotes.length/pageSize);// 0,1,1 (du 2), 
    totalPage+=1
    if (listNotes.length % pageSize ==0){totalPage-=1;}
    if (totalPage==1){
        $('#btnPreviousNotePage').hide();
        $('#btnNextNotePage').hide();
    }
    $('#pageNumberDisplay').text("Trang "+page +"/"+totalPage);


    let i=(page-1)*pageSize;
    // let countUnfinishNote=0;
    for (i;i<listNotes.length;i++){
        
        note=listNotes[i];
    //     <div class="post">
         //     <div class="user-block">
        //       <img class="img-circle img-bordered-sm" src="{% static 'img/avatar5.png' %}" alt="user image">
        //       <span class="username">
        //         <a href="#">Jonathan Burke Jr.</a>
        //       </span>
        // <span class="badge badge-secondary">New</span>
        //       <span class="description">- 7:45 PM today</span>
        //  <btn class="btn btn-warning float-right" ><i class="fas fa-edit"></i> </btn>
        //     </div>
        //     <!-- /.user-block -->
     //     <p>.....</p>

    //   </div>
        let divPost=$('<div>',{class:"post",style:"padding-bottom: 0px;"});
        let divUserBlock=$('<div>',{class:"user-block",style:" margin-bottom: 0px;"});
        divUserBlock.append($('<img>',{class:"img-circle img-bordered-sm", src:"/static/img/avatar5.png", alt:"user image"}));
        divUserBlock.append(
            $('<span>',{class:"username"}).append($('<a>',{target:"_blank",href:"/profile?u="+note['user']['username']}).text(note['user']['first_name'])).append($('<span>',{class:"float-right",'data-toggle':"modal", 'data-target':"#modalDeleteNote",'data-id':note['id']}).append($('<i>',{class:"fas fa-times"}))).append(
                $('<span>',{class:"float-right mx-2", 'data-toggle':"modal", 'data-target':"#modalAddEditNote",'data-id':note['id']}).append($('<i>',{class:"fas fa-edit"}))
            )
        );

        let statusSpan;
        if (note['status']==true){
            statusSpan=$('<span>',{class:"badge badge-success"}).append($('<i>',{class:"fas fa-check-circle"}));
        }
        else {
            statusSpan=$('<span>',{class:"badge badge-danger"}).append($('<i>',{class:"fas fa-times-circle"}));
            // countUnfinishNote+=1;
        }
        
        divUserBlock.append(
            $('<span>',{class:"description"}).append(statusSpan).append($('<span>').text('('+displayDatetime(note['date_created'])+')'))
            );
        // divUserBlock.append(
        //     $('<btn>',{class:"float-right", 'data-toggle':"modal", 'data-target':"#modalAddEditNote",'data-id':note['id']}).append($('<i>',{class:"fas fa-edit"}))
        // );

        divContent=$('<p>',{style:"white-space: pre-wrap;"}).text(note['content']);

        // #Create new Post
        divPost.append(divUserBlock);
        divPost.append(divContent);
        divNhanXet.append(divPost);

        pageSize-=1;
        if(pageSize==0) {break;}
    }
    // Hiển thị badge
    // $('#xfile-note-tab').append($('<span>',{class:"badge badge-light"}).text(' '+ countUnfinishNote));
    // Initial for display pagination
    ValidateNotePageDisplay();
}
$('#modalAddEditNote').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var noteId = button.data('id'); // Extract info from data-* attributes
    $('#noteId').val(noteId);
    if (noteId!=''){
        // Có id == Chỉnh sửa EDITNG
        $.ajax({
            type: 'GET',
            url: '/get-note-by-id',
            data: {
                'id':noteId
            },
        })
            .done((resp) => {
                if(resp['status']===0){
                    let data=resp['data'];
                    $('#noteTitle').val(data['title']);

                    $('#noteContent').val(data['content']);
                    if(data['status']==true){
                        $('#chkBoxNoteStatus').prop('checked',true);
                    }
                    else{
                        $('#chkBoxNoteStatus').prop('checked',false);

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
    else{
        $('#noteTitle').val("");
        $('#noteContent').val("");
        $('#chkBoxNoteStatus').prop('checked',false);

    }

    
});
$('#btnSaveNote').on('click',function(){
    var data={
        'xfileId':$('#originalXfileId').val(),
        'noteId':$('#noteId').val(),
        'noteTitle':$('#noteTitle').val(),
        'noteContent':$('#noteContent').val(),
        'noteStatus': isCheckBoxChecked("chkBoxNoteStatus")
    }
    $.ajax({
        type: 'POST',
        url: '/add-edit-note',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: data,
    })
        .done((resp) => {
            if(resp['status']===0){
                ReloadNotes();
            }
            else{
                showNotification(resp['msg']);
            }
    
        })
        .fail(() => {
            showNotification("Failed");
        });

});
function NotesPerPages(number){
    recoredPerPage=number;
    DisplayNotes(currentPage,recoredPerPage);
};
function ValidateNotePageDisplay(){
    let totalPage=Math.floor(listNotes.length/recoredPerPage);// 0,1,1 (du 2), 
    totalPage+=1
    if (listNotes.length %recoredPerPage ==0){totalPage-=1;}
    if (totalPage==1){
        $('#btnPreviousNotePage').hide();
        $('#btnNextNotePage').hide();
        return;
    }
    if (currentPage>1){
        $('#btnPreviousNotePage').show();
    }
    else{
        $('#btnPreviousNotePage').hide();
    }
    if (currentPage<totalPage){
        $('#btnNextNotePage').show();
    }
    else{
        $('#btnNextNotePage').hide();
    }
}
function ChangeNotePage(isGoingPrevious){
   
    if (isGoingPrevious==1){
        if (currentPage>1){currentPage-=1}

        DisplayNotes(currentPage,recoredPerPage);
    }
    else{
        currentPage+=1;
        DisplayNotes(currentPage,recoredPerPage);
    }
};