
$('.previous_page_btn').on('click', function () {
  current_page--;
  $('.next_page_btn').parent().removeClass('disabled');
  if (current_page <= 0 || current_page > total_pagination) {
    current_page = 1;
    return;
  }
  $('.pagination-pf-page').val(current_page);
  if (current_page == 1) {
    $('.previous_page_btn').parent().addClass('disabled');
  }
  render_view();
});
$('.next_page_btn').on('click', function () {
  current_page++;
  if (current_page == total_pagination) {
    $(this).parent().addClass('disabled');
  }
  if (current_page == 0 || current_page > total_pagination) {
    current_page = total_pagination;
    return;
  }
  $('.pagination-pf-page').val(current_page);
  if (current_page > 1) {
    $('.previous_page_btn').parent().removeClass('disabled');
  }
  render_view();
});
$('.last_page_btn').on('click', function () {

  current_page = total_pagination;
  $('.pagination-pf-page').val(total_pagination);
  if (current_page == total_pagination) {
    $('.next_page_btn').parent().addClass('disabled');
    $(this).parent().addClass('disabled');
    $('.previous_page_btn').parent().removeClass('disabled');
    $('.first_page_btn').parent().removeClass('disabled');
  }
  if (current_page > 1) {
    $('.previous_page_btn').parent().removeClass('disabled');
  }
  render_view();
})
$('.first_page_btn').on('click', function () {

  current_page = 1;
  $('.pagination-pf-page').val(current_page);
  if (current_page == 1) {
    $('.next_page_btn').parent().removeClass('disabled');
    $('.last_page_btn').parent().removeClass('disabled');
    $('.previous_page_btn').parent().addClass('disabled');
    $(this).parent().addClass('disabled');
  }
  if (current_page > 1) {
    $('.previous_page_btn').parent().removeClass('disabled');
  }
  render_view();
})


// $(function () {

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



var runJob = function () {
  var btn = $(this);
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  // console.log( $( btn ).attr("data-url") );
  // console.log( csrftoken );

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajax({
    url: btn.attr("data-url"),
    type: 'post',
    dataType: 'json',
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    success: function (data) {
      // console.log( data );
      return true
    }
  });
};


var navigateLink = function () {
  var btn = $(this);
  // $("#ajax-responsive").html('').load( btn.attr("data-url") );
  $.ajax({
    type: 'GET',
    url: btn.attr("data-url"),
    beforeSend: function () {
      $("#ahome-overlay").fadeIn(300);
    },
    success: function (data) {
      // console.log(data);
      $("#ajax-responsive").html(data);
    }
  }).done(function () {
    setTimeout(function () {
      $("#ahome-overlay").fadeOut(300);
    }, 500);
  });
};



/* Binding */


// Create ahome-generic
// $(".js-link-ahome-generic-create").click(loadForm);
$("#ahome-generic-create").on("click", ".js-link-ahome-generic-create", loadForm);
$("#modal-ahome-generic").on("submit", ".js-ahome-generic-create-form", saveForm);

// Update ahome-generic
$("#ahome-generic-list").on("click", ".js-link-ahome-generic-update", loadForm);
$("#modal-ahome-generic").on("submit", ".js-ahome-generic-update-form", saveForm);

// Update credential
$("#ahome-generic-list").on("click", ".js-link-ahome-generic-credential", loadForm);
$("#modal-ahome-generic").on("submit", ".js-ahome-generic-credential-form", saveForm);

// Delete ahome-generic
$("#ahome-generic-list").on("click", ".js-link-ahome-generic-delete", loadForm);
$("#modal-ahome-generic").on("submit", ".js-ahome-generic-delete-form", saveForm);

// Run Celery Tasks
$("#ahome-generic-list").on("click", ".js-link-ahome-generic-run-synchronize", runJob);
$("#ahome-generic-list").on("click", ".js-link-ahome-generic-run-activate", runJob);
$("#ahome-generic-list").on("click", ".js-link-ahome-generic-run-deactivate", runJob);
$("#ahome-generic-list").on("click", ".js-link-ahome-generic-run-deploy", runJob);

$("#ahome-vm-detail-actions").on("click", ".vm-detail-run-activate", runJob);
$("#ahome-vm-detail-actions").on("click", ".vm-detail-run-synchronize", runJob);
$("#ahome-vm-detail-actions").on("click", ".vm-detail-run-deactivate", runJob);
$("#ahome-vm-detail-actions").on("click", ".vm-detail-run-reconfigure", runJob);
$("#ahome-vm-detail-actions").on("click", ".vm-detail-run-shutdown", runJob);

//navigate
// $( "#ahome-nav-pf-link" ).on( "click", ".js-link-ahome-nav-pf", navigateLink );
$("#ahome-generic-list").on("click", ".js-link-ahome-navigate", navigateLink);
$("#ahome-generic-create").on("click", ".js-link-ahome-navigate", navigateLink);
$(".btn.btn-primary.js-link-ahome-navigate").on("click", navigateLink);
$("a .js-link-ahome-navigate").on("click", navigateLink);
// <li><a href="#" class="js-link-ahome-navigate" data-url="{% url 'iaas' %}?id={{ ias.id }}&provider={{ data.id }}">{{ ias.name }}</a> &nbsp; {% if ias.status != "running" %} ( <i class="fa fa-info" aria-hidden="true"></i> {{ ias.status }} ) {% endif %}</li>



// //Providers
//   $("#providers-link").click(function() {
//     // Initialize the vertical navigation
//     $("#ajax-responsive").html('').load(
//             "{% url 'provider' %}"
//         );
//   });


// });

// //Prefixes
// $("#prefixes-link").click(function() {
//   // Initialize the vertical navigation
//   $("#ajax-responsive").html('').load(
//           "{% url 'prefix' %}"
//       );
// });




// Initialize Tooltip
jQuery(document).ready(function () {
  jQuery('[data-toggle="tooltip"]').tooltip();
});

