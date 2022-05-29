/* Accordions, currently used for production notices */
const notice_accordion = document.getElementsByClassName('notice-container');
if(notice_accordion){
  var i = 0;
  for (i=0; i<notice_accordion.length; i++) {
    notice_accordion[i].addEventListener('click', function () {
      this.classList.toggle('active')
    })
  }
}


$("#iFrameResizer0").on("load", function() {
  let head = $("#iFrameResizer0").contents().find("head");
  let css = '<style>#marg-end {background-color: #ffffff00 !important;}</style>';
  $(head).append(css);
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




/* Philantro script */
(function() {
  const s = document.createElement('script');
  const ph = document.getElementsByTagName('script')[0];
  s.type = 'text/javascript'; s.async = true;
  s.src = 'https://philantro.s3.amazonaws.com/pdf/philantro.js';
  window.options = {OID: '954681622'};
  ph.parentNode.insertBefore(s, ph);
  })();

