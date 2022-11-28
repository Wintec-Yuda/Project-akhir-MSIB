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
                            <span class="rating">
                                Rating : `+value[1]+`
                            </span> 
                        </div> 
                    </div>
                </div> 
            </div>
            `)
        });
        $(".pre-populer").css("display", "none");
    });

    jQuery.ui.autocomplete.prototype._resizeMenu = function () {
        var ul = this.menu.element;
        ul.outerWidth(this.element.outerWidth());
    }

    $("#input-title").on("keyup", function () {
        title = $(this).val().toLowerCase();
        titleList = []

        if (title.length%4 == 0){
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
            $("#recommend-holder").css("display", "block");
            $("#input-title").val("");
            $('#mode-select').prop('selectedIndex',0);
            $.post("/get_recommend", {
                book: title,
                mode: selected_mode
            }, function (data, status) {
                var result_status = data["book-status"];
                var text = "";
                if (result_status == "normal"){
                    text = "Jika anda menyukai <b>" +title+ "</b>, anda mungkin juga menyukai";
                } else if (result_status == "na"){
                    text = "Tidak ditemukan rekomendasi untuk buku <b>" +title+"</b>";
                } else if (result_status == "rare"){
                    text = "Buku <b>" +title+ "</b> adalah buku yang jarang, anda mungkin bisa mencoba";
                }

                $("#recommend-card").append(`<h6 class="text-center book-status">`+text+`</h6>`);
                $.each(data["data"], function (key, value) {
                    $("#recommend-card").append(`
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
                                    <span class="rating">
                                        Rating : `+value[1]+`
                                    </span> 
                                </div> 
                            </div>
                        </div> 
                    </div>
                    `)
                });
                $(".pre-recommend").css("display", "none");
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

    $("#menu-bar").click(function () {
        var x = document.getElementById("myTopnav");
        if (x.className === "topnav") {
          x.className += " responsive";
        } else {
          x.className = "topnav";
        }
    })
});