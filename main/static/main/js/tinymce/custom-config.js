//$(document).ready(function() {

jquery =""
try{
    jquery=grp.jQuery
}catch(err){
    jquery=jQuery
}

jquery("script[src='/static/django_tinymce/jquery-1.9.1.min.js']").remove()
  tinymce.init({
    selector: "textarea",
    theme: "modern",
    height:250,
    paste_data_images: true,
    plugins: [
      "advlist autolink lists link image charmap print preview hr anchor pagebreak",
      "searchreplace wordcount visualblocks visualchars code fullscreen",
      "insertdatetime media nonbreaking save table contextmenu directionality",
      "emoticons template paste textcolor colorpicker textpattern,code"
    ],
    toolbar1: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
    toolbar2: "preview | forecolor backcolor emoticons | code",
    image_advtab: true,
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
//    images_upload_url: 'imagehandler.php'
//    images_upload_handler:function (blobInfo, success, failure) {
//        var xhr, formData;
//        xhr = new XMLHttpRequest();
//        xhr.withCredentials = false;
//        xhr.open('POST', 'postAcceptor.php');
//        xhr.onload = function() {
//          var json;
//
//          if (xhr.status != 200) {
//            failure('HTTP Error: ' + xhr.status);
//            return;
//          }
//          json = JSON.parse(xhr.responseText);
//
//          if (!json || typeof json.location != 'string') {
//            failure('Invalid JSON: ' + xhr.responseText);
//            return;
//          }
//          success(json.location);
//        };
//        formData = new FormData();
//        formData.append('file', blobInfo.blob(), fileName(blobInfo));
//        xhr.send(formData);
//      }
//    templates: [{
//      title: 'Test template 1',
//      content: 'Test 1'
//    }, {
//      title: 'Test template 2',
//      content: 'Test 2'
//    }]

  });
//});