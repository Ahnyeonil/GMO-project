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
                                     <div class="card-image"><img src="../../static/images/${file}"></div>
                                     <div class="card_content">
                                       <h2 class="card_title">${title}</h2>
                                       <p class="card_text">${desc}</p>
                                       <a href="/test"><button class="btn card_btn">Read More</button></a>
                                     </div>
                                   </div>
                                 </li>`

                $('.cards').append(temp_html)
            }
        }
    })
}

// function detail_list_call() {
//
//     $.ajax({
//         type: "GET",
//         url: "/detail/list",
//         data: {},
//         success: function (response) {
//
//             console.log(response)
//
//             // let posts = response['posts']
//             //
//             // for (let i = 0; i < posts.length; i++) {
//             //     let title = posts[i]['title']
//             //     let desc = posts[i]['desc']
//             //     // let writerid = posts[i]['writerid']
//             //     // let star = posts[i]['star']
//             //     let file = posts[i]['file']
//             //
//             //     let temp_html = ``
//             //
//             //     $('.cards').append(temp_html)
//             // }
//         }
//     })
// }