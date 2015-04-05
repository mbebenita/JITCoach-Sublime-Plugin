if (typeof enableSPSProfiling !== "undefined") {
  enableSPSProfiling();
}

var A = [];

function init() {
  for (var i = 1; i < 10; i++) {
    A.push(new Uint8Array(512 * i));
  }
}

init();

function f(a) {
  var k = a.length;
  for (var i = 0; i < k; i++) {
    a[i] = i;
  }
}

function foo() {
  for (var i = 0; i < 1024 * 64; i++) {
    for (var j = 0; j < A.length; j++) {
      var a = A[j];
      var a = A[j];
      var a = A[j];
      var a = A[j];
      var a = A[j];
      f(a);
    }
  }
}

foo();

if (typeof trackedOpts !== "undefined") {
  var opts = trackedOpts(foo);
  for (var i = 0; i < opts.regions.length; i++) {
    var region = opts.regions[i];
    region.line = pc2line(foo, region.offset);
  }
  print(JSON.stringify(opts, null, 2));
}