$(function() {
  $("#download")
    .on('click', function () {
      var content = $("#filter").text();
      var filename = "reddit-personal-filter-list-builder.txt";
      var blob = new Blob([content], {
        type: "text/plain;charset=utf-8"
      });
      saveAs(blob, filename);
    })
  ;
  $("#form")
    .submit(function(evt) {
      evt.preventDefault();
      $.post("/filter", $(this).serialize())
        .then(function(data) {
          $("#filter").text(data);
        })
      ;
    })
  ;
})
