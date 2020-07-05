const CARD_STATUS_CLOSE = "0";
const CARD_STATUS_OPEN = "1";
const CARD_STATUS_FLIP = "2";

function pickCard(card_id, user_id) {
    let current_element = $('#card_'+card_id.toString());
    current_element.parent().css('pointer-events', 'none');
    current_element.parent().off('click');
    $.ajax({
        url: "api/v1/cards/pick",
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        beforeSend : function(xhr) {
            if (localStorage.getItem('token')) {
                xhr.setRequestHeader("Authorization", "JWT " +  localStorage.getItem('token'));
            }
        },
        data: JSON.stringify({'id': card_id, 'status': '1'}),
        success: function (data) {
            fetch_user_info(user_id);
            let hold = [];  // list of cards that hold to flip back when unmatched
            for (let i=0;i<data.length;i++){
                let card = data[i];
                let card_element = $('#card_'+card.id.toString());
                card_element.find('span').first().remove();
                card_element.addClass('flip').append("<span class='align-middle'>"+ card.value +"</span>");
                if (card.status === CARD_STATUS_CLOSE){
                    hold.push(card_element);
                }
            }
            setTimeout(function () {
                for (let i=0;i<hold.length;i++){
                    hold[i].removeClass('flip');
                    hold[i].find('span').first().remove();
                    hold[i].parent().css('pointer-events', 'auto');
                    hold[i].parent().on('click', function () {
                        pickCard(hold[i].data('id'), user_id);
                    });
                }
            }, 500)


        }
    });
}

function newGame(user_id) {
    $.ajax({
        url: "api/v1/cards/new-game",
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        beforeSend : function(xhr) {
            if (localStorage.getItem('token')) {
                xhr.setRequestHeader("Authorization", "JWT " +  localStorage.getItem('token'));
            }
        },
        data: JSON.stringify({'user_id': user_id}),
        success: function (data) {
            $('#clickAmountValue').text('-');
            fetch_board_info();
            let board_element = $('#board .row');
            board_element.empty();
            for (let i=0;i<data.length;i++){
                let card = data[i];
                let card_element = $(`
                        <div class="col-md-3 mb-3">
                            <div class="card" id="card_${card.id}" data-id="${card.id}"></div>
                        </div>
                    `);
                board_element.append(card_element);
                card_element.on('click',function () {
                    pickCard(card.id, user_id);
                });
            }
        }
    });
}

function fetch_user_info(user_id) {
    $.ajax({
        url: "api/v1/users/"+ user_id,
        type: "GET",
        contentType: "application/json",
        beforeSend : function(xhr) {
            if (localStorage.getItem('token')) {
                xhr.setRequestHeader("Authorization", "JWT " +  localStorage.getItem('token'));
            }
        },
        success: function (data) {
            $('#clickAmountValue').text(data.clicks);
            $('#myBestValue').text(data.my_best);
            if (data.clicks === 0) {
                setTimeout(function () {
                    newGame(user_id);
                }, 800);
            }
        }
    });
}

function fetch_board_info() {
    $.ajax({
        url: "api/v1/board",
        type: "GET",
        contentType: "application/json",
        beforeSend : function(xhr) {
            if (localStorage.getItem('token')) {
                xhr.setRequestHeader("Authorization", "JWT " +  localStorage.getItem('token'));
            }
        },
        success: function (data) {
            $('#globalBestValue').text(data.global_best);
        }
    });
}

function login(username, password) {
    $.ajax({
        url: '/api/v1/auth',
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({'username': username, 'password': password}),
        beforeSend : function(xhr) {
            if (localStorage.getItem('token')) {
                xhr.setRequestHeader("Authorization", "JWT " +  localStorage.getItem('token'));
            }
        },
        success: function (data) {
            localStorage.setItem('token', data.access_token);
        }
    });
}