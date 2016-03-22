AngularJS 的 [$http](https://docs.angularjs.org/api/ng/service/$http) 是一个异步调用

为了实现同步调用，例如 jQuery 中的 ajax 同步调用:
```js
var data = {};
var click = function(uri, data){
    $.ajax({
        type:"POST",
        url: uri,
        contentType:"application/json",
        data: JSON.stringify(data),
        dataType:"json",  //返回数据类型
        async: false,
        complete: function(resp){
            console.log(resp);
    });
};
```

AngularJS 提供了 service [$q](https://docs.angularjs.org/api/ng/service/$q) 可以模拟同步请求(实质上还是XHR异步请求); 以下代码实现的功能和
```js
var app = angular.module('myApp', []);
app.controller('appCtrl', ['$scope', 'postJson', function($scope, postJson){
    $scope.click = function(uri, data){
        postJson.postData(uri, data).then(
            function(resp){
                // success
            }, function(err){
                // error
            }
        ).finally(function(){
            // finally
        });
    };
}]);

app.service('postJson', ['$http', '$q', function($http, $q) {
    this.postData = function(url, data){
        var deferred = $q.defer();
        $http({
            method:"POST",
            url: url,
            data: JSON.stringify(data) 
        }).then(
            function (resp) {
                console.log('Success.\n'+resp.data);
                deferred.resolve(resp.data);
            }, function(err) {
                console.log('Error:'+err);
                deferred.reject(err.data);
            }
        );
        return deferred.promise;
    };
}]); 
```