// Show the first tab by default
$('.ahome-tabs-stage .tab-content').hide();
$('.ahome-tabs-stage .tab-content:first').show();
$('.ahome-tabs-nav li:first').addClass('ahome-tab-active');

// Change tab class and display content
$('.ahome-tabs-nav a').on('click', function (event) {
    event.preventDefault();
    $('.ahome-tabs-nav li').removeClass('ahome-tab-active');
    $(this).parent().addClass('ahome-tab-active');
    $('.ahome-tabs-stage .tab-content').hide();
    $($(this).attr('href')).show();
});
