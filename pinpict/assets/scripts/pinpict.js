$(document).ready(function () {
    
    // cookie setup
    // Function to get cookie from django doc
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // for csrf_token from django doc
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    // to conform ajax request to http standart (and avoid hacks for php)
    $.ajaxSettings.traditional = true;


    // pins rating
    var rate_pins = function() {
        $('ul.rate').on('click', 'a.star, a.point', function(e) {
            var link = $(this).attr('href');
            $(this).parent().closest('ul.rate').load(link);
            e.preventDefault();
        });
    };

    function isInArray(value, array) {
        return array.indexOf(value) > -1;
    };
    
    // users following
    $("body").on("click", "a.follow-user", function(e) {
        var link = $(this);
        var button = $(this).children("button");
        console.log(button.html());
        $.ajax(link.attr("href"))
            .done(function(data) {
                console.log(data);
                link.attr("href", data);
                if (button.html() == "Follow") {
                    button.html("Unfollow");
                    link.attr("title", "Unfollow this user");
                } else {
                    button.html("Follow");
                    link.attr("title", "Follow this user");
                }

        }).fail(function() {
            alert("An error occured");
        });
        e.preventDefault();
    });
    
    // pins likes
    $("body").on("click", "a.like-pin", function(e) {
        var link = $(this);
        var button = $(this).children("button");
        console.log(button.html());
        $.ajax(link.attr("href"))
            .done(function(data) {
                console.log(data);
                link.attr("href", data);
                if (button.html() == "Like") {
                    button.html("Unlike");
                    link.attr("title", "Unlike this pin");
                } else {
                    button.html("Like");
                    link.attr("title", "Like this pin");
                }

        }).fail(function() {
            alert("An error occured");
        });
        e.preventDefault();
    });


    // boards following
    $("body").on("click", "a.follow-board", function(e) {
        var link = $(this);
        var button = $(this).children("button");
        console.log(button.html());
        $.ajax(link.attr("href"))
            .done(function(data) {
                console.log(data);
                link.attr("href", data);
                if (button.html() == "Follow") {
                    button.html("Unfollow");
                    link.attr("title", "Unfollow this board");
                } else {
                    button.html("Follow");
                    link.attr("title", "Follow this board");
                }

        }).fail(function() {
            alert("An error occured");
        });
        e.preventDefault();
    });


    // board cover selection
    $("article.board").on("click", ".board-change-cover a", function(e) {
        var board = $(this).parents("article"); // cache parent article
        var board_id = board.attr("id"); // get board id
        var cover = board.find("img.board-main-preview"); // get cover 
        var cover_id = cover.attr("data-main-id"); // get cover
        var covers = [];
        if($(this).html() == "Select") {
            // send request ajax to set cover
            $.ajax( "/pin/" + cover_id + "/main/" ).fail(function() {
                alert('Setting cover failed :(');
            });
            // hide arrows
            board.find("div.board-right-arrow, div.board-left-arrow").hide();
            // delete arrows events
            $("article.board").off("click", ".board-right-arrow");
            $("article.board").off("click", ".board-left-arrow");
            
            // change back button name to "Change cover"
            $(this).html("Change cover");
            $(this).attr("title", "Change cover");
        } else {
            // send request ajax to get covers list
            $.getJSON("/board/covers/" + board_id + "/", function(data) {
                covers = data;
            });
            // show arrows
            board.find("div.board-right-arrow, div.board-left-arrow").show();
            // change button name to "Select"
            $(this).html("Select");
            $(this).attr("title", "Select this cover");

            var get_index = function() {
                for (var i=0; i < covers.length; i++) {
                    if (cover_id == covers[i].pk) {
                        return i;
                    }
                }
            };

            var set_cover = function(index) {
                // set new cover_id
                cover_id = covers[index].pk;
                cover.attr("data-main-id", cover_id);
                // load cover preview
                cover.attr("src", covers[index].previews_path);
            };

            $("article.board").on("click", ".board-right-arrow", function(e){
                // get next index
                var next = get_index() + 1;
                if (next >= covers.length) { next = 0; }
                set_cover(next);
                e.preventDefault();
            });

            $("article.board").on("click", ".board-left-arrow", function(e){
                // get prev index
                var prev = get_index() - 1;
                if (prev < 0) { prev = covers.length - 1; }
                set_cover(prev);
                e.preventDefault();
            });
        }
        e.preventDefault();
    });

    // keyboard navigation
    var keyboard_nav = function() {
        var next = [
            39, // right arrow
            32, // space key
        ];
        var prev = [
            37, // left arrow
            8, // backspace
        ];
        var quit = [
            27, // escpace key
            81, // q key
        ];
        var E = 69; // e, open edit form
        var P = 80; // p, open pinit form

        function navigateTo(link) {
            if (link) {
                window.location = link;
            }
        }
        
        $(document).on('keydown', function(event) {
            if (isInArray(event.keyCode, next)) {
                // go to next item
                var link = $('[rel="next"]').attr('href');
                navigateTo(link);
            }
            else if (isInArray(event.keyCode, prev)) {
                // go to prev item
                var link = $('[rel="prev"]').attr('href');
                navigateTo(link);
            }
            else if (isInArray(event.keyCode, quit)) {
                // go to parent page
                var link = $('[rel="bookmark"]').attr('href');
                navigateTo(link);
            }
            else if (event.keyCode == E) {
                // open edition form
                var link = $('[data-navigate="edit"]').attr('href');
                navigateTo(link);
            }
            else if (event.keyCode == P) {
                // open pinit form
                $('[data-navigate="pinit"]').submit()
            }
        });
    };




    // hide article .pin until justification has been computed
    $('article.pin').css('visibility', 'hidden');


    var justify_pins = function() {
        // hide pins and reset css (for window resizing)
        $('article.pin').css('visibility', 'hidden')
            .css('position', 'relative')
            .css('display', 'inline-block')
            .css('left', 'auto')
            .css('top', 'auto');

        // get section#pins width
        var section_width = $('#pins').width();
        // get pins
        var pins = $('article.pin');
        // store pin width including margins (236 + 14)
        var pin_full_width = pins.eq(0).width()
            + parseInt(pins.eq(0).css('margin-right'))
            + parseInt(pins.eq(0).css('margin-left'));
        // compute number of pins colons
        var n_colons = Math.floor(section_width / pin_full_width);
        if (n_colons > pins.length) {
            n_colons = pins.length;
        }
        // store height margin
        var h_margin = parseInt(pins.eq(0).css('margin-top'))
            + parseInt(pins.eq(0).css('margin-bottom'));

        // create one height variable per colons
        var pos_colons = [];
        for (var i = 0; i < n_colons; i++) {
            // get pin top position
            var pos = pins.eq(i).position();
            // store top and left positions per colon
            pos_colons.push({
                height: pos.top,
                left: pos.left
            });
        };

        // for each article.pin
        var index = 0;
        function next () {
            if (index < pins.length ) {
                function justify () {
                    // create image object to check width and height and see if it has correctly loaded :
                    // 403 status code are not in errors handler…
                    pict = new Image();
                    pict.src = img.attr('src');
                    if (pin.attr('id') != 'create-pin' && (pict.width == 0 || pict.height == 0)) {
                        // error (type 403 for exemple)
                        // remove error pin
                        pin.remove();
                        // reload remaining pin elements
                        pins = $('article.pin');
                        // continue loop without incrementing index
                        return next();
                    }

                    pin.css('position', 'absolute').css('left', pos_colons[colon].left)
                        .css('top', pos_colons[colon].height).css('display', 'block')
                        .css('visibility', 'visible');
                    // store new colon height
                    pos_colons[colon].height = pos_colons[colon].height + pin.height() + h_margin;
                    // increment index and continue loop
                    index++;
                    return next();
                }
                // compute colon number
                var colon = index % n_colons;
                var pin = pins.eq(index);
                // get first img of pin
                var img = pin.find('img').eq(0);
                // if pin has no img (#create-pin)
                if (img.length <= 0) {
                    return justify();
                }

                
                function justify_errors () {
                    // remove error pin
                    pin.remove();
                    // reload remaining pin elements
                    pins = $('article.pin');
                    // continue loop without incrementing index
                    return next();
                }
                // on img load
                img.one('load', justify);
                // on img error
                img.on('error', justify_errors);
                // if img is already loaded, trigger load event
                if (img[0].complete) {
                    //console.log('trigger');
                    img.trigger('load');
                }
            }
            else {
                // justification is done, give new height for section
                // get max colon height
                var height = Math.max.apply(Math, pos_colons.map(function(i){return i.height;}));
                $('#pins').height(height);
            }
        };
        next();
    }
    
    // justify pins
    justify_pins();
    $(window).resize(justify_pins);
    // enable rating
    rate_pins();
    // enable keyboard navigation
    keyboard_nav();

    // get found images width and height, show it.
    $('article.pin.find').each(function() {
        // store parent article
        var article = $(this);
        // find img child
        var img = $(this).find('img');
        // create new image object
        var pict = new Image();
        // get image src
        pict.src = img.attr('src');
        // on img load
        img.one('load', function() {
            // append width and height to footer
            article.find('span.width').append(pict.width);
            article.find('span.height').append(pict.height);
        });
        // if pict is already loaded, trigger load event
        if (pict.complete) {
            img.trigger('load');
        }
    });
});
