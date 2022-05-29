

var about_site_modal = document.getElementById('about-site-dialog')
var about_site_dialog = new A11yDialog(about_site_modal)

about_site_dialog.on('show', function (about_site_modal, about_site_trigger) {
  console.log(about_site_modal)
  console.log(about_site_trigger)
})



var cast_crew_modal = document.getElementById('cast-crew-dialog')
if(cast_crew_modal){
  var cast_crew_dialog = new A11yDialog(cast_crew_modal)

  cast_crew_dialog.on('show', function (cast_crew_modal, cast_crew_trigger) {
    console.log(cast_crew_modal)
    console.log(cast_crew_trigger)
  })
}

var ploxel_modal = document.getElementById('ploxel-dialog')
if(ploxel_modal){
  var cast_crew_dialog = new A11yDialog(ploxel_modal)

  ploxel_dialog.on('show', function (ploxel_modal, ploxel_trigger) {
    console.log(ploxel_modal)
    console.log(ploxel_trigger)
  })
}

$(document).ready(function () {
  $("#sidebar-toggle").on("click", function () {
      $("aside.navigation").toggleClass("no-sidebar");
  });
});

/* Accordions, currently used for production notices */
const accordion = document.getElementsByClassName('prod-content-container');
var i = 0;
for (i=0; i<accordion.length; i++) {
  accordion[i].addEventListener('click', function () {
    this.classList.toggle('active')
  })
}

/* Philantro script */
(function() {
  const s = document.createElement('script');
  const ph = document.getElementsByTagName('script')[0];
  s.type = 'text/javascript'; s.async = true;
  s.src = 'https://philantro.s3.amazonaws.com/pdf/philantro.js';
  window.options = {OID: '954681622'};
  ph.parentNode.insertBefore(s, ph);
  })();