angular.module('newApp')
  .controller('tabsCtrl', ['$scope', 'pluginsService', function ($scope, pluginsService) {
      
      $scope.$on('$viewContentLoaded', function () {
          setTimeout(function(){
              inputSelect();
              handleiCheck();
              timepicker();
              datepicker();
              bDatepicker();
              multiDatesPicker();
          },200);
      });

      $scope.isTabActive = true;    

  }]);
