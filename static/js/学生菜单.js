$("#start_exam").click(function(){

	//让遮光布显示出来
	//	$("#show").show();
	//渐入效果 ;时间单位：毫秒 1000 = 1秒
    alert("??????????????????????????????????????");
	$("#show").fadeIn(500);
	$("#show_test_plan").fadeIn(500);

});

//退出效果
$("#show").click(function() {
	//渐入效果 ;时间单位：毫秒 1000 = 1秒
	$("#show").fadeOut(500);
	$("#show_test_plan").fadeOut(500);
});