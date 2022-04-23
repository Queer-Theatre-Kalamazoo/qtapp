var dialogEl = document.getElementById('my-dialog')
var dialog = new A11yDialog(dialogEl)

dialog.on('show', function (dialogEl, triggerEl) {
  console.log(dialogEl)
  console.log(triggerEl)
})