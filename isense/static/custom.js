$(document).ready(function(){

    $(document).on("change", ".device_id", function(){

      var user_id = $(".userId").val();
      var device_id = $(".device_id").val();

      $(".loader").show();

      $.ajax({
        url: "/api/get_meta_sample_data/", 
        type: 'POST',
        data: JSON.stringify({ "user_id": user_id, "device_name" : device_id}) ,
        contentType: "application/json",
        success: function(response){

          $('.sample_id').selectpicker('destroy');
          $(".sample_id").find("option").remove();
          var available_length;
          $.each(response.data, function(i, sample) {
            // console.log(sample.sample_set_id)
            $('.sample_id').append(`<option value="`+sample.sample_set_id+`">`+sample.sample_set_id+`</option>`);
            available_length++
          });
          // initializing selectpicker
          $('.sample_id').selectpicker({
            size: available_length
          });

          setTimeout(function(){
            $(".loader").hide();
          }, 500);

        },
        error: function () {
          $(".loader").hide();
            alert("error");
        }
      });
    });

    $(document).on("click", "#sample_graph", function(){
     
      var user_id = $("#userId").val();
      var device_id = $("#device_id").val();
      var sample_set_id = $("#sample_id").val();
      var sensor_id = $("#senser_id").val();

      if(device_id == "" || sample_set_id == "" || sensor_id == ""){
        alert("please select the dropdown")
        return false;
      }

      $(".loader").show();
      $('#sample_graph').prop('disabled',true);

      $.ajax({
        url: "api/get_sample_data/", 
        type: 'POST',
        data: JSON.stringify({ "user_id": user_id, "device_name" : device_id, "sensor": sensor_id, "sample_set_id": sample_set_id}) ,
        contentType: "application/json",
        success: function(response){

          var sample_array_data = response.data;

          $.each(sample_array_data, function(i, sampledata) {
            // arr.push([i,sampledata[0]]);
            var data = sampledata[0];
            sampledata[0]=i;
            sampledata[1]=data;
          });

          sample_graph_data(sample_array_data, sensor_id);
          // sample_Scatter_graph_data(sample_array_data, sensor_id);
          // console.log(sample_array_data)
          
          setTimeout(function(){
            $(".loader").hide();
            $('#sample_graph').prop('disabled',false);
          }, 500);
          
        },
        error: function () {
          $(".loader").hide();
          $('#sample_graph').prop('disabled',false);
          alert("error");
        }
      });
    });

    function sample_graph_data(sample_array_data, sensor_id){

      google.charts.load('current', {packages: ['corechart', 'line']});
      google.charts.setOnLoadCallback(drawBackgroundColor);

      function drawBackgroundColor() {
          
        var data = new google.visualization.DataTable();
        data.addColumn('number', 'X');
        data.addColumn('number', "");
  
        data.addRows(sample_array_data);
  
        var options = {
          title: "Line Graph for " + sensor_id,
          hAxis: {
            title: 'Sample'
          },
          vAxis: {
            title: sensor_id
          },
          backgroundColor: '#fffff'
        };
  
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    };

//    function sample_Scatter_graph_data(sample_array_data, sensor_id){
//
//      google.charts.load('current', {'packages':['scatter']});
//      google.charts.setOnLoadCallback(drawChart);
//
//      function drawChart () {
//
//        var data = new google.visualization.DataTable();
//        data.addColumn('number', "pca1");
//        data.addColumn('number', "");
//
//        data.addRows(sample_array_data);
//
//        var options = {
//          width: 1000,
//          height: 400,
//          title: "PCA for " + sensor_id,
//          hAxis: {title: "principal component 1"},
//          vAxis: {title: 'principal component 2'},
//          backgroundColor: '#fffff',
//          legend: 'none'
//        };
//
//        var chart = new google.charts.Scatter(document.getElementById('chart_div_pca'));
//
//        chart.draw(data, google.charts.Scatter.convertOptions(options));
//      }
//    };

     $(document).on("click", ".pca_graph", function(){

      var user_id = $("#userId").val();
      var device_id = $("#device_id").val();
      var sample_set_id = $("#sample_id").val();
      var sensor_id = $("#senser_id").val();

      if(device_id == "" || sample_set_id == "" || sensor_id == ""){
        alert("please select the dropdown")
        return false;
      }
      alert('Do not  refresh page, Please wait 5 minutes.... ')
      $('#pca_graph').prop('disabled',true);
      $(".loader").show();

      $.ajax({
        url: "api/get_sample_data_pca_graph/",
        type: 'POST',
        timeout: 600000,
        data: JSON.stringify({ "user_id": user_id, "device_name" : device_id, "sensor": sensor_id, "sample_set_id": sample_set_id}) ,
        contentType: "application/json",
        success: function(response){
         console.log(response)
            $(".legend_list").html("");

            var sample_array_data = response.data;
            var sample_legend_data = response.legend_list;
            var sample_variance_list = response.variance_list; 
            var arr=[]

            // $.each(sample_array_data, function(i, sampledata) {
            //   arr.push([sampledata[0] , sampledata[1], sampledata[2]]);
            // });

            setTimeout(function(){
              $(".loader").hide();
            }, 500);

            $(".back_color").css("background-color", "white");

            sample_Scatter_graph_data(sample_array_data, sensor_id, sample_variance_list);

            $(".legendUI").show();
            $.each(sample_legend_data, function(i, legendList_item) {
  
              var rowHtml = `<li><span style="background-color:` +legendList_item.color+`"></span>
                                `+legendList_item.text +`</li>` ;
    
              $(".legend_list").append(rowHtml);
            });

            setTimeout(function(){
              $('#pca_graph').prop('disabled',false);
            }, 500);

        },
        error: function () {
          $(".loader").hide();
          $('#pca_graph').prop('disabled',false);
          alert("error");
        }
      });
    });

    function sample_Scatter_graph_data(sample_array_data, sensor_id, sample_variance_list){

          google.charts.load('current', {'packages':['corechart']});
          google.charts.setOnLoadCallback(drawChart);

          function drawChart() {
              console.log(sample_array_data)
              var data = google.visualization.arrayToDataTable(sample_array_data);

              var options = {
                  title: 'PCA for ' + sensor_id,
                  hAxis: {title: 'First Component ( ' +sample_variance_list[0].toFixed(2)+ "% )" },
                  vAxis: {title: 'Second Component ( ' +sample_variance_list[1].toFixed(2)+ "% )"},
                  legend: 'none',
                  tooltip: { isHtml: true},
              };

          var chart = new google.visualization.ScatterChart(document.getElementById('chart_div_pca'));

          chart.draw(data, options);
        }
    };


  });

