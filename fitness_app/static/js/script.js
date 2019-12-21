//if (typeof jQuery != 'undefined') {
//    // jQuery is loaded => print the version
//    alert(jQuery.fn.jquery);
//};

$( function() {
    $(".datepicker").datepicker();
});

$(function() {
    $(".onClickDatepicker").datepicker({
        onSelect: function(d,i) {
            if(d !== i.lastVal) {
                $(".select_btn").trigger("click");
            }
        }
    });
});

$(document).ready(function(){
    var $table = $('#activity-table'),
        $bodyCells = $table.find('tbody tr:first').children(),
        colWidth;

    colWidth = $bodyCells.map(function() {
        return $(this).width();
    }).get();
    $table.find('thead tr').children().each(function(i, v) {
        $(v).width(colWidth[i]);
    });
    $table.find('tfoot tr').children().each(function(i, v) {
        $(v).width(colWidth[i]);
    });
});

$(function() {
    $(".clearMeal").click(function() {
        $(".modalToClear").each(function(i, v) {
            $(v).val("");
        });
        $("#portionTable .portion_tr").each(function(i, v) {
            $(v).remove();
        });
        $('#id_form-TOTAL_FORMS').val(1);
    });
});

$(document).ready(function(){
    if ($("#addModal").attr("value") == 'True') {
        $("#modalAddBtn").trigger("click");
    };
});

$(function() {
    $('#modalAddBtn').click(function() {
        $("#add_more").trigger("click");
    });
});

$(function() {
    $('#add_more').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#portionTable > tbody').append($('#empty_tr').html().replace(/__prefix__/g, form_idx));
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
});

$(document).on("click", ".btnDelPortion", function() {
//    TODO update indexes of td after removal
    var n = this.id.search("-del");
    var tr_name = this.id.substring(0, n) + "-tr";
    $("#" + tr_name).remove();
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) - 1);
});
