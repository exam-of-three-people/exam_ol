function signUp(){
    var flag = confirm("点击确认进入教师注册，点击取消进入学生注册");

if(flag) {
    self.location.href= "../teacherRegister";
}

else{    self.location.href= "	/studentRegister ";  	}
}
