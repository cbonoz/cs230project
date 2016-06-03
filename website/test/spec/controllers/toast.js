'use strict';

describe('Controller: ToastCtrl', function () {

  // load the controller's module
  beforeEach(module('websiteApp'));

  var ToastCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ToastCtrl = $controller('ToastCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(ToastCtrl.awesomeThings.length).toBe(3);
  });
});
