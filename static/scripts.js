function introgangneung() {

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
