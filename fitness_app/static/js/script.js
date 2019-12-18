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