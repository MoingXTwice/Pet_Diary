/*git commit을 위한 js 파일입니다. 파일명을 수정하셔도 되고 그냥 사용하셔도 됩니다.*/
function postDiary() {
    let title = $('#title').val()
    let content = $('#content').val()
    let image = $('#image')[0].files[0]

    let form_data = new FormData()

    form_data.append('title', title)
    form_data.append('content', content)
    form_data.append('image', image)

    $.ajax({
        type: "POST",
        url: "/diary/post",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response['msg'])
        }

    })
}

function login() {
    let user_id = $('#user_id').val()
    let password = $('#password').val()

    if (user_id == "") {
        alert('아이디를 입력해주세요.')
        return;
    } else if (password == "") {
        alert('비밀번호를 입력해주세요.')
        return;
    }

    $.ajax({
        type: "POST",
        url: "/login",
        data: {
            'user_id': user_id,
            'password': password
        },
        success: function (response) {
            console.log(response)
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace('/' + user_id);
            } else {
                alert(response['msg']);
            }
        }

    })
}

function sign_up() {
    let user_id = $('#user_id').val()
    let password = $('#password').val()
    let name = $('#name').val()

    if (user_id == "") {
        alert('아이디를 입력해주세요.')
        return;
    } else if (password == "") {
        alert('비밀번호를 입력해주세요.')
        return;
    } else if (name == "") {
        alert('이름을 입력해주세요.')
        return;
    }

    $.ajax({
        type: "POST",
        url: "/sign_up",
        data: {
            'user_id': user_id,
            'password': password,
            'name': name
        },
        success: function (response) {
            window.location.replace('/login');
        }
    });

}

$(document).ready(function () {

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        todayHighlight: true,
        toggleActive: true
    });

});

function logout() {
    $.removeCookie('mytoken', {path: '/'});
    alert('정상적으로 로그아웃 되었습니다.')
    window.location.href = "/login"
}