$(function () {
    // Helper function
    // Get url parameter jquery Or How to Get Query String Values In js
    // ref: https://stackoverflow.com/questions/19491336/get-url-parameter-jquery-or-how-to-get-query-string-values-in-js
    // return string | false
    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
            }
        }
    };

    // Fetch current user data
    var cur_user = $("#user_data");
    var user_role = cur_user.data("user_role").startsWith("${") ? null : cur_user.data("user_role");
    var user_email = cur_user.data("user_email").startsWith("${") ? null : cur_user.data("user_email");
    var is_logged_in = user_role ? true : false;
    // console.log(user_role);
    // console.log(user_email);

    // deletetion noty message
     function showDeletionNoty (item = 'Item') {
         new Noty({
             type: 'success',
             layout: 'topRight',
             text: 'This ' + item + ' has been deleted successfully!'
         }).show();
     }

    // display based on login or role status
    if (is_logged_in) {
        $(".need_login").css('display', 'block');
        if (user_role == "staff") {
            $(".need_staff:not(.should_inline_block)").css('display', 'block');
            $(".need_staff.should_inline_block").css('display', 'inline-block');
        }
    } else {
        $(".need_anonymous").css('display', 'block');
    }

    // display redirect notification if any
    var redirect_msg = getUrlParameter("redirect_msg");
    if (redirect_msg) {
        new Noty({
            text: redirect_msg,
        }).show();
    }

    function toggleNewMessagePage(switchTo = 'open') {
        let in_new_messages = $(".in_new_message");
        // console.log(in_new_messages)
        let not_in_new_messages = $(".not_in_new_message");
        if (switchTo == 'open') {
            not_in_new_messages.addClass("d-none");
            in_new_messages.removeClass("d-none");
        } else if(switchTo == 'close') {
            in_new_messages.addClass("d-none");
            not_in_new_messages.removeClass("d-none");
        }
    }

    var current_active_button=$("#meeting_message_btn");
    $(".message_btn").on("click", function () {
        let msg_wrapper_id = $(this).data("msg_id");

        $(".message_btn").find("button").removeClass("btn-active");
        current_active_button = $(this).find("button");
        current_active_button.addClass("btn-active");

        $(".message_wrapper").addClass("d-none");
        $("#" + msg_wrapper_id).removeClass("d-none");

        toggleNewMessagePage("close");
    });

    $("#message_delete_btn").on("click", function () {
        $(".message_wrapper").addClass("d-none");

        let current_btn_row = current_active_button.closest(".row");
        current_btn_row.addClass("d-none");
        current_active_button = $("#btn_list").find(".row:not(.d-none):first button");
        current_active_button.addClass("btn-active");
        let cur_msg_wrapper_id = current_active_button.closest(".message_btn").data("msg_id");
        $("#" + cur_msg_wrapper_id).removeClass("d-none");

        showDeletionNoty('message');
    });

    $("#new_message_btn").on("click", function () {
        toggleNewMessagePage("open");
    });

    // reset form inputs
    $(".reset_message").click(function() {
        $(this).closest('form').find("input, textarea").val("");
    });

    // send message
    $(".send_message").click(function () {
        let success_sent_alert = '<div class="alert alert-success alert-dismissible fade show" role="alert"> Message has been sent successfully!<button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span> </button></div>';
        $("#send_message_alert").append(success_sent_alert);
    });

    // determine if show staff permission things
    if (user_role == "staff")
    {
        // delete form post
        $(".delete_form_post").on("click", function() {
            $(this).closest(".row").addClass("d-none");
            let cur_msg_wrapper = $(this).data("msg_id");
            if (cur_msg_wrapper)
                $("#" + cur_msg_wrapper).addClass("d-none");

            showDeletionNoty('post')
        });
        $(".form_msg_mute_btn").on("click", function() {
            if ($(this).text() == "Mute") {
                $(this).text("Muted").css("color", "grey");
                new Noty({
                    type: 'warning',
                    layout: 'topRight',
                    text: 'Forum messages from current sender will be muted!'
                }).show();
            } else {
                $(this).text("Mute").css("color", "#007bff");
                new Noty({
                    type: 'success',
                    layout: 'topRight',
                    text: 'Forum messages from current sender will be notified! '
                }).show();
            }
        });
    }

    //    Messages page
    window.showMessageContent = function (msg_id) {
        let cur_msg;
        cur_msg = $.grep(from_me_messages, function(e){ return e.id == msg_id; });
        if (cur_msg.length  === 0)
            cur_msg = $.grep(to_me_messages, function(e){ return e.id == msg_id; });
        if (cur_msg.length === 0)
            return;
        cur_msg = cur_msg[0];
        // console.log(cur_msg);
        $('#msg_title').text(parseHtmlEntities(cur_msg.subject));
        $('#msg_from_user').text(parseHtmlEntities(cur_msg.from_user)+' at '+parseHtmlEntities(cur_msg.create_at));
        $('#msg_body').text(parseHtmlEntities(cur_msg.body));

        $("#replies_wrapper").empty();
        if (Array.isArray(replies[msg_id])) {
            replies[msg_id].forEach(function (reply) {
                let card_string = '                <div class="card mb-2">\n' +
                    '                  <div class="card-body p-2" style="color: #212529;">\n' +
                    '                      <strong>From: '+reply.from_user+' at '+reply.create_at+'</strong>\n' +
                    '                      <p>'+reply.body+'</p>\n' +
                    '                  </div>\n' +
                    '                </div>';
                $("#replies_wrapper").append(card_string);
            });
        }
        current_message = msg_id;
        toggleNewMessagePage("close");
    }

    var current_message;
    // "add new" button
    const new_message_button = '<button id="new_message_btn" type="button" class="btn btn-info my-2 my-md-3" style="width: 100%">New Message</button>';
    $("#btn_list").prepend(new_message_button);

    $("#new_message_btn").on("click", function () {
        toggleNewMessagePage("open");
    });

    function show_message_btns(messages, selector) {
        try {
            messages.forEach(function (message) {
                // console.log(message);
                // button
                const select_button = '<div class="row pb-1"><div class="col-md-12">' +
                    '                <a href="javascript:void(0)" id="message_btn_' + message.id + '" class="message_btn" data-msg_id="' + message.id + '">\n' +
                    '                    <button type="button" class="btn-active" onclick="showMessageContent(' + message.id + ')" style="width: 100%; height: 50px"\n' +
                    '                    >' + message['subject'] + '</button></a>\n' +
                    '            </div></div>';
                $(selector).append(select_button);
            });
        } catch (e) {
            console.log(e);
        }
    }

    function clearContent(selectors) {
        selectors.forEach(selector => {
            $(selector).text("");
        });
    }

    if (typeof from_me_messages !== "undefined") {
        show_message_btns(from_me_messages, "#from_me_message_btns");
    }

    if (typeof to_me_messages !== "undefined") {
        show_message_btns(to_me_messages, "#to_me_message_btns");
    }

    // standard post function
    const submitFormHandler = function (url, formData, type="POST") {
        const success = function (response) {
            // console.log(response);
             new Noty({
                 type: response.error == 1 ? 'warning' : 'success',
                 layout: 'topRight',
                 text: response.msg
             }).show();
             // refresh page after 2.5 seconds
             setTimeout( function(){
                if(response.error != 1)
                        location.reload();
                      }  , 2500 );
        };
        $.ajax({
          type: type,
          url: url,
          data: formData,
          success: success,
          dataType: 'json'
        });
    };

    // message submit handler
    $( "#message_form" ).submit(function( event ) {
      event.preventDefault();
      submitFormHandler('/message', $("#message_form").serialize());
    });

    // ref： https://stackoverflow.com/questions/1912501/unescape-html-entities-in-javascript
    function parseHtmlEntities(str) {
      var e = document.createElement('textarea');
      e.innerHTML = str;
      // handle case of empty input
      return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
    }

    // on message delete
    $("#message_delete_btn_").click(function () {
        submitFormHandler('/message/' + current_message, {}, "DELETE");
    });

    function arrayGrouBy(orgs, which_id="message_id") {
        return orgs.reduce(function(results, org) {
            (results[org[which_id]] = results[org[which_id]] || []).push(org);
            return results;
        }, {})
    }

    if (typeof replies !== 'undefined') {
        replies = arrayGrouBy(replies)

        $("#replay_form").submit(function (event) {
            event.preventDefault();
            if (current_message)
                submitFormHandler('/message_reply', $("#replay_form").serialize() + '&msg_id=' + current_message);
        })

    }

    // init message page
    if ($("#new_message_btn").length) {
        $("#new_message_btn").click();
    }
});
