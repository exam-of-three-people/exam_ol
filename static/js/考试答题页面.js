<!-- JS部分 -->

$(".time").text("60s");    //首先默认给60s

var i = 60;
var Timer = setInterval(function () {
    i--;
    $(".time").text(i + "s");
    if (i == -1) {
        $(".time").text("请重新发送");
        clearInterval(Timer);
    }
}, 1000);