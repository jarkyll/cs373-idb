
app.controller('MainController', ['$scope', 'service', function($scope, service) {
	service.success(function(data) {
		$scope.data = data;
	});
}]);
/*
app.controller('MainController', ['$scope', function($scope) { 
  $scope.title = 'Top Sellers in Books'; 
}]);
*/