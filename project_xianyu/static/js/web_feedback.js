/**
 * Created by tarena on 19-5-22.
 */

function checkvalid() {
  var msg = $('#message').val();
  if (msg == "") {
    alert("请输入问题详情");
  } else {
    check()
  }
}

function check() {
  $.ajax({
    url: '/connecting/1/',
    type: 'POST',
    headers: {"X-CSRFToken": $.cookie('csrftoken')},
    data: {
      content: $('#message').val(),
    },
    success: function (data) {
      var dat = JSON.parse(data);
      if (dat.flag == 0) {
        alert("您的问题我们已经收到，我们后续会对问题进行检查，谢谢您对于本网站的建议或意见！");
        window.location.href = "/";
      }
    }
  })
}
