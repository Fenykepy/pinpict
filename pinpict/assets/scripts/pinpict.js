$(document).ready(function () {
    $('article.pin.find').each(function() {
        // store parent article
        var article = $(this)
        // find img child
        var img = $(this).find('img')
        // create new image object
        var pict = new Image();
        // get image src
        pict.src = img.attr('src')
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
