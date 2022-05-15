var about_site_modal = document.getElementById('my-dialog')
var about_site_dialog = new A11yDialog(about_site_modal)

about_site_dialog.on('show', function (about_site_modal, about_site_trigger) {
  console.log(about_site_modal)
  console.log(about_site_trigger)
})


var cast_crew_modal = document.getElementById('cast-crew-dialog')
var cast_crew_dialog = new A11yDialog(cast_crew_modal)

cast_crew_dialog.on('show', function (cast_crew_modal, cast_crew_trigger) {
  console.log(cast_crew_modal)
  console.log(cast_crew_trigger)
})