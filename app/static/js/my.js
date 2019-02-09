$(document).ready(function () {
    $.get('/all_visit', function (data) {
        $('#people_num').append(data)
    });
});


$(function () {
    var timer = null;
    var xhr = null;

    $('.user_popup').hover(
        function (event) {

            // alert('sad');
            //mouse in
            var elem = $(event.currentTarget);
            // 过了一秒才执行的代码
            timer = setTimeout(function () {
                timer = null;
                xhr = $.ajax(
                    '/user/' + elem.first().text().trim() + '/popup'
                ).done(function (data) {
                    xhr = null;
                    elem.popover({
                        trigger: 'manual',
                        html: true,
                        animation: false,
                        container: elem,
                        content: data,
                    }).popover('show');
                    // flask_moment_render_all();
                });

            }, 1000);
        },
        function (event) {
            //mouse out
            var elem = $(event.currentTarget);
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            else if (xhr) {
                xhr.abort();
                xhr = null;
            }
            else {
                elem.popover('hide');
            }
        }
    );
});


