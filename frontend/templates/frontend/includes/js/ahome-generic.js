<script type="text/javascript">


$(function () {

  

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-ahome-generic").modal("show");
      },
      success: function (data) {
        $("#modal-ahome-generic .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#ahome-generic-list").html(data.html_model_list);
          $("#ahome-toast-notification").html(data.html_toast_notification);
          $("#ahome-generic-search-bar").html(data.html_search_nav);
          // alert(data.html_toast_notification);
          $("#modal-ahome-generic").modal("hide");
        }
        else {
          $("#modal-ahome-generic .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };





  /* Binding */


  // Create ahome-generic
  // $(".js-link-ahome-generic-create").click(loadForm);
  // $("#modal-ahome-generic").on("submit", ".js-ahome-generic-create-form", saveForm);

  // Update ahome-generic
  // $("#ahome-generic-list").on("click", ".js-link-ahome-generic-update", loadForm);
  // $("#modal-ahome-generic").on("submit", ".js-ahome-generic-update-form", saveForm);

  // Update credential
  $("#ahome-generic-list").on("click", ".js-link-ahome-generic-credential", loadForm);
  $("#modal-ahome-generic").on("submit", ".js-ahome-generic-credential-form", saveForm);


  // Delete ahome-generic
  // $("#ahome-generic-list").on("click", ".js-link-ahome-generic-delete", loadForm);
  // $("#modal-ahome-generic").on("submit", ".js-ahome-generic-delete-form", saveForm);



  // $( "#ahome-generic-list" ).on( "click", ".js-link-ahome-generic-run-synchronize", function() {
  //   var btn = $( this );
  //   var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  //   // console.log( $( btn ).attr("data-url") );

  //   function csrfSafeMethod(method) {
  //       // these HTTP methods do not require CSRF protection
  //       return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  //   }
  //   $.ajax({
  //     url: btn.attr("data-url"),
  //     type: 'post',
  //     dataType: 'json',
  //     beforeSend: function (xhr, settings) {
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //           xhr.setRequestHeader("X-CSRFToken", csrftoken);
  //       }
  //     },
  //     success: function (data) {
  //       // console.log( data );
  //       return true
  //     }
  //   });
  // });






});


</script>