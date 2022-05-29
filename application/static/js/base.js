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



$(document).ready(function () {
  $("#nav-accordion-trigger").click(function () {
      $(".nav-accordion-body").toggle();
  });
});

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


const nav = document.querySelector('#nav');
const menu = document.querySelector('#menu');
const menuToggle = document.querySelector('.nav__toggle');
let isMenuOpen = false; // TOGGLE MENU ACTIVE STATE

menuToggle.addEventListener('click', e => {
  e.preventDefault();
  isMenuOpen = !isMenuOpen; // toggle a11y attributes and active class

  menuToggle.setAttribute('aria-expanded', String(isMenuOpen));
  menu.hidden = !isMenuOpen;
  nav.classList.toggle('nav--open');
}); // TRAP TAB INSIDE NAV WHEN OPEN

nav.addEventListener('keydown', e => {
  // abort if menu isn't open or modifier keys are pressed
  if (!isMenuOpen || e.ctrlKey || e.metaKey || e.altKey) {
    return;
  } // listen for tab press and move focus
  // if we're on either end of the navigation


  const menuLinks = menu.querySelectorAll('.nav__link');

  if (e.keyCode === 9) {
    if (e.shiftKey) {
      if (document.activeElement === menuLinks[0]) {
        menuToggle.focus();
        e.preventDefault();
      }
    } else if (document.activeElement === menuToggle) {
      menuLinks[0].focus();
      e.preventDefault();
    }
  }
});