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

app.factory('teams', ['$http', function($http) { 
  return $http.get('http://localhost:5000/api/teams') 
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

app.factory('volumes', ['$http', function($http) { 
  return $http.get('http://localhost:5000/api/volumes') 
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

app.factory('publishers', ['$http', function($http) { 
  return $http.get('http://localhost:5000/api/publishers') 
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