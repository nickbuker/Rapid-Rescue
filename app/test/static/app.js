let get_input = function() {
    let a = $("input#date_input").val()
    return {'date_input': a}
};

let send_input_json = function(query) {
    $.ajax({
        url: '/predict',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
          $("#data_return").show();
          $("#data_entry").hide();
            },
        data: JSON.stringify(query)
    });
};

// $("#data_return").toggle();
// $("#data_return")
// $("#data_return")

$(document).ready(function(){
  $("#predict").click(function(){
    let query = get_input();
    send_input_json(query);
    // Ajax call
      // Retrieve relvant cluster data
      // On success
        // Plot cluster data
        // Insert plot into data_return div somewhere
        // Show/hide relevant divs
    // $("#data_return").show();
    // $("#data_entry").hide();
  });
  $("#return").click(function(){
    $("#data_entry").show();
    $("#data_return").hide();
  });
});
