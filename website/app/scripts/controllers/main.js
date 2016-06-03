'use strict';

/**
 * @ngdoc function
 * @name websiteApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the websiteApp
 * for each tree that the user encounters, remember it and append it to the list
 */

angular.module('websiteApp')
  .controller('MainCtrl', function ($scope, fileSystem, jsonGetter, _, $log) {
    var tabs = [
          { title: 'Project Tab', content: ""}],
          selected = null,
          previous = null;
    $scope.tabs = tabs;
    $scope.treeData = {}
    $scope.selectedIndex = 0;


    $scope.$watch('selectedIndex', function(current, old){
      previous = selected;
      selected = tabs[current];
      if ( old + 1 && (old != current)) $log.debug('Goodbye ' + previous.title + '!');
      if ( current + 1 )                $log.debug('Hello ' + selected.title + '!');
    });

    $scope.addTab = function (title, view) {
      view = view || title + " Content View";
      tabs.push({ title: title, content: view, disabled: false});
    };

    $scope.removeTab = function (tab) {
      var index = tabs.indexOf(tab);
      tabs.splice(index, 1);
    };

    $scope.clearProjects = () => {
        $scope.tabs = []
        tabs = []
        console.log("clearProjects " + JSON.stringify($scope.tabs))
    }

    $scope.projectFile = "./trees/output_tree.json";

    $scope.loadJson = () => {
        var treeFile = $scope.projectFile;
        console.log("loading: " + treeFile);
        //use a factory to fetch the data
        jsonGetter.fetch(treeFile).then(function(data) {
            let fname = treeFile.split('/').pop();
            console.log("fname success: " + fname + ", " + JSON.stringify(data));

            tabs.push({ title: fname, content: data, disabled: false});
            $scope.badData = false;
            $scope.treeData = data;

        }, function(error) {
            console.log("error: " + JSON.stringify(error));
            $scope.badData = true;
        });
    }

  });
