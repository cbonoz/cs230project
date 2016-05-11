'use strict';

describe('Service: jsonGetter', function () {

  // load the service's module
  beforeEach(module('websiteApp'));

  // instantiate service
  var jsonGetter;
  beforeEach(inject(function (_jsonGetter_) {
    jsonGetter = _jsonGetter_;
  }));

  it('should do something', function () {
    expect(!!jsonGetter).toBe(true);
  });

});
