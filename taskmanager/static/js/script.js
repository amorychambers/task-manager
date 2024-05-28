document.addEventListener('DOMContentLoaded', function() {
    let sidenav = document.querySelectorAll('.sidenav');
    let modals = document.querySelectorAll('.modal')
    let datepicker = document.querySelectorAll('.datepicker')
    let selector = document.querySelectorAll('select')
    let collapsible = document.querySelectorAll('.collapsible')
    M.Sidenav.init(sidenav);
    M.Modal.init(modals)
    M.Datepicker.init(datepicker, {format: "dd mmmm, yyyy", i18n: {done: "Select"}})
    M.FormSelect.init(selector)
    M.Collapsible.init(collapsible, {
      onOpenStart: function(e){
        let div = e.firstElementChild
        let icon = div.firstElementChild
        icon.classList.remove("fa-caret-down")
        icon.classList.add("fa-caret-right")
    }, onCloseStart: function(e){
        let div = e.firstElementChild
        let icon = div.firstElementChild
        icon.classList.remove("fa-caret-right")
        icon.classList.add("fa-caret-down")
    }
  })
  });