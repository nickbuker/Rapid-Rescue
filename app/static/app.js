let get_input = function() {
    let a = $("input#date_input").val()
    let b = $("input#num_units").val()
    let c = $("input[name=game]:checked").val()
    let d = $("input[name=night]:checked").val()
    return {'date_input': a,
            'num_units': parseInt(b),
            'home_game': c,
            'time_range': parseInt(d)}
};

let send_input_json = function(query) {
    $.ajax({
        url: '/predict',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
          $("#data_return").show();
          $("#data_entry").hide();
          $("#plot_return").show();
          $("#plot_entry").hide();
          display_table(data)
            },
        data: JSON.stringify(query)
    });
};

let display_table = function(data) {
  $("span#locs_table").html(data.table)
};

$(document).ready(function() {
    $("input#predict").click(function() {
        let coefficients = get_input();
        send_input_json(coefficients);
    });
    $("#return").click(function(){
      $("#data_entry").show();
      $("#data_return").hide();
      $("#plot_entry").show();
      $("#plot_return").hide();
    });
});
