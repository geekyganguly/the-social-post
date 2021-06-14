// Material Select Initialization
$(document).ready(function () {
  $('.mdb-select').materialSelect();
});

/* WOW.js init */
new WOW().init();

toastr.options = {
  "positionClass": "md-toast-bottom-right"
}

// Tooltips Initialization
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});


$(function () {
  $("#mdb-lightbox-ui").load("/lightbox");
});


$('#search-input').keyup(function () {
  var search = $(this).val();
  var search_results_box = $('#search-results');
  var url = $(this).attr('data-url');
  if(search_results_box.hasClass('hidden')){
    search_results_box.removeClass('hidden');
  }
  $.ajax({
    type: "POST",
    url: url,
    headers:{
      "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
    },
    data: {
      'search': search,
    },
    success: function (results) {
      const data = results.data;
      if (Array.isArray(data)){
        search_results_box.html(``)
        data.forEach(function (data){
          if (data.is_authenticated) {
            if (data.is_connected) {
              search_results_box.append(`
                <a href="/user/${data.username}">
                  <div class="media">
                      <img class="d-flex mr-3 rounded-circle" src="${data.profile_pic}" alt="" height="60" width="60">
                      <div class="media-body text-dark">
                        <p class="mt-2 mb-0"><strong>${data.name}</strong>
                          <span class="badge badge-primary text-white ml-3">Connected</span>
                        </p>
                        <p class="font-small">${data.connection} Connections</p>
                      </div>
                  </div>
                </a>
                <hr class="blue">
              `)
            }
            else {
              search_results_box.append(`
                <a href="/user/${data.username}">
                  <div class="media">
                      <img class="d-flex mr-3 rounded-circle" src="${data.profile_pic}" alt="" height="60" width="60">
                      <div class="media-body text-dark">
                        <p class="mt-2 mb-0"><strong>${data.name}</strong>
                          <span class="badge badge-danger text-white ml-3">Add Connection</span>
                        </p>
                        <p class="font-small">${data.connection} Connections</p>
                      </div>
                  </div>
                </a>
                <hr class="blue">
              `)
            }
          }
          else {
            search_results_box.append(`
              <a href="/user/${data.username}">
                <div class="media">
                    <img class="d-flex mr-3 rounded-circle" src="${data.profile_pic}" alt="" height="60" width="60">
                    <div class="media-body">
                      <div class="text-dark">
                        <p class="mt-2 mb-0"><strong>${data.name}</strong></p>
                        <p class="font-small">${data.connection} Connections</p>
                      </div>
                    </div>
                </div>
              </a>
              <hr class="blue">
            `)
          }
        })
      }
      else{
        if(search.length > 0){
          search_results_box.html(`<p class="text-danger"><strong>${data}</strong></p>`)
        }
        else{
          search_results_box.addClass('hidden')
        }
      }
    },
    error: function (e) {
      console.log(e);
    }
  })
});


$('.like-btn').click(function (e) {
  e.preventDefault();
  var post_id = $(this).attr('data-post-id')
  var like_count = $(`.like-count-${post_id}`);
  $.ajax({
    type: "GET",
    url: '/like',
    data: {
      'post_id': post_id,
    },
    success: function (r) {
      data = r.data;
      if (data.updated) {
        if (data.liked) {
          $(`#like-btn-${post_id}`).removeClass('far');
          $(`#like-btn-${post_id}`).addClass('fas');
        }
        else{
          $(`#like-btn-${post_id}`).removeClass('fas');
          $(`#like-btn-${post_id}`).addClass('far');
        }
        like_count.text(data.total_likes);
      }
    },
    error: function (e) {
      console.log(e);
    }
  })
});


$('.connect-btn').click(function (e) {
  e.preventDefault();
  var id = $(this).attr('data-connect-id');
  var url = $(this).attr('data-connect-url');
  var connection_count = $(`#connection-count-${id}`);
  var connect_btn = $('#connect-btn')
  $.ajax({
    type: "GET",
    url: url,
    data: {
      'id': id,
    },
    success: function (r) {
      data = r.data;
      if (data.updated) {
        if (data.connected) {
          connect_btn.html(`<strong>Connected</strong>`)
          connect_btn.removeClass('btn-danger');
          connect_btn.addClass('btn-primary');

        }
        else{
          connect_btn.html(`<strong>Add Connection</strong>`)
          connect_btn.removeClass('btn-primary');
          connect_btn.addClass('btn-danger');
        }
        connection_count.text(data.total_connections);
      }
    },
    error: function (e) {
      console.log(e);
    }
  })
});