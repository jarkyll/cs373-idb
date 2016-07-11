app.factory('service', ['$http', 
	function($http) {
		return $http.get('localhost:5000/api/characters').success(function(data) {
			return data;
		}).error(function(err) {
			return err;
		});
	}]);