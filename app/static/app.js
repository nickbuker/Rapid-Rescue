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

let send_input_json = function(coefficients) {
    $.ajax({
        url: '/predict',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
          // $('img').hide()
          // $('newimg').show()
            },
        data: JSON.stringify(coefficients)
    });
};

$(document).ready(function() {
    $("input#predict").click(function() {
        let coefficients = get_input();
        send_input_json(coefficients);
    })

})
