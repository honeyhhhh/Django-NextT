var phoneU = false
var count = 60
var curCount
var InterValObj
    // var BASE_URL="http://47.115.187.144:8777/";
var BASE_URL = 'http://118.31.245.67/';
if (sessionStorage.getItem('curCount')) {
    if (sessionStorage.getItem('isTrue') == 'true') {
        phoneU = true
    } else if (sessionStorage.getItem('isTrue') == 'false') {
        phoneU = false
    }
    curCount = parseInt(sessionStorage.getItem('curCount'))
    $('#register-register-tel').val(sessionStorage.getItem('phoneLocal'))
    $('#register-register-getvercode').attr('disabled', 'true')
    $('#register-register-getvercode').text(curCount + '秒')
    InterValObj = window.setInterval(SetRemainTime, 1000)
}
check()
$('#register-register-getvercode').on('click', function() {
    if (phoneU) {
        if (sessionStorage.getItem('curCount')) {
            curCount = parseInt(sessionStorage.getItem('curCount'))
        } else {
            curCount = count
        }
        $(this).attr('disabled', 'true')
        $(this).text(curCount + '秒')
        InterValObj = window.setInterval(SetRemainTime, 1000)

        let data = {
            phone: $('#register-register-tel').val()
        }

        let xhr = new XMLHttpRequest()

        xhr.open('post', BASE_URL + 'to')

        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (JSON.parse(xhr, this.responseText).status == '200') {
                    console.log('send successful')
                    swal({
                        title: '提交成功!',
                        icon: 'success',
                        button: '确定'
                    })
                } else if (JSON.parse(xhr.responseText).status == 'no-one') {
                    swal({
                        title: '请先登录!',
                        icon: 'info',
                        button: '确定'
                    })
                } else if (JSON.parse(xhr.responseText).status == 'phone-error') {
                    swal({
                        title: '电话号码错误或不存在!',
                        icon: 'warning',
                        button: '确定'
                    })
                } else if (JSON.parse(xhr.responseText).status == 'phone-repeat') {
                    swal({
                        title: '请不要重复发送!',
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

        xhr.setRequestHeader('Content-type', 'application/json') // 请求头根据接口文档设置

        xhr.send(JSON.stringify(data))
    } else {
        $('.register-register-phone-error').html('请输入正确的手机号')
    }
})

function SetRemainTime() {
    if (curCount == 0) {
        sessionStorage.removeItem('curCount')
        window.clearInterval(InterValObj);
        $('#register-register-getvercode').removeAttr('disabled')
        $('#register-register-getvercode').text('重新发送');
    } else {
        curCount--;
        sessionStorage.setItem('curCount', curCount)
        $('#register-register-getvercode').text(curCount + '秒')
    }
}

function check() {
    if (phoneU) {
        $('#register-register-getvercode').removeAttr('disabled')
        $('.register-register-submit').removeAttr('disabled')
    } else {
        $('#register-register-getvercode').attr('disabled', 'true')
        $('.register-register-submit').attr('disabled', 'true')
    }
}

$('#register-register-tel').on('keyup', function() {
    let num = $.trim($(this).val())
    let regnum = /^1\d{10}$/
    if (!regnum.test(num)) {
        phoneU = false
        $('.register-register-phone-error').text('请输入正确的手机号')
        sessionStorage.setItem('isTrue', 'false')
        sessionStorage.removeItem('curCount')
        window.clearInterval(InterValObj);
        $("#register-register-getvercode").removeAttr('disabled');
        $("#register-register-getvercode").text('获取验证码')
    } else {
        phoneU = true
        $('.register-register-phone-error').text('')
        sessionStorage.setItem('phoneLocal', num)
        sessionStorage.setItem('isTrue', 'true')
    }
    check()
})
$('.register-register-submit').on('click', function() {
    let direction = $('#register-register-direction').find('option:selected').text()
    let phoneNum = $('#register-register-tel').val()
    let vercode = $('#register-register-vercode').val()
    if (!phoneNum && !vercode || phoneNum && !vercode || !phoneNum && vercode) {
        swal({
            title: '请输入手机号或验证码!',
            icon: 'warning',
            button: '确定'
        })
    } else {
        let data = {
            code: vercode,
            department: direction,
            phone: phoneNum
        }

        let xhr = new XMLHttpRequest()

        xhr.open('post', BASE_URL + 'submit')

        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (JSON.parse(xhr, this.responseText).status == '200') {
                    swal({
                        title: '提交成功!',
                        text: '请留意后续面试通知,我们会以短信的方式发送给你',
                        icon: 'success',
                        button: '确定'
                    })
                    console.log('submit successful')
                } else if (JSON.parse(xhr, this.responseText).status == '500') {
                    swal({
                        title: '数据库加入失败!',
                        icon: 'warning',
                        button: '确定'
                    })
                } else if (JSON.parse(xhr.responseText).status == 'no-one') {
                    swal({
                        title: '请先登录!',
                        icon: 'info',
                        button: '确定'
                    })
                } else if (JSON.parse(xhr.responseText).status == 'code-error') {
                    swal({
                        title: '验证码错误!',
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

        xhr.setRequestHeader('Content-type', 'application/json') // 请求头根据接口文档设置

        xhr.send(JSON.stringify(data))
    }
})