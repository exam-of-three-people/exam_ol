var num = 0

function Submission_results() {
    subject = 0;
    correct = 0;
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


// ####################################################################

function settime(remainTime, rest_time_) {
    console.log(rest_time_)
    let _countdown = parseInt(rest_time_);

    if (_countdown <= 0) {
        warn("提示!", "考试时间到！");
        endExam();
    } else {
        let _second = _countdown % 60;
        let _minute = parseInt(_countdown / 60) % 60;
        let _hour = parseInt(parseInt(_countdown / 60) / 60);
        if (_hour < 10)
            _hour = "0" + _hour.toString();
        if (_second < 10)
            _second = "0" + _second.toString();
        if (_minute < 10)
            _minute = "0" + _minute.toString();
        remainTime.html("<p style='color:green'>" + _hour + ":" + _minute + ":" + _second + "</p>");
        _countdown--;
        let send_data = $("#form").serializeJson("rest_time:" + _countdown.toString() + ";")
        $.ajax({
            type: "POST",
            url: "/auto_save",
            data: send_data,
            dataType: "JSON",
            async: false,
            success: function (data) {
                rest_time_ = parseInt(data)
            }
        });
    }
    //每1000毫秒执行一次
    setTimeout(function () {
        settime(remainTime, rest_time_);
    }, 1000);
};

// 结束考试
function endExam() {
    $("#submit").trigger("click");
}

// 提示框
function warn(title, content) {
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

/**
 * 将form里面的内容序列化成json
 * 相同的checkbox用分号拼接起来
 * @param {dom} 指定的选择器
 * @param {obj} 需要拼接在后面的json对象
 * @method serializeJson
 * */
$.fn.serializeJson = function (otherString) {
    let serializeObj = {},
        array = this.serializeArray();
    $(array).each(function () {
        if (serializeObj[this.name]) {
            serializeObj[this.name] += ';' + this.value;
        } else {
            serializeObj[this.name] = this.value;
        }
    });

    if (otherString != undefined) {
        let otherArray = otherString.split(';');
        $(otherArray).each(function () {
            let otherSplitArray = this.split(':');
            serializeObj[otherSplitArray[0]] = otherSplitArray[1];
        });
    }
    return serializeObj;
};

/**
 * 将josn对象赋值给form
 * @param {dom} 指定的选择器
 * @param {obj} 需要给form赋值的json对象
 * @method serializeJson
 * */
$.fn.setForm = function (jsonValue) {
    let obj = this;
    $.each(jsonValue, function (name, ival) {
        let $oinput = obj.find("input[name=" + name + "]");
        if ($oinput.attr("type") == "checkbox") {
            if (ival !== null) {
                let checkboxObj = $("[name=" + name + "]");
                let checkArray = ival.split(";");
                for (let i = 0; i < checkboxObj.length; i++) {
                    for (let j = 0; j < checkArray.length; j++) {
                        if (checkboxObj[i].value == checkArray[j]) {
                            checkboxObj[i].click();
                        }
                    }
                }
            }
        } else if ($oinput.attr("type") == "radio") {
            $oinput.each(function () {
                let radioObj = $("[name=" + name + "]");
                for (let i = 0; i < radioObj.length; i++) {
                    if (radioObj[i].value == ival) {
                        radioObj[i].click();
                    }
                }
            });
        } else if ($oinput.attr("type") == "textarea") {
            obj.find("[name=" + name + "]").html(ival);
        } else {
            obj.find("[name=" + name + "]").val(ival);
            obj.find("[name=" + name + "]").trigger("onchange")
        }
    })
}

let rest_time_value = $("#data_").attr("data-rest_time")
this.settime($("#rest_time"), rest_time_value)
let form_data = JSON.parse($("#data_").attr("data-answer").replace(/'/g, '"'));
console.log(form_data)
$("#form").setForm(form_data)


function show_test_panel(name) {

    let answer = document.getElementsByName(name);
    let answer_length = answer[0].value.length;
    // answer 是个NodeList, 直接.length永远不为0,最少是1  巨坑!!!
    let flag = document.getElementById(name);

    if (answer_length > 0) {
        console.log("做了");
        dic[name] = 1;
        console.log(dic)
        flag.style.background = "skyblue";
    } else {
        dic[name] = 0;
        flag.style.background = "white";
    }
}


function hg(test_num) {
    let num = 0;
    console.log("aaaaaaaaaaaaaa")
    console.log(dic)
    for (let key in dic) { // 输出字典元素，如果字典的key是数字，输出时会自动按序输出
        num += dic[key];
        console.log(num)
    }
    if (num > 0) {
        p = test_num - num
        let speak = "你还有" + p + "道题没做，确认提交吗?"
        let chose = confirm(speak)
        if (chose == true) {
            alert("shdjkbdsfsdf")
            return true
        }
        if (chose == false) {

            return false
        }
    } else {
        alert("jdbfvkdsvbsd")
        return false
    }

}





