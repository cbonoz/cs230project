'use strict';

/**
 * @ngdoc service
 * @name websiteApp.angularFsReader
 * @description
 * # angularFsReader
 * Service in the websiteApp.
 */
angular.module('websiteApp')
  .service('angularFsReader', ['$q', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function
        var thisService = this;

        //Both 'liveArray' and getFiles have the service 'angularFsReader' as their context.
        //Hence they can be directly accessed wherever 'angularFsReader' is injected.
        thisService.liveArray = [];

        thisService.getFiles = function(nativeURL, validExtensions, skippable_folders, specific_folders, qualifiedFileHandler, reportError) {
            var deferred = $q.defer();

            var skippables = angular.isArray(skippable_folders);
            var specifics = angular.isArray(specific_folders);

            //A helper function of pullDataFromEntry
            var processThisFile = function (entry) {
                //1. Matches the file extension with those passed by the user via 'validExtensions'.
                //2. Returns the fileEntry if there's a match, else returns '[null]'.
                
                var deferred = $q.defer();

                var extRegExp = /(?:\.([^.]+))?$/;

                if (validExtensions.length > 0) {

                    var currentExtension = extRegExp.exec(entry.name)[1];

                    if (typeof(currentExtension) !== 'undefined') {
                        if(validExtensions.indexOf(currentExtension.toLowerCase()) != -1){
                            thisService.liveArray.push(entry);
                            deferred.resolve(entry);
                        }
                        else{
                            deferred.resolve(null);
                        }
                    }
                    else {
                        deferred.resolve(null);
                    }
                }
                else{
                    deferred.resolve(null);
                }

                return deferred.promise;
            };

            //A helper function of pullDataFromEntry
            var processThisDirectory = function (entry) {
                //1. Matches the entry.fullPath property of the directory path with those passed by the user via 'skippable_folders' and 'specific_folder'.
                //2. If entry.fullPath correlates with entries in 'skippable_folders', then the directory is skipped, and [null] is returned'
                //3. If entry.fullPath DOES NOT correlates with entries in 'specific_folders', then the directory is skipped, and [null] is returned'.
                //4. If none of the above cases are true, then the entries are read out of the directory, and a recursive call to exploreThisDirectory() is made.
                //5. Note: The array 'specific_folders' has higher priority than 'skippable_folders', and will override conflicting entries.

                var deferred = $q.defer();
                var fullPath = entry.fullPath;
                fullPath = fullPath.indexOf("/") == 0 ? fullPath.substring(1) : fullPath;

                var ifDirectorySkippable = function(fullPath){
                    if (skippables == true){
                        var location = skippable_folders.indexOf(fullPath);
                        if (location > -1) {
                            return true;
                        }
                        else{
                            return false;
                        }

                    }
                    else {
                        return false;
                    }
                };

                var ifDirectoryInSpecific = function(fullPath){
                    if (specifics === true){
                        for (var i = 0; i < specific_folders.length; i++) {

                            var oneValidPath = specific_folders[i];
                            oneValidPath = oneValidPath.indexOf("/") == 0 ? oneValidPath.substring(1) : oneValidPath;

                            if (fullPath.length >= oneValidPath.length) {
                                var location = fullPath.indexOf(oneValidPath);
                            }
                            else {
                                var location = oneValidPath.indexOf(fullPath);
                            }


                            if (location == 0) {
                                return true;
                            }

                        }
                        return false;
                    }
                    else {
                        return true;
                    }


                };


                if (ifDirectorySkippable(fullPath) == false){

                    if (ifDirectoryInSpecific(fullPath) == true){

                        var directoryReader = entry.createReader();
                        directoryReader.readEntries(function(directoryEntries) {
                            exploreThisDirectory(directoryEntries).then(function(array) {
                                deferred.resolve(array);
                            });
                        });

                    }
                    else{
                        deferred.resolve([null])
                    }
                }
                else{
                    deferred.resolve([null]);
                }

                return deferred.promise;
            };

            //A helper function of exploreThisDirectory
            var pullDataFromEntry = function (entry) {
                //1. The primary purpose of separation of the logic inside this function is to provide the promise interface to the caller function as soon as an entry i.e file/directory is found.
                //2. Depending on the type of entry (file or directory), the relevant promise-enabled function is called.

                var deferred = $q.defer();
                if (entry.isFile === true) {
                    processThisFile(entry).then(function (value) {
                        deferred.resolve([value]);
                    });
                }
                if (entry.isDirectory === true) {
                    processThisDirectory(entry).then(function (array) {
                        deferred.resolve(array);
                    });
                }
                return deferred.promise;
            };

            //The primary recursive function.
            var exploreThisDirectory = function (entries) {
                //1. When supplied with a filesystem entry or array of entries, this function will recursively find and return all the qualifying file objects.
                //2. For this it uses the three helper functions defined above.

                var deferred = $q.defer();
                if (angular.isArray(entries) !== true) {
                    entries = [entries];
                }


                var arr = [];
                for (var i = 0; i < entries.length; i++) {
                    arr.push(pullDataFromEntry(entries[i]));
                }

                $q.all(arr).then(function (results) {
                    var accumulate = [];
                    for (var i = 0; i < results.length; i++) {
                        accumulate = accumulate.concat(results[i]);
                    }
                    deferred.resolve(accumulate);
                });

                return deferred.promise;

            };

            //The callback that will be passed to the windows.resolveLocalFileSystemURL method.
            var exploreFileSystem = function (entries) {

                exploreThisDirectory(entries).then(function (rawPromiseArray) {

                    return $q.all(rawPromiseArray);

                }).then(function (these) {
                    var finalReturnable = [];
                    for (var i = 0; i < these.length; i++) {
                        var value = these[i];
                        if (value !== null) {
                            finalReturnable.push(value);
                        }
                    }
                    if (typeof(qualifiedFileHandler) == typeof (Function)) {
                        qualifiedFileHandler(finalReturnable);
                    }
                    deferred.resolve(finalReturnable);
                });

            };

            window.resolveLocalFileSystemURL(nativeURL, exploreFileSystem, reportError);
            return deferred.promise;
        }
  }]);
