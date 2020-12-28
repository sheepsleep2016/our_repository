/**
 * Created by tarena on 19-5-24.
 */
function setTotal(){
	var allprice=0;//总价格
	var allnum=0;//总数量
	$(".checkitem").each(function(){
		if($(this).hasClass('oncheck')){
			var num=parseInt($(this).parents('[priceOne]').find('input[name=count]').val());//单个商品的购买数量
			var price=$(this).parents('[priceOne]').find('[unitprice]').text();//商品单价需要从后台获取
			allprice+=num*price;//每样商品的总价
			allnum+=num;
		}
	});
	$(".allprice").html(allprice.toFixed(2));
	$(".allnum").html(allnum);
}
setTotal();


//手动修改文本框商品数量与库存的限制
function amount_input(tag,sellprice,stock){
	var amount=parseInt($(tag).val());
	if(isNaN(amount)){
		layer.msg('最少购买量为1');
		$(tag).val(1);
	}else{
		if(amount>stock){
			layer.msg('购买数量不能大于库存');
			$(tag).val(stock);
		}else if(amount<1){
			layer.msg('最少购买量为1');
			$(tag).val(1);
		}
	}
	var val=parseFloat(sellprice)*parseInt($(tag).val());
	setTotal();
}
// 全选
$('#checkall').click(function(){
	$(this).toggleClass('oncheck');
	if($(this).hasClass('oncheck')){
		$('.checkitem').addClass('oncheck');
		setTotal();
	}else{
		$('.checkitem').removeClass('oncheck');
		setTotal();
	}
});
//单选
$('.checkitem').click(function(){
	$(this).toggleClass('oncheck');
	var itemsleng=$('.checkitem').length;
	var checkedleng=$('[priceOne]').find('i').filter('.oncheck').length;
	if(checkedleng==itemsleng){
		$('.checkall').addClass('oncheck');
		setTotal();
	}else{
		$('.checkall').removeClass('oncheck');
		setTotal();
	}
});
// 购买数量加
function plus(tag,sellprice,stock){
	var _this=$(tag);
	var input=_this.prev('input');
	if(_this.prev('input[disabled]').length>0){
		return;
	}
	var amount=parseInt(input.val());
	amount++;
	if(amount>stock){
		return layer.msg('购买数量不能大于库存');
	}else{
		input.val(amount);
		setTotal();
	}
}
// 购买数量减
function minus(tag,sellprice,stock){
	var _this=$(tag);
	var input=_this.next('input');
	if(_this.next('input[disabled]').length>0){
		return;
	}
	var amount=parseInt(input.val());
	amount--;
	if(amount<=0){
		return layer.msg('购买数量不能小于1');
	}else{
		input.val(amount);
		setTotal();
	}
}
