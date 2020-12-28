var InterValObj; //timer变量，控制时间
			var count = 60; //间隔函数，1秒执行
			var curCount;//当前剩余秒数
			//发送短信验证码
			function sendMessage() {
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