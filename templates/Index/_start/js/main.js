$('[data-plugin-rotate-tect], .rotate-text').each(function() {
    var $this = $(this), opts = null,
    pluginOptions = $this.data('plugin-options'),
    defaults = {
        "animation": "dissolve",  // Options are dissolve (default), fade, flip, flipUp, flipCube, flipCubeUp and spin.
        "separator": ",",  // If you don't want commas to be the separator, you can define a new separator (|, &, * etc.) by yourself using this field.
        "speed": 2500  // How many milliseconds until the next word show.
    };
    opts = $.extend( {}, defaults, pluginOptions );
    $this.textrotator(opts); 
});



(function($) { 
    

  $(function() {

    $('#show-rtl').click(function(e){
      e.preventDefault();
      $('.flip-container.l1').addClass('hover');
      setTimeout(function() { $('.flip-container.l2').addClass('hover'); }, 50);
      setTimeout(function() { $('.flip-container.l3').addClass('hover'); }, 100);
      setTimeout(function() { $('.flip-container.l4').addClass('hover'); }, 150);
      $('#show-rtl').fadeOut(300, function(){
        $('#hide-rtl').fadeIn().css('display', 'block');
      });
      $('body').animate({
        backgroundColor: "#E8E0DD"
      });
      
    });

    $('#hide-rtl').click(function(e){
      e.preventDefault();
      $('.flip-container.l1').removeClass('hover');
      setTimeout(function() { $('.flip-container.l2').removeClass('hover'); }, 50);
      setTimeout(function() { $('.flip-container.l3').removeClass('hover'); }, 100);
      setTimeout(function() { $('.flip-container.l4').removeClass('hover'); }, 150);
      $('#hide-rtl').fadeOut(300, function(){
        $('#show-rtl').fadeIn();
      });
      $('body').animate({
        backgroundColor: "#DDE5E8"
      });
    });

  });


})(jQuery);