'use strict';

/**
 * @ngdoc function
 * @name websiteApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the websiteApp
 */

angular.module('websiteApp')
  .controller('MainCtrl', function ($scope, fileSystem, jsonGetter, _) {

    $scope.folder = "./trees/"
    // $scope.folder = "../../../../visualize/trees/"
    // $scope.folder = "~/app/trees/"


    $scope.loadJson = (tree_file) => {
        $scope.selected_file = tree_file;
        console.log("loading " + tree_file)
        jsonGetter.fetch(tree_file).then(function(data) {
            console.log(JSON.stringify(data))
            $scope.tree_data = data;
            $scope.bad_data=false;
        }, function(error) {
            console.log("error")
            $scope.tree_data = {}
            $scope.bad_data = true;
        });
    }

    $scope.$watch('folder', function(newValue, oldValue) {
        console.log(newValue);
        $scope.updateFolder();
    });


    $scope.updateFolder = () => {
        // $scope.tabs = fileSystem.getFolderContents($scope.folder);
        let tree_file = $scope.folder + "project_" + ($scope.selected_index+1) + ".json";
        $scope.loadJson(tree_file);
    }

    $scope.tabs = _.map(_.range(1,11), (x) => { return "project_" + x; })
    // $scope.tabs = Directory.GetFiles($scope.folder)
    // $scope.tabs = []

    $scope.tab_content = '<tree-graph class="full-screen" data="tree_data" ng-hide="bad_data"></tree-graph><h4 ng-show="bad_data">No test file <i>{{tab}}.json</i> found</h4>'


    let getFiles = function(dir) {
        $scope.files = []
        fileSystem.getFolderContents(dir).then(function(entries) {
            for(var i = 0; i<entries.length; i++) {
                $scope.files.push(entries[i].fullPath);
            }
            console.log($scope.files)
        }, function(err) {
            console.log(err);
            $window.alert(err.text);
        });
    };

    let getUsageInfo = function() {
        $scope.files = []
        fileSystem.getCurrentUsage().then(function(usage) {
            $scope.files.push(usage.used + " / " + usage.quota);
        }, function(err) {
            console.log(err);
            $window.alert(err.text);
        });
    };



    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $scope.awesomeThings = this.awesomeThings;


     $scope.friends = [
        {name:'John', age:25, gender:'boy'},
        {name:'Jessie', age:30, gender:'girl'},
        {name:'Johanna', age:28, gender:'girl'},
        {name:'Joy', age:15, gender:'girl'},
        {name:'Mary', age:28, gender:'girl'},
        {name:'Peter', age:95, gender:'boy'},
        {name:'Sebastian', age:50, gender:'boy'},
        {name:'Erika', age:27, gender:'girl'},
        {name:'Patrick', age:40, gender:'boy'},
        {name:'Samantha', age:60, gender:'girl'}
      ];

  });
