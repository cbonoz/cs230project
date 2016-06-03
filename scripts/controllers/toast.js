'use strict';

/**
 * @ngdoc function
 * @name websiteApp.controller:ToastCtrl
 * @description
 * # ToastCtrl
 * Controller of the websiteApp
 */
angular.module('websiteApp')
  .controller('ToastCtrl',  function($scope, $mdToast) {
  $scope.closeToast = function() {
    $mdToast.hide();
  };
});
