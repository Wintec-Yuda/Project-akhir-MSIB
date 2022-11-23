$(document).ready(function () {
    var title = "";
    var titleList = [];

    $.get("/get_popular", function(data, status){
        $.each(data["data"], function (key, value) {
            $("#populer-card").append(`
            <div class="col-lg-3 p-1">
                <div class="card-inner p-3 d-flex flex-column align-items-center h-100"> 
                    <img class="rounded img-fluid" src="`+value[2]+`" style="height: 210px !important;">
                    <div class="align-self-center h-100">
                        <div class="text-center mg-text"> 
                            <span class="mg-text">
                                `+value[0]+`
                            </span> 
                        </div>
                        <div class="text-center"> 
                            <span id="rating">
                                Rating : `+value[1]+`
                            </span> 
                        </div> 
                    </div>
                </div> 
            </div>
            `)
        });
        $("#populer-holder").css("display", "block");
    });

    jQuery.ui.autocomplete.prototype._resizeMenu = function () {
        var ul = this.menu.element;
        ul.outerWidth(this.element.outerWidth());
    }

    $("#input-title").on("keyup", function () {
        title = $(this).val().toLowerCase();
        titleList = []

        if (title.length%3 == 0){
            $.post("/get_title", {
                book: title
            }, function (data, status) {
                $.each(data["data"], function (key, value) {
                    titleList.push(value)
                });
                $("#input-title").autocomplete({
                    source: titleList,
                    position: { my : "right top+15", at: "right bottom" }
                });
            });
        }
    });

    $("#input-title").on("autocompleteselect", function (event, ui) {
        title = ui.item.value
    });

    $("#search-btn").click(function (e) {
        e.preventDefault();
        var selected_mode = $('#mode-select option:selected').val();
        if (title != "" && selected_mode !="") {
            $("#input-title").val("")
            $.post("/get_recommend", {
                book: title,
                mode: selected_mode
            }, function (data, status) {
                console.log("Data: " + data["data"] + "\nStatus: " + status);
            });

            $('html, body').animate({
                scrollTop: $("#recommend-holder").offset().top
            }, 1000);
        } else if (title != ""){
            alert("Pilih Mode Rekomendasi")
        } else if (selected_mode != ""){
            alert("Masukkan Judul")
        } else {
            alert("Masukkan Judul dan Pilih Mode Rekomendasi")
        }
    });

});