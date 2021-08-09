
const XFILE_TYPES=[
    [1,'Trang mạng'],
    [2,'Tổ chức'],
    [3,'Đối tượng']
];
const XFILE_STATUS=[
    [1,'Khởi tạo','gray','Hồ sơ đang được khởi tạo bởi Trợ lý',0],
    [2,'Đang kiểm định','info','Hồ sơ đang trong quá trình kiểm định',0],
    [3,'Đang duyệt','warning','Hồ sơ đang chờ duyệt bởi Trưởng phòng',0],
    [4,'Hoàn tất','success','Hồ sơ đã được duyệt',0],
];
$('document').ready(function () {
    getData();
    // addInforUser();
    // addInforTargetType();
    // addInforHSMT();
 });

function getData(){
    $.ajax({
        type: 'GET',
        url: '/statistic-api',
        // headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
        .done((resp) => {
            if(resp['status']===0){
                //getinfor
                let data=resp['data'];

                               // {"xfiles": 
                //     [
                //         {"status": 2, "department": "Ph\u00f2ng 5"},
                //          {"status": 1, "department": "Ph\u00f2ng 5"}, 
                //          ...
                //          , 
                //     ]
                //         "users_count": 39,
                //          "target_types_count": 11
                // }
                if(data['ct']){
                    $('#statisticXfileAll').show();
                } 
                else{
                    $('#statisticXfileAll').hide();

                }
                // let numberfUsers = data['users_count'];
                // $('#numerofUsers').text(numberfUsers);
                // let numberofTargets = data['target_types_count'];
                // $('#numberofTargets').text(numberofTargets);
                //data draw chart
                //trangthai, giatri trang thai
        
                trangthai=[];
                giatritrangthai=[];  
                for(let i=0;i< data['xfiles'].length;i++){
                    for (let j=0;j<XFILE_STATUS.length;j++){
                        if (data['xfiles'][i]['status'] == XFILE_STATUS[j][0]){
                            // Nếu trạng thái hoàn tất thì chỉ tính cho original =1
                            XFILE_STATUS[j][4]+=1;
                            if (data['xfiles'][i]['status']==4 && data['xfiles'][i]['original']==false){
                                XFILE_STATUS[j][4]-=1;
                            }
                            break
                        }
                    }         
               }    
               //add values to array

                for(let i =0; i< XFILE_STATUS.length;i++){
                    trangthai.push(XFILE_STATUS[i][1]);
                    giatritrangthai.push(XFILE_STATUS[i][4]);
                }
                let numberofCompletedXfiles=XFILE_STATUS[3][4];
                let numberofInitialXfiles=XFILE_STATUS[0][4];
                let numberofInCheckingProcessXfiles=XFILE_STATUS[1][4];
                let numberofInApprovingProcessXfiles=XFILE_STATUS[2][4];
                $('#numberofInitialXfiles').html(numberofInitialXfiles);
                $('#numberofInCheckingProcessXfiles').html(numberofInCheckingProcessXfiles);
                $('#numberofInApprovingProcessXfiles').html(numberofInApprovingProcessXfiles);
                $('#numberofCompletedXfiles').html(numberofCompletedXfiles);
                // #tblLogs

                let logs=data['logs'];
                reloadNewestActivities(logs);
            

            // initXfileTable(displaytable);
            if(data['ct']){
                createTable(data);
                datatargettype = data['target_type'];
                drawpolarArea(datatargettype);  
                // var values = $.map(target_area, function(value, key) { return value });
                // var keys = $.map(target_area, function(value, key) { return key });
                target_area = data['target_area']
                target_area_data = data['target_area_data']
                drawbarChart(target_area,target_area_data);
                // 
                target_group = data['target_group']
                target_group_data= data['target_group_data']
                drawbarChartGroupTarget(target_group,target_group_data);
                target_direction=data['target_direction']
                target_direction_data = data['target_direction_data']
                drawradarChart(target_direction,XFILE_TYPES,target_direction_data)
                
                $('#logActivity').hide();

            }

            else{
                $('#thongke').hide();
                $('#chartThongke').hide();
                $('#diabanCt').hide();
                $('#statisticXfileAll').hide();
            }
            //draw pie chart
            drawChart(trangthai,giatritrangthai);
            //draw polar chart
            // }
            // else{   
            //     alert("Lỗi status");
            // }
            




            }
        })
        .fail(() => {
            alert("Failed");
        });
}

function reloadNewestActivities(dataSet){

    var tbl=$('#tblNewestActivities');
    tbl.html('');
    for (let i=0; i<dataSet.length;i++){
        let oneLog=dataSet[i];

        let tableRow=$('<tr>');
        
        let aTag='';
        let hrefLink='';
        if (oneLog['object_id']=='' || oneLog['object_id']==null ){
            aTag=oneLog['content'];
        }
        else{
            for (let j in LOG_CONTENT_TYPE){
                if (oneLog['content_type_id'].toString()==LOG_CONTENT_XFILE){
                    hrefLink='/hsmt/edit-detail?id='+oneLog['object_id'];
                    aTag=$('<a>',{href:hrefLink}).text(oneLog['content']);
                    break;
                }
                else if (oneLog['content_type_id'].toString()==LOG_CONTENT_NOTE){
                    hrefLink='/hsmt/edit-detail?id='+oneLog['object_id'];
                    aTag=$('<a>',{href:hrefLink}).text(oneLog['content']);
                    break;
                }
                else if (oneLog['content_type_id'].toString()==LOG_CONTENT_USER){
                    hrefLink='/profile?u='+oneLog['object_repr'];
                    aTag=$('<a>',{href:hrefLink}).text(oneLog['content']);
                    
                    break;
                }
            }
        }
        tableRow.append($('<td>').append(aTag));
        tableRow.append($('<td>').text(displayDatetime(oneLog['action_time'])));
        tableRow.append($('<td>').append($('<a>',{href:'/profile?u='+oneLog['username']}).text(oneLog['username'])));
        if (hrefLink!=''){
            tableRow.append($('<td>').append($('<a>',{href:hrefLink,class:"btn btn-info btn-sm"}).append($('<i>',{class:"fas fa-eye"}))));
        }
        else{
            tableRow.append($('<td>'));
        }
        
        tbl.append(tableRow);
    }
}
function createTable(data){
    dataDepartment = [
        //Phòng,khởi tạo, Đang kiểm định, đang duyệt, hoàn tất, tổng số,tiến độ.
        ['Phòng 1',0,0,0,0,0],
        ['Phòng 2',0,0,0,0,0],
        ['Phòng 3',0,0,0,0,0],
        ['Phòng 4',0,0,0,0,0],
        ['Phòng 5',0,0,0,0,0],
        ['Phòng 6',0,0,0,0,0]
    ];
    for(let i=0;i< data['xfiles'].length;i++){
        for(let j=0;j<dataDepartment.length;j++){
                if(data['xfiles'][i]['department']==dataDepartment[j][0]){
                    for (let h=0;h<XFILE_STATUS.length;h++){
                        if (data['xfiles'][i]['status'] == XFILE_STATUS[h][0]){
                            dataDepartment[j][h+1]+=1;
                            dataDepartment[j][dataDepartment.length-1]+=1;                                }
                    }                     
               }
        
        }

    }
    
    for(let i=0;i<dataDepartment.length;i++){
        $('#statisticXfileAll tbody').append(
            "<tr>"
            +"<td>"+(i+1)+"</td>"
            +"<td>"+dataDepartment[i][0]+"</td>"
            +"<td>"+dataDepartment[i][5]+"</td>"
            +"<td><span class='badge bg-danger'>"+dataDepartment[i][1]+"</span></td>"
            +"<td><span class='badge bg-warning'>"+dataDepartment[i][2]+"</span></td>"
            +"<td><span class='badge bg-info'>"+dataDepartment[i][3]+"</span></td>"
            +"<td><span class='badge bg-success'>"+dataDepartment[i][4]+"</span></td>"

          +"</tr>"


        );
    }
        
}





function drawChart(trangthai,giatritrangthai) {
    /* ChartJS
     * -------
     * Here we will create a few charts using ChartJS
     */
    var donutData        = {
      datasets: [
        {
          data: giatritrangthai,
          backgroundColor : [ '#d2d6de', '#f56954' , '#f39c12','#00a65a' ],
        }
      ],
      labels: 
        trangthai,
    }
    //------------- 
    //- PIE CHART -
    //-------------
    // Get context with jQuery - using jQuery's .get() method.
    var pieChartCanvas = $('#pieChart').get(0).getContext('2d')
    var pieData        = donutData;
    var pieOptions     = {
      maintainAspectRatio : false,
      responsive : true,
      legend: {
        display: true
      },
      plugins: {
        labels: {
          render: 'value'
        }
      }
    }
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(pieChartCanvas, {
      type: 'pie',
      data: pieData,
      options: pieOptions
    })
    let type='pie';

  }
  function drawpolarArea(datatargettype){
    var ctx = $("#chart-line");
    backgroundColor= dynamicColors(datatargettype);
    var maxy = Math.max.apply(null,datatargettype)+2;
    var myLineChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: ["Trang Mạng", "Tổ chức", "Đối tượng"],
            datasets: [{
                data: datatargettype,
                // backgroundColor: ["rgba(255, 0, 0, 0.5)", "rgba(100, 255, 0, 0.5)", "rgba(200, 50, 255, 0.5)", "rgba(0, 100, 255, 0.5)"]
                backgroundColor: backgroundColor,
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Phân loại HSMT'
            },
            scale:{
                ticks:{
                    max:maxy
                }   
            }
        }
    });
  }


//radarchart for group directions


function drawradarChart(target_direction,XFILE_TYPES,target_direction_data){
    var ctx = $("#radarChartInfor");
    // backgroundColor= dynamicColors(datatargettype);
    var keys = $.map(target_direction_data, function(value, key) { return key });
    var values = $.map(target_direction_data, function(value, key) { return value });
    var maxy = Math.max.apply(null,values)+2;
    var dataset = []
    for(i=0;i<keys.length;i++){
         randomlist = ['1']
         var backgroundColorRGB,backgroundColorRGBA=dynamicColorsrgb();
         dataz= {
               label:XFILE_TYPES[i][1],

               fill: true,
               data:target_direction_data[keys[i]],
               backgroundColor:backgroundColorRGBA,
               borderColor:backgroundColorRGB,
                pointHoverBackgroundColor: '#fff',
                pointBorderColor: '#fff',
                pointHoverBorderColor:backgroundColorRGB,
                pointLabelFontSize: 40
                
        }
        dataset.push(dataz)
    }
    // datasets: [{
        // label: 'My First Dataset',
        // data: [65, 59, 90, 81, 56, 55, 40],
        // fill: true,
        // backgroundColor: 'rgba(255, 99, 132, 0.2)',
        // borderColor: 'rgb(255, 99, 132)',
        // pointBackgroundColor: 'rgb(255, 99, 132)',
        // pointBorderColor: '#fff',
        // pointHoverBackgroundColor: '#fff',
        // pointHoverBorderColor: 'rgb(255, 99, 132)']    
    var myradarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: target_direction,
            datasets: dataset,
            
        },
        options: {
            title: {
                display: true,
                text: 'Hướng HSMT'
            },
            scale:{
                ticks:{
                     max:maxy,
                     callback: function(value) {if (value % 1 === 0) {return value;}}
                 }   
             },
             elements: {
                line: {
                  borderWidth: 3
                }
              }
          
        }
    });
  }







  //bar chart for target area
  function drawbarChart(target_area,target_area_data){
    var ctx = $("#barChart");
    backgroundColor= dynamicColors(target_area_data);
    var maxy = Math.max.apply(null,target_area_data)+2;
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: target_area,
            datasets: [{
                data: target_area_data,
                backgroundColor: backgroundColor,
                borderColor: backgroundColor,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                responsive:true,
                maintainAspectRatio:false,
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        max:maxy,
                        callback: function(value) {if (value % 1 === 0) {return value;}}
                    }
                }],
                xAxes: [{
                    barPercentage: 0.4,
                        ticks:{
                            fontSize:12,
                            fontColor: 'black',
                            fontStyle:'normal'
                        }

                }],

             
            },
            legend:{
                display:false
            },
            plugins: {
                labels: {
                  render: 'value'
                }
              }
        
        }
    });
  }
//bar chart phân chia nhóm mục tiêu
function drawbarChartGroupTarget(target_group,target_group_data){
    var ctx = $("#barChartphanchianhommuctieu");
    backgroundColor= dynamicColors(target_group_data);
    var maxy = Math.max.apply(null,target_group_data)+2;
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: target_group,
            datasets: [{
                data: target_group_data,
                backgroundColor: backgroundColor,
                borderColor: backgroundColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive:true,
            maintainAspectRatio:false,
            scales: {

                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        max:maxy,
                        callback: function(value) {if (value % 1 === 0) {return value;}}
                    }
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    ticks:{
                        fontSize:12,
                        fontColor: 'black',
                        fontStyle:'normal'
                    }

                }],

             
            },
            legend:{
                display:false
            },
            plugins: {
                labels: {
                  render: 'value'
                }
              }
        
        }
    });
  }
function dynamicColors(dataset) {
    backgroundColor=[];
    for(let i=0;i<dataset.length;i++){
        let r = Math.floor(Math.random() * 255);
        let g = Math.floor(Math.random() * 255);
        let b = Math.floor(Math.random() * 255);
        backgroundColor.push("rgba(" + r + "," + g + "," + b + ", 0.5)")
    }

    return backgroundColor;
}


function dynamicColorsrgb() {
    let r = Math.floor(Math.random() * 255);
    let g = Math.floor(Math.random() * 255);
    let b = Math.floor(Math.random() * 255);
    let backgroundColorRGB="rgb(" + r + "," + g + "," + b+")"
    let backgroundColorRGBA="rgb(" + r + "," + g + "," + b +", 0.3)"
    return backgroundColorRGB,backgroundColorRGBA;
}
