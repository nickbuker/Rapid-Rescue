// Hover move listing
$(document).ready(function () {
    //superfish
    $("ul.sf-menu").superfish({
        autoArrows: false, // disable generation of arrow mark-up
        animation: {
            height: 'show'
        }
    });
    // rollovers
    $(".side-block a").hover(function () {
        // on rollover	
        $(this).stop().animate({
            marginLeft: "10"
        }, "fast");
    }, function () {
        // on out
        $(this).stop().animate({
            marginLeft: "0"
        }, "fast");
    });
    // slideshow
    $('#slides')
        .before('<div id="slideshow-nav">')
        .cycle({
        fx: 'scrollHorz',
        speed: 500,
        timeout: 6000,
        pause: 1,
        pager: '#slideshow-nav',
        next: 'img#next',
        prev: 'img#prev'
    });
    // fade slide
    $('.fade-slide').cycle({
        fx: 'fade',
        speed: 500,
        timeout: 3000,
        pause: 1
    });
    // toggle
    $(".toggle-container").hide();
    $(".toggle-trigger").click(function () {
        $(this).toggleClass("active").next().slideToggle("slow");
        return false;
    });
    // accordion
    $('.accordion-container').hide();
    $('.accordion-trigger:first').addClass('active').next().show();
    $('.accordion-trigger').click(function () {
        if ($(this).next().is(':hidden')) {
            $('.accordion-trigger').removeClass('active').next().slideUp();
            $(this).toggleClass('active').next().slideDown();
        }
        return false;
    });
    //close			
});
// search clearance	
function defaultInput(target) {
    if ((target).value == 'Search...') {
        (target).value = ''
    }
}

function clearInput(target) {
    if ((target).value == '') {
        (target).value = 'Search...'
    }
}