$(function () {


    //默认绑定省
    collegeBind();
    //绑定事件
    $("#college").change(function () {
        majorBind();
    })

    $("#grade").change(function () {
        classBind();
    })

    $("#major").change(function () {
        classBind();
    })
})

function Bind(str) {
    alert($("#college").html());
    $("#college").val(str);

}

function collegeBind() {
    let str = "<option>--请选择--</option>";
    $.ajax({
        type: "POST",
        url: "/studentRegister/selects",
        data: {"parent_id": "", "my_select": "college"},
        dataType: "JSON",
        async: false,
        success: function (data) {
            //从服务器获取数据进行绑定
            $.each(data.data, function (i, item) {
                str += "<option value=" + item.id + ">" + item.name + "</option>";
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


    let college_id = $("#college").val();
    //判断省份这个下拉框选中的值是否为空
    if (college_id == "") {
        return;
    }
    $("#major").html("");
    let str = "<option>--请选择--</option>";


    $.ajax({
        type: "POST",
        url: "/studentRegister/selects",
        data: {"parent_id": college_id, "my_select": "major"},
        dataType: "JSON",
        async: false,
        success: function (data) {
            //从服务器获取数据进行绑定
            $.each(data.data, function (i, item) {
                str += "<option value=" + item.id + ">" + item.name + "</option>";
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


    let major_id = $("#major").val();
    //判断市这个下拉框选中的值是否为空
    if (major_id == "") {
        return;
    }
    $("#class_").html("");
    let str = "";
    //将市的ID拿到数据库进行查询，查询出他的下级进行绑定
    $.ajax({
        type: "POST",
        url: "/studentRegister/selects",
        data: {"parent_id": major_id, "my_select": "class", "grade": $("#grade").val()},
        dataType: "JSON",
        async: false,
        success: function (data) {
            //从服务器获取数据进行绑定
            $.each(data.data, function (i, item) {
                str += "<option value=" + item.id + ">" + item.name + "</option>";
            })
            //将数据添加到省份这个下拉框里面
            $("#class_").append(str);
        },
        error: function () {
            alert("Error");
        }
    });

}