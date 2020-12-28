var InterValObj; //timer变量，控制时间
var count = 60; //间隔函数，1秒执行
var curCount;//当前剩余秒数
var valicate_code;//定义一个全局变量接收 产生的验证码
//发送邮箱验证码
function sendMessage() {
// var sss = send_acount();
  curCount = count;
  // 设置button效果，开始计时
  document.getElementById("btnSendCode").setAttribute("disabled","true" );//设置按钮为禁用状态
  document.getElementById("btnSendCode").value=curCount + "秒后重获";//更改按钮文字
  InterValObj = window.setInterval(SetRemainTime, 1000); // 启动计时器timer处理函数，1秒执行一次
}
//timer处理函数
function SetRemainTime() {
	if (curCount == 0) {//超时重新获取验证码
		window.clearInterval(InterValObj);// 停止计时器
		document.getElementById("btnSendCode").removeAttribute("disabled");//移除禁用状态改为可用
		document.getElementById("btnSendCode").value="重获验证码";
	}else {
		curCount--;
		document.getElementById("btnSendCode").value=curCount + "秒后重获";
	}
}

var $form = document.form;
var RegExp = {     //映射input输入框的name值
  "newpassword": /^[a-zA-Z]([_a-zA-Z0-9]{5,15})$/,		//字母开头，由数字与字母和下划线组成
  "confirmPassword": null
};

//页面加载完成
window.onload = function(){
    //获取所有需要验证的表单Input
    var $input = document.getElementsByClassName("formVal");

    //循环，给所有的需要验证的表单input绑定onfocus(获取焦点)与onblur(失去焦点)事件
    for(var i=0;i<$input.length;i++){
        var $this = $input[i];
        $this.onfocus=function(){                    //光标处于当前input
            this.style.border = "1px solid red";
        };

        $this.onblur=function(){                     //光标离开当前input
            onblur(this);   //传入当前对象
        }
    }
};

//向上追溯指定元素根节点
var closest = function(el, selector) {
    var matchesSelector = el.matches || el.webkitMatchesSelector || el.mozMatchesSelector || el.msMatchesSelector;

    while (el) {
        if (matchesSelector.call(el, selector)) {
            break;
        }
        el = el.parentElement;
    }
    return el;
};


//关闭弹出框
var closeAlert = function($this){
    var $modal = closest($this,".alert-contain-modal")
    $modal.remove();
};

//创建弹出框
var userAlert = function(msg,href00){
    var modal = document.createElement("div");
    modal.className="alert-contain-modal";
    var _html='<div class="alert-contain">';
        _html+='<div class="alert-header clearfixed">';
        _html+='<span>提示</span>';
        _html+='<a href='+href00+' class="close" onclick="closeAlert(this)">X</a>';
        _html+='</div>';
        _html+='<div class="alert-content">'+msg+'</div>';
        _html+='<div class="alert-footer">';
        _html+='<a class="btn" href='+href00+' onclick="closeAlert(this)">确定</a>';
        _html+='</div>';
        _html+='</div>';
    modal.innerHTML =_html;
    document.body.append(modal);
};

var onblur = function($this){
    if(!$this.tagName)return true;
    var newpassword = document.body.querySelectorAll("input[name='newpassword']")[0].value;
    var val = $this.value;                               //当前元素的值
    var name = $this.name;                               //当前元素的name，对应Rexp对象里的属性名
    var $tooltip = $this.nextSibling.nextSibling;        //提示信息，类名为tooltip的元素对象
    var $errTip = $tooltip.nextSibling.nextSibling;     //提示错误信息文本，类名为tipText的元素对象
    var $nullTip = $errTip.nextSibling.nextSibling;    //提示空信息文本，类名为tipText的元素对象

    //当前Input边框默认为红色，即默认当前格式是错误的
    $this.style.border = "1px solid red";

    //检测是否为空
    if(val.trim()===""){                                //判断是否为空
        $tooltip.style.visibility="visible";
        $tooltip.innerText = $nullTip.innerText;
        return false;
    }else{
        $tooltip.style.visibility="hidden";
    }
    //检测格式是否正确
    if(name=="confirmPassword"?val==newpassword:RegExp[name].test(val)){     //判断格式是否错误或密码是否一致
        $tooltip.style.visibility="hidden";
    }else{
        $tooltip.style.visibility="visible";
        $tooltip.innerText = $errTip.innerText;
        return false;
    }

    //恢复input样式
    $this.style.border = "1px solid #ccc";
    return true;
};

function subimit(){
    var formJson={};     //储存表单参数值
    var isErr = false;  //默认没有空

    //循环正则表达式里面所有的表单元素
    Object.keys(RegExp).forEach(function(key){          //key为RegExp中对应的属性名
        var $input = document.body.querySelectorAll("input[name='"+key+"']")[0];
        formJson[key] = $input.value;
        if(!onblur($input)&&!isErr){
            isErr = true;
        }
    });
    console.log(formJson);      //打印当前表单元素
    if(isErr) {
        userAlert("当前修改项有错误，请根据红色提示更改对应注册项！","javascript:void(0)")
        return false;
    }
    /********没有空切验证格式成功****下面编写提交表单对象到后台的代码******/
    /*************提交表单到后台完毕**********/
    gonext();
    return false;
}


//给后台传输邮箱 数据，后台发送邮件
function send_acount(){
    $.ajax({
        url: '/update_pwd/',
        type: 'POST',
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        data: {
          user_account: $('#user_account').val(),
          msg:0
        },
    success: function (data) {
      var dat = JSON.parse(data);
      if (dat.flag ==0){
        userAlert("该用户名不存在","javascript:void(0)");
      }else{
        valicate_code = dat.flag;
        userAlert("邮件已发送，请进入邮箱获取验证码！","javascript:void(0)");
        sendMessage();}
      }
    })
  }

function getnext(i) {
  if (i == "step2") {
    var check_code = document.getElementById("check_code").value;
    if (check_code == valicate_code) {
      document.getElementById(i).style.display = "block";
      document.getElementById("step1").style.display = "none";
    } else {
      userAlert("验证码填写有误，请重新输入", "javascript:void(0)")
    }
  }else{
    document.getElementById(i).style.display = "block";
    document.getElementById("step2").style.display = "none";
  }
}

//传输数据修改密码：
function gonext() {
    $.ajax({
        url: '/update_pwd/',
        type: 'POST',
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        data: {
          new_pwd: $('#new_pwd').val(),
          user_account: $('#user_account').val(),
          msg:1
        },
    success: function (data) {
      var dat = JSON.parse(data);
      userAlert(dat.flag, "/login");
    }
  })
}

