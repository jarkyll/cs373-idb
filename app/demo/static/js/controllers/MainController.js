app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('MainController', ['$scope', 'tests', 'characters', function($scope, tests, characters) { 
	$scope.runTests = function() {
		console.log("Pressed run tests button");
    };
    tests.success(function(data) { 
    	$scope.tests = data; 
    	console.log(JSON.stringify(data));
  });
    characters.success(function(data) { 
    	$scope.characters = data['result']; 
    	console.log(JSON.stringify(data));
  });
}]);