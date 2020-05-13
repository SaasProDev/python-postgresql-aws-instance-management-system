
{% load frontend_extras %}

<script type="text/javascript">
  // JQuery

  // $(function () {
  //   var progressUrl = "{% url 'celery_progress:task_status'  task_id %}",
	 //    progressBarId = "{{ model }}-progress-bar-{{ uuid }}";
  //   CeleryProgressBar.initProgressBar(progressUrl, {
  //                           progressBarId: progressBarId,
  //                       } )
  // });



	// // JQuery
	// $(function () {
	//   var progressUrl = "{% url 'celery_progress:task_status'  task_id %}";
	//   CeleryProgressBar.initProgressBar(progressUrl, progressBarId='provider-progress-bar-{{ uuid }}')
	// });

	// //


  // function fetchdata(){
  //  $.ajax({
  //   url: "{% url 'provider-detail'  pk %}",
  //   type: 'get',
  //   dataType: 'json',
  //   success: function(data){
  //    // Perform operation on return value
  //    console.log(data.status);
  //   },
  //   complete:function(data){
  //    setTimeout(fetchdata,5000);
  //   }
  //  });
  // }

  // $(function(){
  //  setTimeout(fetchdata,5000);
  // });




// var id = setTimeout(function(){alert('hi');}, 3000);
// clearTimeout(id);




// var timeoutId = setTimeout(function() {
//   $("#subscribe-floating-box").animate({"height": "toggle"}, { duration: 300 });
// }, 3000);

// $('#subscribe-field').focus(function(){
//   clearTimeout(timeoutId);
// });


// $( "#{{ model }}-progress-bar-{{ uuid }}" ).css('width',0 + "%");


// function progress_bar_move_{{ pk }}() {
//   var elem = document.getElementById("{{ model }}-progress-bar-{{ uuid }}");
//   // console.log( elem.style.width.replace('%','') );
//   var width = parseInt( elem.style.width.replace('%','') );
//   console.log( width );
//   var id = setInterval(frame, 1000);
//   function frame() {
//     if (width >= 80) {
//       clearInterval(id);
//     } else {
//       width = width + Math.floor((Math.random() * 5) + 1); 
//       elem.style.width = width + '%'; 
//     }
//   }
// }






var timeoutId_{{pk}} = setTimeout(function() {
  
  $.ajax({
   url: "{% url model|concatenate:'-detail'  pk %}",
   type: 'get',
   dataType: 'json',
   beforeSend: function () {

         // $('#ajax-button').attr('disabled', true);
         // $('#ajax-container').html('');
         // addSpinner($('#ajax-container'));
         // var width=Math.floor((Math.random() * 70) + 1) //(1/5*100);

         $( "#{{ model }}-spinner-{{ uuid }}" ).html('<span class="spinner spinner-xs spinner-inline {{ model }}-spinner-{{ uuid }}" role="status" aria-hidden="true"></span>');

         $( "#{{ model }}-progress-description-{{ uuid }}" ).html('<div class="spinner spinner-xs spinner-inline spinner-{{ data.uuid }}"></div> <strong>{{ action }} in progress...</strong>');

         $( "#{{ model }}-progress-bar-{{ uuid }}" ).removeClass('progress-bar-success progress-bar-danger')
         $("#{{ model }}-runner-status-{{uuid}}").html("loading...");

         // $( "#{{ model }}-progress-bar-{{ uuid }}" ).css('width',width + "%");

         // progress_bar_move_{{ pk }}();
   
       },
   success: function(data){
        // Perform operation on return value
        console.log(data.status);
        console.log("{{ model }}-spinner-{{ uuid }}");
        console.log(data.runner.celery_progress);

        $( "#{{ model }}-progress-bar-{{ uuid }}" ).css('width',data.runner.celery_progress + "%");


        //successful
          if ( data.status == 'successful' ) {
            clearTimeout( timeoutId_{{pk}} );
            
            $( "#{{ model }}-spinner-{{ uuid }}" ).html('<span class="fa fa-circle {{ model }}-spinner-{{ uuid }}" style="color:green" role="status" aria-hidden="true"></span>');

            $( "#{{ model }}-progress-description-{{ uuid }}" ).html('<div class="fa fa-circle {{ model }}-spinner-{{ data.uuid }}" style="color:green" role="status" aria-hidden="true"></div> <strong>{{ action }} successful.</strong>');

            //progress-bar-danger
            $( "#{{ model }}-progress-bar-{{ uuid }}" ).removeClass('progress-bar-danger').addClass('progress-bar-success');
            $("#{{ model }}-runner-status-{{uuid}}").html("Running");

            $("#{{ model }}-user-credential-instance-{{ uuid }}").html("Succeed");
          };

        //failed

          if ( data.status == 'failed' ) {
            clearTimeout( timeoutId_{{pk}} );
            
            $( "#{{ model }}-spinner-{{ uuid }}" ).html('<span class="fa fa-circle {{ model }}-spinner-{{ uuid }}" style="color:#b51c10" role="status" data-toggle="tooltip" data-placement="top" title="{{ msg|escapejs }}" role="status" aria-hidden="true"></span>');

            $( "#{{ model }}-progress-description-{{ uuid }}" ).html('<div class="fa fa-circle {{ model }}-spinner-{{ data.uuid }}" style="color:#b51c10" role="status" aria-hidden="true"></div> <strong>{{ action }} failed.</strong>');

            //progress-bar-danger
            $( "#{{ model }}-progress-bar-{{ uuid }}" ).removeClass('progress-bar-success').addClass('progress-bar-danger');
            
            // Status
            $("#{{ model }}-runner-status-{{uuid}}").html("Failed to start");
            $("#{{ model}}-user-credential-instance-{{ uuid }}").html("Hahhoooo");
            console.log($("#{{ model }}-user-credential-instance-{{ uuid }}").html("Succeed"));

          };


        //running or starting

          if ( data.status == 'running' || data.status == 'starting' ) {

            $( "#{{ model }}-spinner-{{ uuid }}" ).html('<span class="spinner spinner-xs spinner-inline {{ model }}-spinner-{{ uuid }}" role="status" aria-hidden="true"></span>');

          };

   
   }

  });

}, 2000);



</script>


