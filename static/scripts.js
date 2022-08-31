function signup() {
    $.ajax({
        type: "POST",
        url: "/signup",
        data: {
            userid: user_id,
            userpw: user_pw,
            username: user_name,
            usernickname: user_nickname
        },
        success: function (response) {

            if (response['msg'] === '회원 가입 완료!'){
                alert(response['msg'])
                location.replace('/login')
            }
            else if (response['msg'] === '동일한 id가 존재합니다!') {
                alert(response['msg'])
                $('#member_id').val('')
            }
            else if (response['msg'] === '동일한 닉네임이 존재합니다!') {
                alert(response['msg'])
                $('#member_nickname').val('')
            }

        }
    })
}

// 포스팅-속초
function save_post_sc() {
    let city = $('#city').val()
    let dst = $('#dst').val()
    let star = $('#star').val()
    let title = $('#title').val()
    let dsc = $('#dsc').val()

    $.ajax({
        type: 'POST',
        url: '/post',
        data: { city_give:city, dst_give:dst, star_give:star, title_give:title, dsc_give:dsc},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}