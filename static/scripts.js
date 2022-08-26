
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