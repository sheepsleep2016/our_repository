/**
 * Created by tarena on 19-5-22.
 */

function checkvalid() {
  var title = $('#title').val();
  var msg = $('#message').val();
  var order_id = $('#order_id').val();
  console.log(title, msg, order_id);
  if (title == "") {
    alert("请输入标题");
  } else if (msg == "") {
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
      title: $('#title').val(),
      content: $('#message').val(),
      order_id: $('#order_id').val(),
    },
    success: function (data) {
      var dat = JSON.parse(data);
      if (dat.flag == 0) {
        alert("您的问题我们已经收到，我们后续会对订单进行核查，并将处理结果通过邮件或者电话告知您");
        window.location.href = "/";
      }
    }
  })
}
