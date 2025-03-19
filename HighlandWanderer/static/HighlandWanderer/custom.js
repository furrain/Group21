$(document).ready(function(){
    // Back-to-Top button
    var backToTopBtn = $('<button id="backToTop" class="btn btn-secondary" style="position: fixed; bottom: 20px; right: 20px; display: none;">Back to Top</button>');
    $('body').append(backToTopBtn);

    // Show/hide the Back-to-Top button
    $(window).scroll(function(){
        if ($(this).scrollTop() > 200) {
            $('#backToTop').fadeIn();
        } else {
            $('#backToTop').fadeOut();
        }
    });

    // Click the button and scroll smoothly to the top
    $('#backToTop').click(function(){
        $('html, body').animate({ scrollTop: 0 }, 500);
        return false;
    });

    // Toggle Comment Form: Clicking the button shows/hides the comment form.
    // If the button is inside a form, use e.preventDefault() to prevent the default behavior
    $('#toggleCommentBtn').on('click', function(e){
        e.preventDefault();
        $('#commentFormContainer').toggle(300);
    });
});