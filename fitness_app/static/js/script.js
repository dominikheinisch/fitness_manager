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

function align_activity_table() {
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
};

$(document).ready(function(){
    align_activity_table();
});

window.onresize = function() {
    align_activity_table();
}

$(function() {
    $(".clearMeal").click(function() {
        $(".modalToClear").each(function(i, v) {
            $(v).val("");
        });
        $("#portionTable .portion_tr").each(function(i, v) {
            $(v).remove();
        });
        $('#id_form-TOTAL_FORMS').val(0);
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

function handleAddPortion(prefix) {
    var total_forms_str = "#id_" + prefix + "-TOTAL_FORMS";
    var form_idx = $(total_forms_str).val();
    $("#portionTable > tbody").append($("#empty_tr").html().replace(/__prefix__/g, form_idx));
    $(total_forms_str).val(parseInt(form_idx) + 1);
};

$(function() {
    $('#add_more').click(function() {
        handleAddPortion("form");
    });
});

$(function() {
    $('#add_portion').click(function() {
        handleAddPortion("portions");
    });
});

function handleBtnDelPortion(that, prefix) {
//    TODO update indexes of td after removal
    var n = that.id.search("-del");
    var tr_str = "#" + that.id.substring(0, n) + "-tr";
    var total_forms_str = "#id_" + prefix + "-TOTAL_FORMS";
    $(tr_str).remove();
    var form_idx = $(total_forms_str).val();
    $(total_forms_str).val(parseInt(form_idx) - 1);
};

$(document).on("click", ".btnDelPortion", function() {
    var that = this
    handleBtnDelPortion(that, "form");
});

$(document).on("click", ".btnDelTempPortion", function() {
    var that = this
    handleBtnDelPortion(that, "portions");
});

