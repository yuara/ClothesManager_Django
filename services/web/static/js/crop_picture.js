// Open the modal with the preview
$("#id_picture").change(function () {
  if (this.files && this.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $("#image").attr("src", e.target.result);
      $("#modalCrop").modal("show");
    }
    reader.readAsDataURL(this.files[0]);
  }
});
// Handle the cropper box
var $image = $("#image");
var cropBoxData;
var canvasData;
$("#modalCrop").on("shown.bs.modal", function () {
  $image.cropper({
    viewMode: 1,
    dragMode: 'move',
    aspectRatio: 1/1,
    minCropBoxWidth: 200,
    minCropBoxHeight: 200,
    ready: function () {
      $image.cropper("setCanvasData", canvasData);
      $image.cropper("setCropBoxData", cropBoxData);
    }
  });
}).on("hidden.bs.modal", function () {
  cropBoxData = $image.cropper("getCropBoxData");
  canvasData = $image.cropper("getCanvasData");
  $image.cropper("destroy");
});

// Enable zoom in button
$(".js-zoom-in").click(function () {
  $image.cropper("zoom", 0.1);
});

// Enable zoom out button
$(".js-zoom-out").click(function () {
  $image.cropper("zoom", -0.1);
});

// Collect the data and post to the server
$(".js-crop-and-upload").click(function () {
  var cropData = $image.cropper("getData");
  $("#modalCrop").modal("hide");
  $("#id_x").val(cropData["x"]);
  $("#id_y").val(cropData["y"]);
  $("#id_width").val(cropData["width"]);
  $("#id_height").val(cropData["height"]);
  if ($('canvas')) {
    $('canvas').remove();
  }
  document.getElementById("cropped-preview-img").append($image.cropper("getCroppedCanvas"));
  document.getElementsByTagName("canvas")[0].classList.add("default-preview-img");
  $('#preview-title').show()
});
