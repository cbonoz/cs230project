'use strict';

describe('Service: angularFsReader', function () {

  // load the service's module
  beforeEach(module('websiteApp'));

  // instantiate service
  var angularFsReader;
  beforeEach(inject(function (_angularFsReader_) {
    angularFsReader = _angularFsReader_;
  }));

  it('should do something', function () {
    expect(!!angularFsReader).toBe(true);
  });

});
