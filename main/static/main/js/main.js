$(function() {

	$('#toggle_signUp').bind("click",function(){
		$('#signIn').modal('hide');
		$('#signUp').modal('show');
	});

	$('#toggle_logIn').click(function(){
		$('#signUp').modal('hide');
		$('#signIn').modal('show');
	});

  var width = window.innerWidth;
  if(width < 767){
    $('.view-answer a').removeClass('pull-right');
  }
	
});

window.onload = function(){
    var t = $("#id_topic").val()

    $("#id_category").change(function(){
	$.ajax({
       url:Django.url("topic-by-category")+"?category="+$("#id_category").val(),
       success:function(data){
            $("#id_topic").html("")
            $.each(JSON.parse(data),function(k,j){
                $("#id_topic").append("<option value='"+j.id+"'>"+j.name+"</option>")
            })
            if(t=="" && data == "")
                $("#id_topic").html("<option>Topic</option>")
             else
                $("#id_topic").val(t)
        }
        })
    })

    $( "#id_category" ).trigger("change");

  $(".chip .close").click(function(){
        $(this).parents(".chip").remove()
   })
}


$(document).on("keydown.autocomplete",".tag_field",function(){
        var _this=$(this)
       $(this).autocomplete({
             source: function( request, response ) {
                $.ajax({
                  url: Django.url("tag-auto-complete")+"?q="+request.term,
                  dataType: "json",
//                  data: {
//                    q: request.term
//                      },
                  success: function( data ) {
//                            data=$.parseJSON(data)
                            response($.map(data, function(item) {
                                return {
                                    label: item.label,
                                    id: item.id,
                                    value: item.value,
                                    image: item.image
                                    };
                            }));

                      }
                    });
              },
            select:function(event, ui){

//                $(".company_auto_image").attr("src",ui.item.image)
//                $("#company_id").val(ui.item.id)
                  $(".chip-container").append('<div class="chip"><input type="hidden" name="tag" value="'+ui.item.id+'"/><a href="">'+ui.item.label+'</a><i class="close material-icons">close</i></div>')
                  $(".tag_field").val("")
//                  _this.val("")
//                  console.log($(".tag_field").val(),124,$(this))
            },
            minLength: 3,
       })
       .autocomplete( "instance" )._renderItem = function( ul, item ) {
          return $( "<li>" )
            .append( "<div>" + item.label+ "</div>" )
            .appendTo( ul );
        };
    })

 $(document).on("keydown.autocomplete",".q-search",function(){

       $(this).autocomplete({
             source: function( request, response ) {
                $.ajax({
                  url: Django.url("question-auto-complete")+"?q="+request.term,
                  dataType: "json",
//                  data: {
//                    q: request.term
//                      },
                  success: function( data ) {
//                            data=$.parseJSON(data)
                            response($.map(data, function(item) {
                                return {
                                    label: item.label,
                                    id: item.id,
                                    value: item.value,
                                    link: item.link
                                    };
                            }));

                      }
                    });
              },
            select:function(event, ui){
                  window.location = ui.item.link
            },
            minLength: 3,
       })
       .autocomplete( "instance" )._renderItem = function( ul, item ) {
          return $( "<li>" )
            .append( "<div>" + item.label+ "</div>" )
            .appendTo( ul );
        };
    })
 $("#input_img").click(function(){
    $("#search-form").submit()
 })


