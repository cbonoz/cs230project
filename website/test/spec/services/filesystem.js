'use strict';

describe('Service: fileSystem', function () {

  // load the service's module
  beforeEach(module('websiteApp'));

  // instantiate service
  var fileSystem;
  beforeEach(inject(function (_fileSystem_) {
    fileSystem = _fileSystem_;
  }));

  it('should do something', function () {
    expect(!!fileSystem).toBe(true);
  });

});
