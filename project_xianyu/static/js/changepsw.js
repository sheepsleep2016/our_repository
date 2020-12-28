var $form = document.form;
var RegExp = {     //映射input输入框的name值
  "newpassword": /^[a-zA-Z]([_a-zA-Z0-9]{5,12})$/,		//字母开头，由数字与字母和下划线组成
  "user_pwd":/^[_a-zA-Z0-9]{4,15}$/,
  "confirmnewPassword": null
}

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
}

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
}


//关闭弹出框
var closeAlert = function($this){
    var $modal = closest($this,".alert-contain-modal")
    $modal.remove();
}

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
    if(name=="confirmnewPassword"?val==newpassword:RegExp[name].test(val)){     //判断格式是否错误或密码是否一致
        $tooltip.style.visibility="hidden";
    }else{
        $tooltip.style.visibility="visible";
        $tooltip.innerText = $errTip.innerText;
        return false;
    }

    //恢复input样式
    $this.style.border = "1px solid #ccc";
    return true;
}

function subimit(){
    var formJson={};     //储存表单参数值
    var isErr = false;  //默认没有空

    //循环正则表达式里面所有的表单元素
    Object.keys(RegExp).forEach(function(key){          //key为RegExp中对应的属性名
        var $input = document.body.querySelectorAll("input[name='"+key+"']")[0];
        formJson[key] = $input.value;
        if(!onblur($input)&&!isErr){
            isErr = true;
        };
    })
    console.log(formJson);      //打印当前表单元素
    if(isErr) {
        userAlert("当前修改项有错误，请根据红色提示更改对应注册项！","javascript:void(0)")
        return false;
    }else{
        console.log(formJson);
        get_msg()
    }

    /********没有空切验证格式成功****下面编写提交表单对象到后台的代码******/


    /*************提交表单到后台完毕**********/

    return false;
}

function get_msg() {
    $.ajax({
        url: '/personal/changepwd',
        type: 'POST',
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        data: {
          pwd_old: $('#pwd_old').val(),
          pwd_new: $('#pwd_new').val(),
        },
    success: function (data) {
      var dat = JSON.parse(data);
      if (dat.msg == 0){
        userAlert("密码修改成功!","/personal");
      }else{console.log(dat);
        userAlert("原始密码输入错误","javascript:void(0)");}
    }
  })
}