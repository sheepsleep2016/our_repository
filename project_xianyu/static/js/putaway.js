/**
 * Created by tarena on 19-5-23.
 */
//下面用于多图片上传预览功能
function setImagePreviews(avalue) {
  var docObj = document.getElementById("files");
  var dd = document.getElementById("preview");
  dd.innerHTML = "";
  var fileList = docObj.files;
  for (var i = 0; i < fileList.length; i++) {
    dd.innerHTML += "<div style='float:left' > <img id='img" + i + "'  /> </div>";
    var imgObjPreview = document.getElementById("img" + i);
    if (docObj.files && docObj.files[i]) {
      //火狐下，直接设img属性
      imgObjPreview.style.display = 'block';
      //控制缩略图大小
      imgObjPreview.style.width = '5rem';
      imgObjPreview.style.height = '5rem';
      //imgObjPreview.src = docObj.files[0].getAsDataURL();
      //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式
      imgObjPreview.src = window.URL.createObjectURL(docObj.files[i]);
    }
    else {
      //IE下，使用滤镜
      docObj.select();
      var imgSrc = document.selection.createRange().text;
      alert(imgSrc);
      var localImagId = document.getElementById("img" + i);
      //必须设置初始大小
      localImagId.style.width = "5rem";
      localImagId.style.height = "5rem";
      //图片异常的捕捉，防止用户修改后缀来伪造图片
      try {
        localImagId.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";
        localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;
      }
      catch (e) {
        alert("您上传的图片格式不正确，请重新选择!");
        return false;
      }
      imgObjPreview.style.display = 'none';
      document.selection.empty();
    }
    if (docObj.files.length > 5) {
      alert('最多只能添加5张图片');
      return;
    }
  }
  return true;
}

function clearNoNum(obj) {
  obj.value = obj.value.replace(/[^\d.]/g, ""); //清除"数字"和"."以外的字符
  obj.value = obj.value.replace(/^\./g, ""); //验证第一个字符是数字而不是
  obj.value = obj.value.replace(/\.{2,}/g, "."); //只保留第一个. 清除多余的
  obj.value = obj.value.replace(".", "$#$").replace(/\./g, "").replace("$#$", ".");
  obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/, '$1$2.$3'); //只能输入两个小数
}

function checkvalid() {
    var commodity_name=$("#commodity_name").val();
    var commodity_discrib=$("#commodity_discrib").val();
    var commodity_price=$("#commodity_price").val();
    var imgs=$("#files").val();
    if(commodity_name==""){
    alert("请输入物品名称");
    }else if(commodity_discrib=="") {
    alert("请添加物品描述");
    }else if (commodity_price==""){
    alert("请输入物品单价");
    }else if (files==""){
    alert("请添加图片");
    }else{
    sendmsg();
    }
}

function sendmsg() {
    var docObj = document.getElementById("files");
    var fileList = docObj.files;
    var list_name =[];
    var dataform = new FormData();
    // var list_content = [];
    var reader = new FileReader();
    for (var i = 0; i < fileList.length; i++) {
      list_name.splice(0,0,fileList[i].name);
      dataform.append("i",fileList[i]);
      // reader.readAsBinaryString(fileList[i]);
      // list_content.splice(0,0,reader.result);
    }
    var comm_name= $('#commodity_name').val();
    var comm_type= $('#commodity_type').val();
    var comm_discrib=$('#commodity_discrib').val();
    var comm_count=$('#commodity_count').val();
    var comm_price=$('#commodity_price').val();
    // var imgs00=fileList;
    var imgsname=list_name;
    var comm_province=$('#province').val();
    var comm_city=$('#city').val();
    var isactive=$('#isactive').val();

    dataform.append("comm_name",comm_name);
    dataform.append("comm_type",comm_type);
    dataform.append("comm_discrib",comm_discrib);
    dataform.append("comm_count",comm_count);
    dataform.append("comm_price",comm_price);
    dataform.append("comm_province",comm_province);
    dataform.append("comm_city",comm_city);
    dataform.append("isactive",isactive);
    dataform.append("imgsname",imgsname);
    dataform.append("fileList",fileList);

    console.log(fileList,list_name);
    $.ajax({
        url: '/putaway/',
        type: 'POST',
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        data: dataform,

          // comm_name: $('#commodity_name').val(),
          // comm_type: $('#commodity_type').val(),
          // comm_discrib:$('#commodity_discrib').val(),
          // comm_count:$('#commodity_count').val(),
          // comm_price:$('#commodity_price').val(),
          // imgs00:fileList,
          // imgsname:list_name,
          // comm_province:$('#province').val(),
          // comm_city:$('#city').val(),
          // isactive:$('#isactive').val(),

    success: function (data) {
      var dat = JSON.parse(data);
      if (dat.flag ==0){
        window.location.href="/personal";
      }else{console.log(dat);
      alert("发布失败，请您核查信息重新发布");}
    }
  })
}
//
// window.onload =function(){
//   var content000 = $("#discrib").val();
//   document.getElementById('commodity_discrib').innerHTML = content000
// };

