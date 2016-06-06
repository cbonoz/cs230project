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
  .controller('MainCtrl', function ($scope, fileSystem, jsonGetter, _, $log, $mdToast) {
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

    $scope.removeTab = function (tab) {
      var index = tabs.indexOf(tab);
      tabs.splice(index, 1);
    };


    $scope.projectFile = "Account_.json";
    var n = 0;

    $scope.loadText = () => {
        n+=1
        let fname = "tree" + n + ".json"
        let data = JSON.parse($scope.jsonText)
        console.log("loadText: " + data)
        tabs.push({ title: fname, content: data, disabled: false});
        $scope.badData = false;
        $scope.treeData = data;

        $scope.showSimpleToast("JSON Successfully loaded");
    }

    $scope.loadJson = () => {
        var treeFile = "./trees/" + $scope.projectFile;
        console.log("loading: " + treeFile);
        //use a factory to fetch the data
        jsonGetter.fetch(treeFile).then(function(data) {
            let fname = treeFile.split('/').pop();
            console.log("fname success: " + fname + ", \ndata.length " + data.length);

            tabs.push({ title: fname, content: data, disabled: false});
            $scope.badData = false;
            $scope.treeData = data;

            $scope.showSimpleToast(treeFile + ' Successfully Loaded');

        }, function(error) {
            console.log("error: " + JSON.stringify(error));
            $scope.badData = true;
        });
    }

    //***
    //controller logic for rendering toast below
    //***

    //screen location for the toast
    var last = {
      bottom: false,
      top: true,
      left: true,
      right: false
    };

    $scope.toastPosition = angular.extend({},last);

    $scope.getToastPosition = function() {
      sanitizePosition();

      return Object.keys($scope.toastPosition)
        .filter(function(pos) { return $scope.toastPosition[pos]; })
        .join(' ');
    };

    function sanitizePosition() {
      var current = $scope.toastPosition;

      if ( current.bottom && last.top ) current.top = false;
      if ( current.top && last.bottom ) current.bottom = false;
      if ( current.right && last.left ) current.left = false;
      if ( current.left && last.right ) current.right = false;

      last = angular.extend({},current);
    }

    $scope.showSimpleToast = function(msg) {
      console.log("showSimpleToast")
      var pinTo = $scope.getToastPosition();

      $mdToast.show(
        $mdToast.simple()
          .textContent(msg)
          .position(pinTo )
          .hideDelay(3000)
      );
    };

    $scope.showActionToast = function() {
      console.log("showActionToast")
      var pinTo = $scope.getToastPosition();
      var toast = $mdToast.simple()
        .textContent('Marked as read')
        .action('UNDO')
        .highlightAction(true)
        .highlightClass('md-accent')// Accent is used by default, this just demonstrates the usage.
        .position(pinTo);

      $mdToast.show(toast).then(function(response) {
        if ( response == 'ok' ) {
          alert('You clicked the \'UNDO\' action.');
        }
      });
    };

  });
