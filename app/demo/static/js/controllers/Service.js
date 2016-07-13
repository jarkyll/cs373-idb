app.factory('tests', ['$http', function($http) { 
  return $http.get('http://localhost:5000/runtests') 
            .success(function(data) { 
            	console.log('success')
            	console.log(data);
              return data; 
            }) 
            .error(function(err) { 
            	console.log('error')
              return err; 
            }); 
}]);

app.factory('characters', ['$http', function($http) { 
  return $http.get('http://localhost:5000/api/characters') 
            .success(function(data) { 
              console.log('success')
              console.log(data);
              return data; 
            }) 
            .error(function(err) { 
              console.log('error')
              return err; 
            }); 
}]);
