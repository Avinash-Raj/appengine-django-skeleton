/**
 * Created by Avinash on 30/12/15.
 */

var app = angular.module('todo', []);

app.controller('MainCtrl', function ($scope) {
    $scope.onDragComplete=function(data,evt){
       console.log("drag success, data:", data);
    };
    $scope.onDropComplete=function(data,evt){
        console.log("drop success, data:", data);
    };
 });