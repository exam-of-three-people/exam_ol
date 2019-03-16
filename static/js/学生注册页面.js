$(function () {


    //默认绑定省
    collegeBind();
    //绑定事件
    $("#college").change(function () {
        majorBind();
    })

    $("#major").change(function () {
        classBind();
    })


})
alert("ddddhjjjjjjjjjjjjjjjjjj");

function Bind(str) {
    alert($("#college").html());
    $("#college").val(str);


}

function collegeBind() {
    //清空下拉数据
    $("#college").html("");


    var str = "<option>==请选择===</option>";
    $.ajax({
        type: "POST",
        url: "/selects",
        data: {"parentiD": "", "MyColums": "Province"},
        dataType: "JSON",
        async: false,
        success: function (data) {
            //从服务器获取数据进行绑定
            $.each(data.Data, function (i, item) {
                str += "<option value=" + item.Id + ">" + item.MyTexts + "</option>";
            })
            //将数据添加到省份这个下拉框里面
            $("#college").append(str);
        },
        error: function () {
            alert("Error");
        }
    });


}

function majorBind() {


    var provice = $("#college").attr("value");
    //判断省份这个下拉框选中的值是否为空
    if (provice == "") {
        return;
    }
    $("#major").html("");
    var str = "<option>==请选择===</option>";


    $.ajax({
        type: "POST",
        url: "/selects",
        data: {"parentiD": provice, "MyColums": "City"},
        dataType: "JSON",
        async: false,
        success: function (data) {
            //从服务器获取数据进行绑定
            $.each(data.Data, function (i, item) {
                str += "<option value=" + item.Id + ">" + item.MyTexts + "</option>";
            })
            //将数据添加到省份这个下拉框里面
            $("#major").append(str);
        },
        error: function () {
            alert("Error");
        }
    });


}

function classBind() {


    var provice = $("#major").attr("value");
    //判断市这个下拉框选中的值是否为空
    if (provice == "") {
        return;
    }
    $("#classes").html("");
    var str = "<option>==请选择===</option>";
    //将市的ID拿到数据库进行查询，查询出他的下级进行绑定
    $.ajax({
        type: "POST",
        url: "/selects",
        data: {"parentiD": provice, "MyColums": "Village"},
        dataType: "JSON",
        async: false,
        success: function (data) {
            //从服务器获取数据进行绑定
            $.each(data.Data, function (i, item) {
                str += "<option value=" + item.Id + ">" + item.MyTexts + "</option>";
            })
            //将数据添加到省份这个下拉框里面
            $("#classes").append(str);
        },
        error: function () {
            alert("Error");
        }
    });
    //$.post("/Home/GetAddress", { parentiD: provice, MyColums: "Village" }, function (data) {  
    //    $.each(data.Data, function (i, item) {
    //        str += "<option value=" + item.Id + ">" + item.MyTexts + "</option>";
    //    })
    //    $("#classes").append(str);
    //})
}