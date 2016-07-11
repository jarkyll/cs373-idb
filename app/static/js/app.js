var app = angular.module("myApp", [])    
	// Changing interpolation start/end symbols.
    .config(function($interpolateProvider, $httpProvider){         
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });