
src="https://sdk.amazonaws.com/js/aws-sdk-2.283.1.min.js"
function validateFileType(input){
          var fileName = document.getElementById("fileName").value;
          var idxDot = fileName.lastIndexOf(".") + 1;
          var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
          if (extFile=="jpg" || extFile=="jpeg" || extFile=="png"){
              readURL(input);
          }else{
              alert("Only images are allowed!");
          }   
}

function readURL(input) {  
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $('.image-upload-wrap').hide();
      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();
      $('.image-title').html(input.files[0].name);
    };
    reader.readAsDataURL(input.files[0]);
    uploadFile(input);
    setTimeout(function(){buscarRespuesta(input)}, 3500);  
} else {
    removeUpload();
  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}
$('.image-upload-wrap').bind('dragover', function () {
                $('.image-upload-wrap').addClass('image-dropping');
        });
	$('.image-upload-wrap').bind('dragleave', function () {
                $('.image-upload-wrap').removeClass('image-dropping');
});

function uploadFile(input){
  var file = input.files[0] //File a subir a S3
  
  //Config credentials
  AWS.config.region = 'us-west-2'; // Region
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-west-2:309212a7-40bc-4dff-83c2-1f509a113fc2',
    });
  
    //Bucket Definition
    var bucketName = 'parcial-cloud-icesi-luisyswan';
    var bucket = new AWS.S3({
        params: {
            Bucket: bucketName
    }
    });
    
    
    //Upload file
    var objKey ="images/" + file.name;
    bucket.upload({
    Key: objKey,
    Body: file,
    ACL: 'public-read'
  }, function(err, data) {
    if (err) {
      return alert('There was an error uploading your photo: ', err.message);
    }
});
}

function buscarRespuesta(input){
    var file = input.files[0]
    var objKey ="answers/images/" + file.name + ".txt";
    AWS.config.region = 'us-west-2'; // Region
    AWS.config.credentials = new 
    AWS.CognitoIdentityCredentials({    
      IdentityPoolId: 'us-west-2:309212a7-40bc-4dff-83c2-1f509a113fc2',
    });  
      //Bucket Definition
    var bucketName = 'parcial-cloud-icesi-luisyswan';
  var bucket = new AWS.S3({
        params: {
            Bucket: bucketName
        }
    });
  bucket.getObject(  
    { Bucket: bucketName, Key: objKey },  
    function (error, data) {    
      if (error != null) {      
        setTimeout(function(){buscarRespuesta(input)}, 3500);
      } else {     
        alert(data.Body.toString('ascii'));     
        // do something with data.Body
      }
  }
);
}


