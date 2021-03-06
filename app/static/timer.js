$(document).ready(function() {
    function startTimer(duration, display) {
        var timer = duration, hours, minutes, seconds;
        var refresh = setInterval(function () {
            hours = parseInt(timer / 3600, 10)
            minutes = parseInt( (timer - hours * 3600 ) / 60, 10)
            seconds = parseInt(timer % 60, 10);

            hours = "0" + hours;
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            var output = hours + " : " + minutes + " : " + seconds;
            display.text(output);
            $("title").html(output + " - TimerTimer");

            if (--timer < 0) {
                display.text("Time's Up!");
                clearInterval(refresh);  // exit refresh loop
            }
        }, 1000);

    }

    // start timer
    jQuery(function ($) {
        var display = $('#time');
        startTimer(Seconds, display);
    });

})
