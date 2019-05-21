
function Submission_results() {
    subject=0;
    correct=0;
    for (item = 0; item < contents.length; i++) {
        subject = subject + 1;
        if (contents[i].question == contents[i].answer) {
            print('第%d道题回答正确', i - 1)
            correct = correct + 1;

        }
    }
    lv = correct / subject;
    alert('你的成绩为' + str(lv))
}

function hg() {
    alert('你的成绩是' + str(lv))

}

// ####################################################################

function settime(remainTime) {
        var _countdown = parseInt(getCookieValue("${test.id}")) / 1000;

        if (_countdown <= 0) {
            warn("提示!","考试时间到！");
            endExam();
        } else {
            var _second = _countdown % 60;
            var _minute = parseInt(_countdown / 60) % 60;
            var _hour = parseInt(parseInt(_countdown / 60) / 60);
            if (_hour < 10)
                _hour = "0" + _hour.toString();
            if (_second < 10)
                _second = "0" + _second.toString();
            if (_minute < 10)
                _minute = "0" + _minute.toString();
            remainTime.html(_hour + ":" + _minute + ":" + _second);
            _countdown--;
            editCookie("${test.id}", _countdown * 1000, _countdown * 1000);
        }
        //每1000毫秒执行一次
        setTimeout(function() {
            settime(remainTime);
        }, 1000);
    };

        // 结束考试
    function endExam(){
        $("#btnSubmit").trigger("click");
    }
    // 提示框
        function warn(title,content){
            $.alert({
                title: title,
                content: content,
                icon: 'fa fa-rocket',
                animation: 'zoom',
                closeAnimation: 'zoom',
                buttons: {
                    okay: {
                        text: '确定',
                        btnClass: 'btn-primary'
                    }
                }
            });
            return;
        }


