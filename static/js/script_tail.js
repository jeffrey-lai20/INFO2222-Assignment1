$(document).ready(function () {
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

});