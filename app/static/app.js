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

let validate_form = function(imput_a, imput_b) {
  if ((imput_a == "") || (isNaN(imput_b))) {
    return false
  }
  else {
    $("#calculating").show();
    $("#pred_button").hide();
    return true
  }
};

let send_input_json = function(query) {
  let valid = validate_form(query.date_input, query.num_units)
  if (valid == true) {
    $.ajax({
        url: '/predict',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
          $("#data_return").show();
          $("#data_entry").hide();
          $("#calculating").hide();
          display_stuff(data)
            },
        data: JSON.stringify(query)
  })}
  if (valid == false) {
    alert("Date and Quantity fields must be filled.")
  }
};

let display_stuff = function(data) {
  $("span#locs_table").html(data.table)
  $("img#map").attr('src', '/static/'+ data.img_name)
};

$(document).ready(function() {
    $("input#predict").click(function() {
        let coefficients = get_input();
        send_input_json(coefficients);
    });
    $("#return").click(function(){
      $("#data_entry").show();
      $("#pred_button").show();
      $("#data_return").hide();
      $("#plot_entry").show();
    });
});
