/**
 * Created by tarena on 19-5-25.
 */
$(function () {
  //1.全选和取消全选
  var isChecked = false;
  $(".checkAll").click(function () {
    isChecked = !isChecked;
    if (isChecked) {
      //切换选中样式
      $(this)
        .attr("src", "/static/image/product_true.png")
        .attr("checked", "true");//修改状态标记;
    } else {
      $(this)
        .attr("src", "/static/image/product_normal.png")
        .removeAttr("checked");
    }
    total();
  });

  //3.数量加减
  $(".add").click(function () {
    //获取输入框的值
    var value = $(this).prev().val();
    //值+1
    var maxcount = $(this).parents(".goods_list_td")
        .find(".goods_count b").html();
    // $("#maxcount").val();
    console.log(maxcount);
    if (value < maxcount) {
      $(this).prev().val(++value);
      //修改总金额
      changePrice($(this), value);
      total()
    }
  });
  $(".minus").click(function () {
    var value = $(this).next().val();
    value--;
    if (value < 1) {
      value = 1;
    }
    $(this).next().val(value);
    //修改总金额
    changePrice($(this), value);
    total();
  });
  //监听输入框数量变化
  $(".goods_count input").blur(function () {
    //输入框的值是正整数
    //出现小数，负数，非数字字符串，一律显示为1
    var value = $(this).val();
    var r1 = Number(value);//是否数字字符串
    var r2 = value >= 1;//是否是>=1的正数
    //使用小数点分割字符串，
    //如果不存在小数点，数组长度为1，存在，>1
    var r4 = Number(value) <= Number($("#maxcount").val());
    var r3 = value.split('.').length == 1;
    if (r1 && r2 && r3 && r4) {
      //value合法

    } else {
      value = 1;
      $(this).val(value);
    }
    changePrice($(this), value);
    total();
  });

	//计算总数量和总价格
	function total() {
    var fees = 0;//特殊费用（检验费）
    var pstr = document.getElementById("comm_sum").innerText;
    var price = Number(pstr.substring(1)).toFixed(2);
    console.log(price);
    var sum;//总价格

    //获取被选中商品的总数量和总价格进行累加
    //each()遍历列表，
    //每取到一个元素就自动调用相关函数
    $("img[checked]").each(function () {
    //当前获取的元素
    var price00 = Number(price);
    // var price00 = Number(pstr00.substring(1));
    if (price00 < 100) {
      fees += price00 * 0.01;
      console.log("1111111111");
    }
    if (100< price00 && price00 < 1000) {
      fees += 1+(price00 - 100) * 0.02;
      console.log("2222222222");
    }
    if (1000< price00 && price00 < 10000) {
      fees += 19+(price00 - 1000) * 0.04;
      console.log("3333333333");
    }
    if (price00 > 10000) {
      fees += 379+(price00 - 10000) * 0.08;
      console.log("4444444444");
    }
    // $(".survey_fees").html(fees + "元");
    });
    //显示
    fees = Number(fees.toFixed(2));
    price = Number(price).toFixed(2);
    sum = (Number(price)+fees).toFixed(2);
    var to_pr = document.getElementById('total_price');
    var su_fe = document.getElementById('survey_fees');
    var to_pay = document.getElementById('total_pay');
    to_pr.innerHTML=price + "元";
    su_fe.innerHTML=fees + "元";
    to_pay.innerHTML=sum + "元";
    // $(".total_price").html(price + "元");
    // $(".survey_fees").html(fees + "元");
    // $(".total_pay").html(sum + "元");
    // });
  }

  //价格联动
  function changePrice(that, n) {//元素对象，数量
    //获取单价"￥5050"
    var pstr = that.parents(".goods_list_td")
        .find(".goods_price span").html();
    var price = pstr.substring(1);//"5050"
    //获取总价
    //总价保留两位小数
    var sum = (n * price).toFixed(2);
    that.parents(".goods_list_td")
        .find(".goods_sum b").html("￥" + sum);
  }
});

function order(){
    var pristr = document.getElementById("total_pay").innerText;
    $.ajax({
      url: '/paying/',
      type: 'POST',
      headers: {"X-CSRFToken": $.cookie('csrftoken')},
      data: {
        province: $("#province").val(),
        city: $("#city").val(),
        position: $("#position").val(),
        order_user: $("#order_user").val(),
        phone: $("#order_phone").val(),
        count: $("#count").val(),
        comid: Number(document.getElementById("getcomid").innerText),
        price: Number(pristr.substring(0, pristr.length - 1))
        // price: Number(.replace(/[^0-9]/ig,""))
        // price:parseInt(document.getElementById("total_pay").innerText)
      },
      success: function (data) {
        var dat = JSON.parse(data);
        if (dat.falg == 0){
          alert("不好意思，宝贝已被他人抢走");
          window.location.href = "/";}
        else{
          console.log(dat.flag);
          window.location.href = dat.flag;}
      }
    })
  }

var checkdata
var $form = document.form;
var RegExp = {
  "2": /^[\u4e00-\u9fa5]{2,4}$/,
  "3": /^1(3|4|5|7|8|9)\d{9}$/,
};

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

var onblur = function ($this) {
  if (!$this.tagName)return true;
  var val = $this.value;                               //当前元素的值
  var name = $this.name;                               //当前元素的name，对应Rexp对象里的属性名
  var $tooltip = $this.nextSibling.nextSibling;        //提示信息，类名为tooltip的元素对象
  var $errTip = $tooltip.nextSibling.nextSibling;     //提示错误信息文本，类名为tipText的元素对象
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
  if (name == "1" ? true : RegExp[name].test(val)) {
    $tooltip.style.visibility = "hidden";
  } else {
    $tooltip.style.visibility = "visible";
    $tooltip.innerText = $errTip.innerText;
  }
  $this.style.border = "1px solid #ccc";
  return true;
};
// window.onload =function(){
//   var InterValObj; //timer变量，控制时间
//   var count = 10; //间隔函数，1秒执行
//   var curCount;//当前剩余秒数
//   curCount = count;
//   // 设置button效果，开始计时
//   InterValObj = window.setInterval(SetRemainTime, 1000); // 启动计时器timer处理函数，1秒执行一次
//
//   //timer处理函数
//   function SetRemainTime() {
//     // console.log(curCount);
//     if (curCount == 0) {//超时重新获取验证码
//       send_msg();
//       window.clearInterval(InterValObj);// 停止计时器
//
//     } else {
//         curCount--;
//       }
//     }
//
//   //给后台传输数据
//   function send_msg() {
//     $.ajax({
//       url: '/changelock/',
//       type: 'POST',
//       headers: {"X-CSRFToken": $.cookie('csrftoken')},
//       data: {
//         comid: Number(document.getElementById("getcomid").innerText),
//         msg: 0
//       },
//       success: function (data) {
//         var dat = JSON.parse(data);
//         if (dat.flag == 0) {
//           alert("支付超时");
//         }
//       }
//     })
//   }
// };

// window.onbeforeunload   =   function(){
//       var   n   =   window.event.screenX   -   window.screenLeft;
//       var   b   =   n   >   document.documentElement.scrollWidth-20;
//       if(b   &&   window.event.clientY   <   0   ||   window.event.altKey)
//       {
//           alert("是关闭而非刷新");
//           window.event.returnValue   =   "是否关闭？";
//       }else{
//              alert("是刷新而非关闭");
//      }
// };
