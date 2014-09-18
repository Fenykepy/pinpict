$(document).ready(function () {
    // hide article .pin until justification has been computed
    $('article.pin').css('visibility', 'hidden');


    justify_pins = function () {
        // hide pins and reset css (for window resizing)
        $('article.pin').css('visibility', 'hidden')
            .css('position', 'relative')
            .css('display', 'inline-block')
            .css('left', 'auto')
            .css('top', 'auto');

        // get section#pins width
        var section_width = $('#pins').width();
        // store pin width including margins (236 + 14)
        var pin_full_width = 250;
        // compute number of pins colons
        var n_colons = Math.floor(section_width / pin_full_width);
        // store height margin
        var h_margin = 14;
        // get pins
        var pins = $('article.pin');

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
        }

        // for each article.pin
        var index = 0;
        function next () {
            if (index < pins.length ) {
                // compute colon number
                var colon = index % n_colons;
                var pin = pins.eq(index);
                // get first img of pin
                var img = pin.find('img').eq(0);
                // if pin has no img (#create-pin)
                if (img.length <= 0) {
                    console.log('no img');
                    return justify();
                }

                function justify () {
                    pin.css('position', 'absolute').css('left', pos_colons[colon].left)
                        .css('top', pos_colons[colon].height).css('display', 'block')
                        .css('visibility', 'visible');
                    // store new colon height
                    pos_colons[colon].height = pos_colons[colon].height + pin.height() + h_margin;
                    // increment index and continue loop
                    index++;
                    return next();
                }
                
                // on img load
                img.one('load', justify);
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
            pict.trigger('load');
        }
    });
});
