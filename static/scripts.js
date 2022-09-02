function weather() {
    const API_KEY = "222e7197c6498dd6ede62a9fe39c3dee";
    const weather_gangneung = "https://api.openweathermap.org/data/2.5/weather?q=gangneung&appid=222e7197c6498dd6ede62a9fe39c3dee&units=metric";
    const weather_sokcho = "http://api.openweathermap.org/data/2.5/weather?q=sokcho&appid=222e7197c6498dd6ede62a9fe39c3dee&units=metric";
}

function weather_sokcho() {
    $.ajax({
        type: "GET",
        url: "http://api.openweathermap.org/data/2.5/weather?q=sokcho&appid=222e7197c6498dd6ede62a9fe39c3dee&units=metric",
        data: {},
        success: function(res) {
            let temp = res["main"]["temp"]
            let temp_html = `
                <a href="/sokcho/intro">
                    <div class="card1">
                        <div class="card-img">
                            <img src="https://i.redd.it/b3esnz5ra34y.jpg">
                        </div>
                        <div class="card_title">
                            <span>${temp} ℃</span>
                            <p>속초</p>
                        </div>
                    </div>
                </a>
            `
            $(".cards-list").append(temp_html)
        }
    })
}

function weather_gangneung() {
    $.ajax({
        type: "GET",
        url: "http://api.openweathermap.org/data/2.5/weather?q=gangneung&appid=222e7197c6498dd6ede62a9fe39c3dee&units=metric",
        data: {},
        success: function(res) {
            let temp = res["main"]["temp"]
            let temp_html = `
                <a href="/gangneung/intro">
                    <div class="card1">
                        <div class="card-img">
                            <img src="https://i.redd.it/b3esnz5ra34y.jpg">
                        </div>
                        <div class="card_title">
                            <span>${temp} ℃</span>
                            <p>강릉</p>
                        </div>
                    </div>
                </a>
            `
            $(".cards-list").append(temp_html)
        }
    })
}
 
function gangneung_list_call() {
    $.ajax({
        type: "GET",
        url: "/gangneung/intro/list",
        data: {},
        success: function (response) {

            let locations = response['locations']

                for (let i = 0; i < locations.length; i++) {
                    let title = locations[i]['title']
                    let desc = locations[i]['desc']
                    let img = locations[i]['image']

                    let temp_html = `<div class="col">
                                        <div class="card h-100">
                                            <img src=${img}
                                                 class="card-img-top">
                                            <div class="card-body">
                                                <h5 class="card-title">${title}</h5>
                                                <p class="card-text">${desc}</p>
                                            </div>
                                        </div>
                                    </div>`

                    $('#cards-box').append(temp_html)
                }
        }
    })
}

function post_list_call() {

    $.ajax({
        type: "GET",
        url: "/post/list",
        data: {},
        success: function (response) {

            let posts = response['posts']

            for (let i = 0; i < posts.length; i++) {
                let title = posts[i]['title']
                let desc = posts[i]['desc']
                // let writerid = posts[i]['writerid']
                // let star = posts[i]['star']
                let file = posts[i]['file']

                let temp_html = `<li class="card-item">
                                   <div class="card">
                                     <div class="card-image"><img class="object-fix" src="../../static/images/${file}" alt="사진"></div>
                                     <div class="card_content">
                                       <h2 class="card_title">${title}</h2>
                                       <p class="card_text">${desc}</p>
                                       <a href="#detail-popup"><button class="btn card_btn" onclick="simple_detail_call('${title}')">Read More</button></a>
<!--                                       <a href="/detail"><button class="btn card_btn">Read More</button></a>-->
                                     </div>
                                   </div>
                                 </li>`

                $('.cards').append(temp_html)

            }
        }
    })
}

function detail_list_call(id) {

    $.ajax({
        type: "POST",
        url: "/detail/list",
        data: {idstr: id},
        success: function (response) {

            console.log(response)

            let hiddenid = response['hiddenid']
            $('.hiddenid').val(hiddenid)

            // postdetail
            let postdetail = response['postdetail']

            let file = postdetail['file']
            let title = postdetail['title']
            let desc = postdetail['desc']
            let writerid = postdetail['writerid']
            let star = postdetail['star']
            let star_img = '⭐'.repeat(star)

            let temp_html = `<img src="../../static/images/${file}">
                                <div class="content-title">
                                  <h2>${title}</h2>
                                  <span class="star-rate">${star_img}</span>
                                  <p>${desc}</p>
                                  <p>${writerid}</p>
                                </div>`


            let detail_post = $('.detail-post')

            detail_post.empty()
            detail_post.append(temp_html)


            // comment
            let comments = response['comments']
            let commentlist = $('.comments')

            commentlist.empty()

            for (let i = 0; i < comments.length; i++) {

                let comment = comments[i]['comment']
                let nickname = comments[i]['nickname']
                let commentid = comment[i]['_id']
                // let password = comments[i]['password']
                // let posting = comments[i]['posting']

                let temp_html = `<div class="comment">
                                  <h4 class="comment-author">${nickname}</h4>
                                  <p>${comment}</p>
                                  <a href="#" class="close" onclick="delete_comment(${commentid})">&times;</a>
                                  <input type="hidden" value="${commentid}" />
                                </div>`


                commentlist.append(temp_html)

            }

            // count
            let count = comments.length
            let countclass = $('.comment-head > span')
            countclass.text(` 댓글 ${count}개`)

        }
    })
}

function delete_comment(commentid) {

    let password_required = prompt("정말 삭제를 원하시면 비밀번호를 입력해주세요")

    if (password_required === "" || password_required == null)
        return alert("비밀번호를 입력하지 않으면 삭제할 수 없습니다")

    $.ajax({
        type: 'POST',
        url: '/gangneung/detail/deletecomment',
        data: {commentid: commentid, commentpwd: password_required},
        success: function (response) {
            if(response !== undefined) {
                alert(response['msg'])
                window.location.reload()
            }
        }
    });
}

function simple_detail_call(title) {

    $.ajax({
        type: "POST",
        url: "/post/simpledetail",
        data: {titlename: title},
        success: function (response) {

            if(response['postdetail'] === undefined)
                alert(response['msg'])

            let postdetail = response['postdetail']

            let file = postdetail['file']
            let title = postdetail['title']
            let desc = postdetail['desc']
            let writerid = postdetail['writerid']
            let star = postdetail['star']
            let star_img = '⭐'.repeat(star)

            let temp_html = `<li class="detailcard-item">
                                   <div class="detailcard">
                                     <div class="detailcard-image"><img src="../../static/images/${file}" alt="사진" class="object-fix-simpledetail"></div>
                                     <div class="detailcard_content">
                                       <h2 class="detailcard_title">장소 : ${title}</h2>
                                       <p class="detailcard_text">설명 : ${desc}</p>
                                       <p class="detailcard_text">평점 : ${star_img}</p>
                                       <p class="detailcard_text">작성자 : ${writerid}</p>
                                     </div>
                                   </div>
                                 </li>`

            let detail_post = $('.detail-posting')

            detail_post.empty()
            detail_post.append(temp_html)
            $('#detail-popup').attr("opacity", "1");

        }
    })
}

// 포스팅-속초
function save_post_sc() {
    let writerid = $('#writerid').val()
    let dst = $('#dst').val()
    let star = $('#star').val()
    let title = $('#title').val()
    let desc = $('#desc').val()
    let file = $('#file').val()

    $.ajax({
        type: 'POST',
        enctype: 'multipart/form-data',
        url: '/post',
        data: { writerid:writerid, dst:dst, star:star, title:title, desc:desc, file:file},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

