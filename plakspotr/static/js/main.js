var input = document.getElementById('img-input'); // see Example 4

input.onchange = function (e) {
    loadImage(
        e.target.files[0],
        function (canvas) {
            canvas.setAttribute('id', 'img-preview');
            document.getElementById('main-jumbo').appendChild(canvas);
            var btn = document.getElementById('analyze-btn');
            if (btn) {
                btn.removeAttribute('disabled');
            }
        },
        {   // canvas conversion options
            maxWidth: 1200,
            maxHeight: 1200,
            orientation: true,  // use orientation from EXIF data
            canvas: true        // returns a canvas element instead of an img
        }
    );
}

function analyzeImg() {
    var c = document.getElementById('img-preview'),
        data = c.toDataURL("image/jpeg", 0.90),
        b64data = data.split(',')[1];
    uploadImgur(b64data);
}

function upload(file) {
    var form = new FormData(),
        xhr = new XMLHttpRequest();

    form.append('image', file);
    xhr.open('post', 'spot', true);
    xhr.send(form);
}


function uploadImgur(file) {

    /* Is the file an image? */
    if (!file) return;
    if (file instanceof File && !file.type.match(/image.*/)) return;
    console.log('file type is '+typeof(file));
    if (file.startsWith('data:image/png;base64,')) {
       file = file.split(',')[1];
    }

    /* It is! */
    document.body.className = "uploading";

    /* Lets build a FormData object*/
    var fd = new FormData();
    fd.append("image", file); // Append the file
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://api.imgur.com/3/image.json"); // Boooom!
    xhr.onload = function() {
    // on success
        var data = JSON.parse(xhr.responseText).data,
            url = data.link;
        console.log('upload successful')
        console.log(data);
        document.querySelector("#imgur-url").href = url;
        document.querySelector("#imgur-url").innerHTML = url;
        document.body.className = "uploaded";
        analyzeImage(url);
    };
    // Ok, I don't handle the errors. An exercice for the reader.
    xhr.setRequestHeader('Authorization', 'Client-ID bae399be44e53ae');
    /* And now, we send the formdata */
    xhr.send(fd);
}

function analyzeImage(imageUrl) {
  console.log('start analysis');
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "https://api.openalpr.com/v2/recognize_url");
  xhr.onload = function() {
  // on success
    var data = JSON.parse(xhr.responseText);
    console.log('analysis complete');
    console.log(data);
    uploadAnalysis(imageUrl, data);
    if (data.results.length > 0) {
        var result = data.results[0].plate;
        document.querySelector("#plateNumber").innerHTML = '<h1>' + result +'</h1>';
}
   };
  var fd = new FormData();
  fd.append('image_url', imageUrl);
    // TODO: do this server side
  fd.append('secret_key', 'sk_d9f61fcd9db91602e13e76ae');
  fd.append('country', 'eu');
  fd.append('recognize_vehicle', 1);
  xhr.send(fd);
}

function uploadAnalysis(imageUrl, data) {
    console.log('send analysis back to plakspotr');
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "spot");
    // TODO: make this more generic.. the request should provide the redirection url
    xhr.onload = function() {
        var rtext = xhr.responseText;
        console.log(rtext);
        var data = JSON.parse(rtext);
        console.log('Redirecting now that analysis is ready');
        console.log(data);
        window.location.href = '/spots/lgf';
    };
    var fd = new FormData();
    fd.append('analysis', JSON.stringify(data));
    fd.append('url', imageUrl);
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
