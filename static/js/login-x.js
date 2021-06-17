$(document).keyup(function(event){
	　　if(event.keyCode ==13){
	　　　　$(".login-submit").trigger("click");
		}
});


$('.login-submit').on('click', function() {
    let number = $('#student-number').val()
    let password = $('#student-password').val()
    let csrftoken = $("[name = 'csrfmiddlewaretoken']").val()
    if (!number && !password || number && !password || !number && password) {
        swal({
            title: '请输入学号或密码!',
            icon: 'warning',
            button: '确定'
        })
    } else {
        let data = {
            id: number,
            pwd: password,
			csrfmiddlewaretoken: $("[name = 'csrfmiddlewaretoken']").val()
        }
        let xhr = new XMLHttpRequest()

        xhr.open('post', 'http://118.31.245.67/' + 'login/')

        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (JSON.parse(xhr.responseText).status == '200') {
                    window.location.href = '/register/'
                } else if (JSON.parse(xhr.responseText).status == '302') {
                    swal({
                        title: '您已经报名!',
                        icon: 'info',
                        button: '确定'
                    })
                } else if (JSON.parse(xhr.responseText).status == 'id-pwd-error') {
                    swal({
                        title: '学号或密码错误!',
                        icon: 'warning',
                        button: '确定'
                    })
                }
            } else if (xhr.status != 200) {
                swal({
                    title: '未知错误,请加群792771841联系管理员',
                    icon: 'warning',
                    button: '确定'
                })
            }
        }
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
        xhr.setRequestHeader('Content-type', 'application/json') // 请求头根据接口文档设置

        xhr.send(JSON.stringify(data))
    }
})
