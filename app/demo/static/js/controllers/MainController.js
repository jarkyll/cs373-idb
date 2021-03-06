app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('MainController', ['$scope', 'characters', 'teams', 'volumes', 'publishers', function($scope, characters, teams, volumes, publishers) { 
	$scope.runTests = function() {
		$.get('http://localhost:5000/runtests', function(data,status) {
        alert(data);
      },'html');
    };
    /*
  tests.success(function(data) { 
    	$scope.tests = data; 
    	console.log(JSON.stringify(data));
  }); */
  characters.success(function(data) { 
    	$scope.characters = data['result']; 
    	//console.log(JSON.stringify(data));
  }); 
  teams.success(function(data) { 
      $scope.teams = data['result']; 
      //console.log(JSON.stringify(data));
  });
  volumes.success(function(data) { 
      $scope.volumes = data['result']; 
      //console.log(JSON.stringify(data));
  });
  publishers.success(function(data) { 
      $scope.publishers = data['result']; 
      //console.log(JSON.stringify(data));
  });
  $scope.formatjson = function(a){

     a = a.map(function(x){
        if (x == null) { return 'No record';}
        return x.replace(/^[a-z]\[\]/,function(m){
            return m.toUpperCase()
        });
     });
    return a.join();
  };
}]);