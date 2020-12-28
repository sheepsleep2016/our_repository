
function checkvalid() {
    var strmg=$("#user_name").val();
    var pass=$("#user_pwd").val();
    var code=$("#code").val();
    if(strmg==""){
    $("#show").html("请输入您的邮箱/用户名/手机号");
    }else if(pass=="") {
    $("#show").html("请输入密码");
    }else if (code==""){
    $("#show").html("请输入验证码");
    }else{
    checkaccount();
    }
}
function checkaccount() {
    $.ajax({
        url: '/login00/',
        type: 'POST',
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        data: {
          user_account: $('#user_account').val(),
          user_pwd: $('#user_pwd').val(),
          code:$('#code').val(),
          rem:$('#rem').val(),
        },
    success: function (data) {
      var dat = JSON.parse(data);
      if (dat.flag ==0){
        window.location.href="/";
      }else{console.log(dat);
      $("#show").html(dat.flag);}
    }
  })
}


