(function(){
    var app=angular.module("cibansa")

    app.factory("ArticleService",function($q,$http){

        function ArticleService(){

            this.getArticle= function(question){
                var deferred = $q.defer()
                $http.get(Django.url("article-api:article-detail",[question]))
                .then(function(data){
                    deferred.resolve(data)
                },
                 function(data){
                    deferred.reject("Unable to load article")
                 })
                 return deferred.promise
            }
        }
        return ArticleService
    })
})()