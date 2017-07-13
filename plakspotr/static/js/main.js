var input = document.querySelector('input[type=file]'); // see Example 4

input.onchange = function () {
  var file = input.files[0];

  drawOnCanvas(file);   // see Example 6
  //displayAsImage(file); // see Example 7
  //uploadImgur(file);    // and analyze..
};

function upload(file) {
  var form = new FormData(),
      xhr = new XMLHttpRequest();

  form.append('image', file);
  xhr.open('post', 'upload', true);
  xhr.send(form);
}

function drawOnCanvas(file) {
  var reader = new FileReader();

  reader.onload = function (e) {
    var dataURL = e.target.result,
        c = document.querySelector('canvas'), // see Example 4
        ctx = c.getContext('2d'),
        img = new Image(),
        MAX_WIDTH = 1280,
        MAX_HEIGHT = 1280;

    img.onload = function() {
      var width = img.width,
          height = img.height;
      // scale down
      if (width > height){
        if (width > MAX_WIDTH)
          height *= MAX_WIDTH / width;
          width = MAX_WIDTH;
      } else {
        if (height > MAX_HEIGHT) {
          width *= MAX_HEIGHT / height;
          height = MAX_HEIGHT;
        }
      }
      c.width = width;
      c.height = height;
      ctx.drawImage(img, 0, 0, width, height);
      var smallDataUrl = c.toDataURL("image/jpeg", 0.90);
      uploadImgur(smallDataUrl);
    };

    img.src = dataURL;
  };

  reader.readAsDataURL(file);
}


function uploadImgur(file) {

    /* Is the file an image? */
    if (!file) return
    if (file instanceof File && !file.type.match(/image.*/)) return;
    else {
       file = file.substring(23);
    }
    console.log('file type is '+typeof(file));


    /* It is! */
    document.body.className = "uploading";

    /* Lets build a FormData object*/
    var fd = new FormData();
    fd.append("image", file); // Append the file
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://api.imgur.com/3/image.json"); // Boooom!
    xhr.onload = function() {
    // on success
        var data = JSON.parse(xhr.responseText).data
        var link = data.link;
        console.log('upload successful')
        console.log(data);
        document.querySelector("#imgur-url").href = link;
        document.querySelector("#imgur-url").innerHTML = link;
        document.body.className = "uploaded";
        analyzeImage(link);
    }
    // Ok, I don't handle the errors. An exercice for the reader.
    xhr.setRequestHeader('Authorization', 'Client-ID bae399be44e53ae');
    /* And now, we send the formdata */
    xhr.send(fd);
}


function analyzeImage(url) {
  console.log('start analysis');
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "https://api.openalpr.com/v2/recognize_url");
  xhr.onload = function() {
  // on success
     var data = JSON.parse(xhr.responseText);
     console.log('analysis complete');
     console.log(data);
     if (data.results) {
       var result = data.results[0].plate;
       document.querySelector("#plateNumber").innerHTML = '<h1>' + result +'</h1>';
     }
  }
  var fd = new FormData();
  fd.append('image_url', url);
  fd.append('secret_key', 'sk_d9f61fcd9db91602e13e76ae');
  fd.append('country', 'eu');
  xhr.send(fd);
}

function displayAsImage(file) {
  var imgURL = URL.createObjectURL(file),
      img = document.createElement('img');

  img.onload = function() {
    URL.revokeObjectURL(imgURL);
  };

  img.src = imgURL;
  document.body.appendChild(img);
}
