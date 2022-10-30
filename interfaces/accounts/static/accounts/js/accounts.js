$(document).ready(function() {

  $('#id_select_voice').on('change', function() {
    change($(this).val());
  });

});

function change(sourceUrl) {

    var audio = document.getElementById("player");
    var source = document.getElementById("mp3_src");

    audio.pause();
    console.log('asdasd')

    if (sourceUrl) {
        source.src = sourceUrl.split(';')[0];
        console.log(source.src)
        audio.load();
    }
}
