$mainSidenav = "mainSidenav"
/* Element ID that will slide over when the sidenav opens */
$mainSidenavTarget = "BODY"

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px and add a black background color to body */
function openNav() {
    document.getElementById($mainSidenav).style.width = "250px";
    document.getElementById($mainSidenavTarget).style.marginLeft = "250px";
  }
  
  /* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
  function closeNav() {
    document.getElementById($mainSidenav).style.width = "0";
    document.getElementById($mainSidenavTarget).style.marginLeft = "0";
}

