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

});
