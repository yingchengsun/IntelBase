/****  Variables Initiation  ****/
var doc = document;
var docEl = document.documentElement;
var $sidebar = $('.sidebar');
var $sidebarFooter = $('.sidebar .sidebar-footer');
var $mainContent = $('.main-content');
var $pageContent = $('.page-content');
var $topbar = $('.topbar');
var $logopanel = $('.logopanel');
var $sidebarWidth = $(".sidebar").width();
var content = document.querySelector('.page-content');
$loader = $('#preloader');
var docHeight = $(document).height();
var windowHeight = $(window).height();
var windowWidth = $(window).width();

$(window).load(function() {
  "use strict";
  setTimeout(function () {
      $('.loader-overlay').addClass('loaded');
      $('body > section').animate({
        opacity: 1,
      }, 400);
  }, 500);

});

/* ==========================================================*/
/* APPLICATION SCRIPTS                                       */
/* ========================================================= */

/****  Custom Scrollbar  ****/
function customScroll() {
  if($.fn.mCustomScrollbar) {
    $('.withScroll').each(function () {
        $(this).mCustomScrollbar("destroy");
        var scroll_height = $(this).data('height') ? $(this).data('height') : 'auto';
        var data_padding = $(this).data('padding') ? $(this).data('padding') : 0;
        if ($(this).data('height') == 'window'){
          thisHeight = $(this).height();
          windowHeight = $(window).height() - data_padding - 50;
          if(thisHeight < windowHeight)
            scroll_height = thisHeight;
          else
            scroll_height = windowHeight;  

        }
        $(this).mCustomScrollbar({
            scrollButtons: {
                enable: false
            },
            autoHideScrollbar: $(this).hasClass('show-scroll') ? false : true,
            scrollInertia: 150,
            theme: "light",
            set_height: scroll_height,
            advanced: {
                updateOnContentResize: true
            }
            
        });
    });
  }
}

/* ==========================================================*/
/* BEGIN SIDEBAR                                             */
function createSideScroll() {
  if($.fn.mCustomScrollbar) {
    destroySideScroll();
    if(!$('body').hasClass('sidebar-collapsed') && !$('body').hasClass('sidebar-collapsed') && !$('body').hasClass('submenu-hover') && $('body').hasClass('fixed-sidebar')){
      $('.sidebar-inner').mCustomScrollbar({
          scrollButtons: {
              enable: false
          },
          autoHideScrollbar: true,
          scrollInertia: 150,
          theme: "light-thin",
          advanced: {
              updateOnContentResize: true
          }
      });
    }
    if($('body').hasClass('sidebar-top')){
      destroySideScroll();
    }
  }
}

function destroySideScroll() {
   $('.sidebar-inner').mCustomScrollbar("destroy");
}

/* Toggle submenu open */
function toggleSidebarMenu() {
    // Check if sidebar is collapsed
    if($('body').hasClass('sidebar-collapsed'))
      $('.nav-sidebar .children').css({display: ''});
    else
      $('.nav-active.active .children').css('display', 'block');
    $('.nav-sidebar').on('click', 'li.nav-parent > a', function (e) {
        e.preventDefault();
        if($('body').hasClass('sidebar-collapsed') && !$('body').hasClass('sidebar-hover')) return;
        if($('body').hasClass('submenu-hover')) return;
        var parent = $(this).parent().parent();
        parent.children('li.active').children('.children').slideUp(200);
        $('.nav-sidebar .arrow').removeClass('active');
        parent.children('li.active').removeClass('active');

        var sub = $(this).next();
        // var slideOffeset = -200;
        var slideSpeed = 200;

        if (sub.is(":visible")) {
            $(this).parent().removeClass("active");
            sub.slideUp(slideSpeed, function () {
                if ($('body').hasClass('page-sidebar-fixed') == false && $('body').hasClass('page-sidebar-closed') == false) {
                    // App.scrollTo(the, slideOffeset);
                }                       
                // handleSidebarAndContentHeight();
            });
        } else {
            $(this).find('.arrow').addClass('active');
            sub.slideDown(slideSpeed, function () {
              $(this).parent().addClass("active");
                if ($('body').hasClass('page-sidebar-fixed') == false && $('body').hasClass('page-sidebar-closed') == false) {
                    //App.scrollTo(the, slideOffeset);
                }
                //handleSidebarAndContentHeight();
            });
        }
        createSideScroll();
    });
}

// Add class everytime a mouse pointer hover over it
var hoverTimeout;
 $('.nav-sidebar > li').hover(function() {
    clearTimeout(hoverTimeout);
    $(this).siblings().removeClass('nav-hover');
    $(this).addClass('nav-hover');
}, function() {
    var $self = $(this);
    hoverTimeout = setTimeout(function() {
        $self.removeClass('nav-hover');
    }, 200);
});

 $('.nav-sidebar > li .children').hover(function() {
    clearTimeout(hoverTimeout);
    $(this).closest('.nav-parent').siblings().removeClass('nav-hover');
    $(this).closest('.nav-parent').addClass('nav-hover');
}, function() {
    var $self = $(this);
    hoverTimeout = setTimeout(function() {
        $(this).closest('.nav-parent').removeClass('nav-hover');
    }, 200);
});

 
 // Menu Toggle
function toggleSidebar(){
    $('.topbar').on('click', '.menutoggle', function(){
      var body = $('body');
      var bodypos = body.css('position');
      if(bodypos != 'relative') {
         if(!body.hasClass('sidebar-collapsed')) {
            body.addClass('sidebar-collapsed');
            $('.nav-sidebar ul').attr('style','');
            $(this).addClass('menu-collapsed');
            destroySideScroll();
         } else {
            body.removeClass('sidebar-collapsed');
            $('.nav-sidebar li.active ul').css({display: 'block'});
            $(this).removeClass('menu-collapsed');
            createSideScroll();
         }
      } else {
         if(body.hasClass('sidebar-show'))
            body.removeClass('sidebar-show');
         else
            body.addClass('sidebar-show');     
      }
   });

    var body = $('body');
    var bodypos = body.css('position');
    windowWidth = $(window).width();
    if(windowWidth < 1024) {
        body.addClass('sidebar-collapsed');
        $('.nav-sidebar ul').attr('style','');
        $(this).addClass('menu-collapsed');
        destroySideScroll();
    }
    else{
        body.removeClass('sidebar-collapsed');
        $('.nav-sidebar li.active ul').css({display: 'block'});
        $(this).removeClass('menu-collapsed');
        createSideScroll();
    }





}

/* END SIDEBAR                                               */
/* ========================================================= */

// Check if sidebar is collapsed
if($('body').hasClass('sidebar-collapsed'))
  $('.nav-sidebar .children').css({display: ''});
  
/***** Scroll to top button *****/
function scrollTop(){
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });
    $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 1000);
        return false;
    });
}

/****  Initiation of Main Functions  ****/
$(document).ready(function () {
    createSideScroll();
    toggleSidebarMenu();
    toggleSidebar();
    customScroll();
    scrollTop();
});


$( window ).resize(function() {
  setTimeout(function () {
    customScroll();
    toggleSidebar();


  }, 100);

});