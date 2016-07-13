app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('MainController', ['$scope', 'tests', function($scope, tests) { 
	$scope.runTests = function() {
		console.log("Pressed run tests button");
    };
    tests.success(function(data) { 
    	$scope.tests = data; 
    	    	console.log(JSON.stringify(data));
  });
}]);