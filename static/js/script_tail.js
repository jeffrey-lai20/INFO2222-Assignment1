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
    console.log(user_role);
    console.log(user_email);
    // display based on login or role status
    if (is_logged_in) {
        $(".need_login").css('display', 'block');
        if (user_role == "staff") {
            $(".need_staff").css('display', 'block');
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
});