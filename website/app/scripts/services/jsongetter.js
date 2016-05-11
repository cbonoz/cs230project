'use strict';

/**
 * @ngdoc service
 * @name websiteApp.jsonGetter
 * @description
 * # jsonGetter
 * Factory in the websiteApp.
 */
angular.module('websiteApp')
  .factory('jsonGetter', function($timeout, $http) {
    var Webtest = {
        fetch: function(file_name) {
            console.log("getting " + file_name)
            return $timeout(function() {
                return $http.get(file_name).then(function(response) {
                    return response.data;
                });
            }, 30);
        }
    }

    return Webtest;
});
