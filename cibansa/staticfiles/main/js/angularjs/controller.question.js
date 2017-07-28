(function(){

    var app = angular.module("cibansa")

    app.controller("QuestionController",function(QuestionService,$scope,$http,$sce){
            $scope.tinymceOptions = {
                plugins: "advlist autolink lists link image charmap print preview hr anchor pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking save table contextmenu directionality emoticons template paste textcolor colorpicker textpattern code",
                toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
                file_picker_callback: function(callback, value, meta) {
                  if (meta.filetype == 'image') {
                    var input = document.createElement('input')
                    input.setAttribute('type', 'file');
                    input.setAttribute('accept', 'image/*');

                    $(input).trigger('click');
                    $(input).on('change', function() {
                      var file = this.files[0];
                      var reader = new FileReader();
                      reader.onload = function(e) {
                        callback(e.target.result, {
                          alt: ''
                        });
                      };
                      reader.readAsDataURL(file);
                    });
                  }
                },
              };
            $scope.init = function(question){
                questionService = new QuestionService()
                questionService.getQuestion(question).then(
                    function(response){
                        console.log(response)
                        $scope.qObj = response.data
//                        console.log($scope.qObj.owner.profile_pix )
//                        $scope.qObj.owner.profile_pix  = $sce.trustAsHtml($scope.qObj.owner.profile_pix )
                    },
                    function(response){
                        console.log(response)
                    }
                )

            }

            $scope.trustedHtml = function(html){
                return $sce.trustAsHtml(html)
            }

            $scope.postAnswer = function(question){
                if ($scope.qObj.answerComment){
                    $scope.qObj.answerSubmitted =true
                    $http.post(Django.url("question-api:question-post-answer"),
                            {question:question,user:Django.user.id,comment:$scope.qObj.answerComment})
                    .then(function(response){
                        $scope.qObj.answerSubmitted =false
                        $scope.qObj.question_answers.push(response.data)
                        $scope.qObj.answerComment=""
                    },function(response){
                        $scope.qObj.answerSubmitted =false
                    })
                }

            }

            $scope.showReply = function($index,$event){
                jQuery("#reply"+$index).show()
                jQuery($event.currentTarget).hide()
            }

            $scope.postReply = function(answer,$index){
                console.info(answer.model_name)
                var replyComment = answer.model_name//jQuery("#replyComment"+$index).val()

                if(replyComment){
                    $scope.qObj.replySubmitted =true
                    $http.post(Django.url("question-api:question-post-answer-reply"),
                        {answer:answer.id,user:Django.user.id,comment:replyComment})
                    .then(function(response){
                        $scope.qObj.replySubmitted =false
                        answer.answer_replies.push(response.data)
                        jQuery("#replyComment"+$index).val("")
                        jQuery("#reply"+$index).hide()
                        jQuery("#replyBtn"+$index).show()
                    },function(response){
                        $scope.qObj.replySubmitted =false
                    })
                }

            }

            $scope.likeAnswer = function(answer){

                if(answer.has_liked){
                    $http.post(Django.url("answer-like-api:answer-like-un-like"),
                    {answer:answer.id})
                    .then(function(response){
                           answer.has_liked=false
                           answer.answer_likes=answer.answer_likes-1
                    },function(response){
                         console.log(response)
                    })
                }
                else{
                    $http.post(Django.url("answer-like-api:answer-like-list"),
                    {answer:answer.id,user:Django.user.id})
                    .then(function(response){
                           answer.has_liked=true
                           answer.answer_likes=answer.answer_likes+1
                    },function(response){
                         console.log(response)
                    })
                }

            }
            $scope.likeAnswerReply = function(answerReply){
                console.log(answerReply)
                if(answerReply.has_liked){
                    $http.post(Django.url("answer-reply-like-api:answer-reply-like-un-like"),
                    {answer_reply:answerReply.id})
                    .then(function(response){
                           answerReply.has_liked=false
                           answerReply.answer_reply_likes=answerReply.answer_reply_likes-1
                    },function(response){
                         console.log(response)
                    })
                }
                else{
                    $http.post(Django.url("answer-reply-like-api:answer-reply-like-list"),
                    {answer_reply:answerReply.id,user:Django.user.id})
                    .then(function(response){
                           answerReply.has_liked=true
                           answerReply.answer_reply_likes=answerReply.answer_reply_likes+1
                    },function(response){
                         console.log(response)
                    })
                }

            }
    })
})()