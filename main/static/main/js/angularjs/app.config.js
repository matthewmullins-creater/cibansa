var app = angular.module("cibansa")
app.run( function run($http){
 });
app.config(function($interpolateProvider,$httpProvider,$locationProvider,$provide) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';/// we set this option to enable request.is_ajax()
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
        $locationProvider.html5Mode({
          enabled: true,
          requireBase: false
        });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/json';


});

