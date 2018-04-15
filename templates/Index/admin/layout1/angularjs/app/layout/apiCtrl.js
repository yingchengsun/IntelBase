'use strict';

angular.module('newApp')
  .controller('apiCtrl', function ($scope, layoutApiService, applicationService) {
      $scope.$on('$viewContentLoaded', function () {
          
          $('[data-toggle]').on('click', function (event) {
              event.preventDefault();
              var toggleLayout = $(this).data('toggle');
              if (toggleLayout == 'sidebar-behaviour') applicationService.toggleSidebar();
              if (toggleLayout == 'submenu') applicationService.toggleSubmenuHover();
              if (toggleLayout == 'sidebar-hover') applicationService.toggleSidebarHover();
              if (toggleLayout == 'boxed') applicationService.toggleboxedLayout();
              if (toggleLayout == 'topbar') applicationService.toggleTopbar();
              if (toggleLayout == 'sidebar-top') applicationService.toggleSidebarTop();
              if (toggleLayout == 'rtl') applicationService.toggleRTL();
          });

          applicationService.init();
      });
  });