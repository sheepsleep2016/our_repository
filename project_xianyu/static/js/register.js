var checkdata
var $form = document.form;
var RegExp = {     //映射input输入框的name值
  "username": /^[a-zA-Z]([_a-zA-Z0-9]{5,12})$/,		//字母开头，由数字与字母和下划线组成
  "password": /^[a-zA-Z]([_a-zA-Z0-9]{5,15})$/,		//字母开头，由数字与字母和下划线组成
  "confirmPassword": null,
  "email": /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/,
  "telphone": /^1(3|4|5|7|8|9)\d{9}$/,
  "identity": /^[1-9][0-9]{5}(19|20)[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|31)|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}([0-9]|x|X)$/
}

//页面加载完成efgregbrbhe
window.onload = function () {
  //获取所有需要验证的表单Input
  var $input = document.getElementsByClassName("formVal");

  //循环，给所有的需要验证的表单input绑定onfocus(获取焦点)与onblur(失去焦点)事件
  for (var i = 0; i < $input.length; i++) {
    var $this = $input[i];
    $this.onfocus = function () {                    //光标处于当前input
      this.style.border = "1px solid red";
    };

    $this.onblur = function () {                     //光标离开当前input
      onblur(this);   //传入当前对象
    }
  }
};

//向上追溯指定元素根节点
var closest = function (el, selector) {
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
var closeAlert = function ($this) {
  var $modal = closest($this, ".alert-contain-modal")
  $modal.remove();
};

//创建弹出框
var userAlert = function (msg) {
  var modal = document.createElement("div");
  modal.className = "alert-contain-modal";
  var _html = '<div class="alert-contain">';
  _html += '<div class="alert-header clearfixed">';
  _html += '<span>提示</span>';
  _html += '<a href="javascript:void(0)" class="close" onclick="closeAlert(this)">X</a>';
  _html += '</div>';
  _html += '<div class="alert-content">' + msg + '</div>';
  _html += '<div class="alert-footer">';
  _html += '<a class="btn" href="javascript:void(0)" onclick="closeAlert(this)">确定</a>';
  _html += '</div>';
  _html += '</div>';
  modal.innerHTML = _html;
  document.body.append(modal);
};

var onblur = function ($this) {
  if (!$this.tagName)return true;
  var password = document.body.querySelectorAll("input[name='password']")[0].value;
  var val = $this.value;                               //当前元素的值
  var name = $this.name;                               //当前元素的name，对应Rexp对象里的属性名
  var $tooltip = $this.nextSibling.nextSibling;        //提示信息，类名为tooltip的元素对象
  var $checkTip = $tooltip.nextSibling.nextSibling;     //提示是否已经注册
  var $errTip = $checkTip.nextSibling.nextSibling;     //提示错误信息文本，类名为tipText的元素对象
  var $nullTip = $errTip.nextSibling.nextSibling;      //提示空信息文本，类名为tipText的元素对象

  //当前Input边框默认为红色，即默认当前格式是错误的
  $this.style.border = "1px solid red";

  //检测是否为空
  if (val.trim() === "") {                                //判断是否为空
    $tooltip.style.visibility = "visible";
    $tooltip.innerText = $nullTip.innerText;
    return false;
  } else {
    $tooltip.style.visibility = "hidden";
  }
  //检测格式是否正确
  if (name == "confirmPassword" ? val == password : RegExp[name].test(val)) {     //判断格式是否错误或密码是否一致
    $.ajax({
      url: '/checkUser/',
      type: 'POST',
      headers: {"X-CSRFToken": $.cookie('csrftoken')},
      data: {num: val},
      success: function (data) {
        var dat = JSON.parse(data);
        if (dat.flag == 0) {
          $tooltip.style.visibility = "visible";
          $tooltip.innerText = $checkTip.innerText;
          return false
        } else {
          $tooltip.style.visibility = "hidden";
          return true
        }
      }
    })
  } else {
    $tooltip.style.visibility = "visible";
    $tooltip.innerText = $errTip.innerText;
    return false;
  }

  // if(name='checknum'){
  //     if(checkdata==val){
  //         $tooltip.style.visibility="hidden";
  //         return true
  //     }
  //     else{
  //         $tooltip.style.visibility="visible";
  //         $tooltip.innerText = $checkTip.innerText;
  //         return false
  //     }
  // }else{
  //     $tooltip.style.visibility="hidden";
  // }

  //恢复input样式
  $this.style.border = "1px solid #ccc";
  return true;
};

function subimit() {
  var formJson = {};     //储存表单参数值
  var isErr = false;  //默认没有空

  //循环正则表达式里面所有的表单元素
  Object.keys(RegExp).forEach(function (key) {          //key为RegExp中对应的属性名
    var $input = document.body.querySelectorAll("input[name='" + key + "']")[0];
    formJson[key] = $input.value;
    if (!onblur($input) && !isErr) {
      isErr = true;
    }
  });
  console.log(formJson);      //打印当前表单元素
  if (isErr) {
    userAlert("当前注册项有错误，请根据红色提示更改对应注册项！");
    return false;
  } else if (checkdata != document.getElementById("u_check").value) {
    console.log(formJson)
    userAlert("验证码输入有误，请重新输入")
    return false;
  } else {
    return true
  }

  /********没有空切验证格式成功****下面编写提交表单对象到后台的代码******/


  /*************提交表单到后台完毕**********/

}


function button() {
  var formJson = {};     //储存表单参数值
  var isErr = false;  //默认没有空

  //循环正则表达式里面所有的表单元素
  Object.keys(RegExp).forEach(function (key) {          //key为RegExp中对应的属性名
    var $input = document.body.querySelectorAll("input[name='" + key + "']")[0];
    formJson[key] = $input.value;
    if (!onblur($input) && !isErr) {
      isErr = true;
    }
  });
  if (isErr) {
    userAlert("当前注册项有错误，请根据红色提示更改对应注册项！");
    return false;
  }  else {
  settime()
  val1 = document.getElementById("u_email").value;
  console.log(val1);
  $.ajax({
    url: '/send000/',
    type: 'POST',
    headers: {"X-CSRFToken": $.cookie('csrftoken')},
    data: {email: val1},
    success: function (data) {
      var dat = JSON.parse(data);
      checkdata = dat.flag
    }
  });
    return true
  }

}

function disable() {
  document.getElementById("accept").disabled = true;
  $(".btu").attr("style", "background:gray");
}


function enable() {
  document.getElementById("accept").disabled = false;
  $(".btu").attr("style", "background:green");

}
// 初始化
$(document).ready(function () {
  //没有勾选同意协议则注册按钮置灰
  var b = $(".accept");
  if (b.disabled = true) {
    $(".btu").attr("style", "background:gray");
  }
});

// 计时器
var InterValObj; //timer变量，控制时间
var count = 60; //间隔函数，1秒执行
var curCount;//当前剩余秒数
var valicate_code;//定义一个全局变量接收 产生的验证码
//发送邮箱验证码
function settime() {
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