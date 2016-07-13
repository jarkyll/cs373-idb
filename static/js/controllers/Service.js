app.factory('tests', ['$http', function($http) { 
  return $http.get('http://localhost:5000/runtests') 
            .success(function(data) { 
              return data; 
            }) 
            .error(function(err) { 
              return err; 
            }); 
}]);
