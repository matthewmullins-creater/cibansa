(function(){

    var app = angular.module("cibansa")

    app.controller("ArticleController",function(ArticleService,$scope,$http,$sce){
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
            $scope.init = function(a){
                articleService = new ArticleService()

                articleService.getArticle(a).then(
                    function(response){
                        console.log(response)
                        $scope.aObj = response.data
                    },
                    function(response){
                        console.log(response)
                    }
                )

            }

            $scope.trustedHtml = function(html){
                return $sce.trustAsHtml(html)
            }

            $scope.postComment = function(){
                if($scope.comment){
                    $scope.aObj.commentSubmitted =true
                    $http.post(Django.url("article-api:article-post-comment"),
                            {article:$scope.aObj.id,user:Django.user.id,comment:$scope.comment})
                    .then(function(response){
                        $scope.aObj.commentSubmitted =false
                        $scope.aObj.article_comments.push(response.data)
                        $scope.comment=""
                    },function(response){
                        $scope.aObj.commentSubmitted =false
                    })
                }

            }
//
            $scope.showReply = function($index,$event){
                jQuery("#reply"+$index).show()
                jQuery($event.currentTarget).hide()
            }
//
            $scope.postReply = function(ac,$index){
                $scope.aObj.replySubmitted =true
                var replyComment = ac.replyComment
                if(replyComment){
                     $http.post(Django.url("article-api:article-post-comment-reply"),
                        {comment:ac.id,user:Django.user.id,content:replyComment})
                    .then(function(response){
                        $scope.aObj.replySubmitted =false
                        ac.comment_replies.push(response.data)
                        jQuery("#replyComment"+$index).val("")
                        jQuery("#reply"+$index).hide()
                        jQuery("#replyBtn"+$index).show()
                    },function(response){
                        $scope.aObj.replySubmitted =false
                    })
                }

            }

//            $scope.likeAnswer = function(answer){
//
//                if(answer.has_liked){
//                    $http.post(Django.url("answer-like-api:answer-like-un-like"),
//                    {answer:answer.id})
//                    .then(function(response){
//                           answer.has_liked=false
//                           answer.answer_likes=answer.answer_likes-1
//                    },function(response){
//                         console.log(response)
//                    })
//                }
//                else{
//                    $http.post(Django.url("answer-like-api:answer-like-list"),
//                    {answer:answer.id,user:Django.user.id})
//                    .then(function(response){
//                           answer.has_liked=true
//                           answer.answer_likes=answer.answer_likes+1
//                    },function(response){
//                         console.log(response)
//                    })
//                }
//
//            }
            $scope.likeArticle = function(){
                if($scope.aObj.has_liked){
                    $http.post(Django.url("article-likes-api:a-likes-un-like"),
                    {article:$scope.aObj.id})
                    .then(function(response){
                           $scope.aObj.has_liked=false
                           $scope.aObj.article_likes=$scope.aObj.article_likes-1
                    },function(response){
                         console.log(response)
                    })
                }
                else{
                    $http.post(Django.url("article-likes-api:a-likes-list"),
                    {article:$scope.aObj.id,user:Django.user.id})
                    .then(function(response){
                           $scope.aObj.has_liked=true
                           $scope.aObj.article_likes=$scope.aObj.article_likes+1
                    },function(response){
                         console.log(response)
                    })
                }

            }

            $scope.likeArticleComment = function(ac){
                if(ac.has_liked){
                    $http.post(Django.url("article-cl-api:ac-likes-un-like"),
                    {comment:ac.id})
                    .then(function(response){
                           ac.has_liked=false
                           ac.comment_likes=ac.comment_likes-1
                    },function(response){
                         console.log(response)
                    })
                }
                else{
                    $http.post(Django.url("article-cl-api:ac-likes-list"),
                    {comment:ac.id,user:Django.user.id})
                    .then(function(response){
                           ac.has_liked=true
                           ac.comment_likes=ac.comment_likes+1
                    },function(response){
                         console.log(response)
                    })
                }

            }

            $scope.likeCommentReply = function(rep){
                if(rep.has_liked){
                    $http.post(Django.url("article-crl-api:a-com-rep-likes-un-like"),
                    {comment_reply:rep.id})
                    .then(function(response){
                           rep.has_liked=false
                           rep.comment_reply_likes=rep.comment_reply_likes-1
                    },function(response){
                         console.log(response)
                    })
                }
                else{
                    $http.post(Django.url("article-crl-api:a-com-rep-likes-list"),
                    {comment_reply:rep.id,user:Django.user.id})
                    .then(function(response){
                           rep.has_liked=true
                           rep.comment_reply_likes=rep.comment_reply_likes+1
                    },function(response){
                         console.log(response)
                    })
                }

            }
    })
})()