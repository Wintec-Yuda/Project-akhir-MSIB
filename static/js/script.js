$(document).ready(function () {
    var title = "";
    var titleList = [];

    jQuery.ui.autocomplete.prototype._resizeMenu = function () {
        var ul = this.menu.element;
        ul.outerWidth(this.element.outerWidth());
    }

    $("#input-title").on("keyup", function () {
        title = $(this).val();
        titleList = []

        if (title.length == 4) {
            $.post("/get_title", {
                book: title
            }, function (data, status) {
                $.each(data["data"], function (key, value) {
                    titleList.push(value)
                });
                $("#input-title").autocomplete({
                    source: titleList
                });
            });
        }

    });

    $("#search-btn").click(function (e) {
        e.preventDefault();

        if (title != "") {



        }

    });

});