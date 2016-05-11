'use strict';

/**
 * @ngdoc directive
 * @name websiteApp.directive:sideBar
 * @description
 * # sideBar
 */
angular.module('websiteApp')
  .directive('sideBar', function () {
    return {
      template: '<div></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the sideBar directive');
      }
    };
  });
