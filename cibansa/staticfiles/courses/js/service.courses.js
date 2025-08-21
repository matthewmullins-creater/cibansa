(function(){
    var app=angular.module("cibansa")

    app.factory("CoursesService",function($q,$http){

        function CoursesService(){

            this.getCourses= function(question){
                var deferred = $q.defer()
                $http.get(Django.url("courses-api:courses-detail",[question]))
                .then(function(data){
                    deferred.resolve(data)
                },
                 function(data){
                    deferred.reject("Unable to load courses")
                 })
                 return deferred.promise
            }
        }
        return CoursesService
    })
})()