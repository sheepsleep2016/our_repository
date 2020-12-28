/**
 * Created by tarena on 19-5-20.
 */


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


//创建弹出框
var qwer = function(){
    var modal = document.createElement("div");
    modal.className="alert-contain-modal";
    var _html='<div class="alert-contain">';
        _html+='<div class="alert-header clearfixed">';
        _html+='<span>提示</span>';
        _html+='<a href="javascript:void(0)" class="close" onclick="closeAlert(this)">X</a>';
        _html+='<form action="" method="post" class="form-report">';
        _html+='<label>';
        _html+='<span>订单编号:</span>';
        _html+='<select name="select" class="select2">';
        _html+='{% for comm_name in order_list %}';
        _html+='<option>{{ comm_name }}</option>';
        _html+='{% endfor %}';
        _html+='</label>';
        _html+='<label class="a">';
        _html+='<span>标题:</span>';
        _html+='<input type="text" class="order_id" name="title">';
        _html+='</label>';
        _html+='<label>';
        _html+='<span>具体内容:</span>';
        _html+='<textarea name="content" placeholder="请填写需要反馈的具体内容"></textarea>';
        _html+='</label>';
        _html+='<div class="alert-footer">';
        _html+='<input type="submit" class="btn" onclick="closeAlert(this)">';
        _html+='</div>';
        _html+='</form>';
        _html+='</div>';
        _html+='</div>';
    modal.innerHTML =_html;
    document.body.append(modal);
}


//创建弹出框
var userAlert = function(msg){
    var modal = document.createElement("div");
    modal.className="alert-contain-modal";
    var _html='<div class="alert-contain">';
        _html+='<div class="alert-header clearfixed">';
        _html+='<span>提示</span>';
        _html+='<a href="javascript:void(0)" class="close" onclick="closeAlert(this)">X</a>';
        _html+='</div>';
        _html+='<div class="alert-content">'+msg+'</div>';
        _html+='<div class="alert-footer">';
        _html+='<a class="btn" href="javascript:void(0)" onclick="closeAlert(this)">确定</a>';
        _html+='</div>';
        _html+='</div>';
    modal.innerHTML =_html;
    document.body.append(modal);
}

function choice01() {
 // userAlert("adsdasdasdasdasdas")
  qwer()
}



