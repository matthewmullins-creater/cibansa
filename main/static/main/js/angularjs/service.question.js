(function(){
    var app=angular.module("cibansa")

    app.factory("QuestionService",function($q,$http){

        function QuestionService(){

            this.getQuestion = function(question){
                var deferred = $q.defer()
                $http.get(Django.url("question-api:question-detail",[question]))
                .then(function(data){
                    deferred.resolve(data)

                },
                 function(data){
                    deferred.reject("Unable to get question")
                 })

                 return deferred.promise
            }

        }
        return QuestionService
    })
})()