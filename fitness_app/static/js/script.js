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
