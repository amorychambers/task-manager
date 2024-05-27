document.addEventListener('DOMContentLoaded', function() {
    let sidenav = document.querySelectorAll('.sidenav');
    let modals = document.querySelectorAll('.modal')
    M.Sidenav.init(sidenav);
    M.Modal.init(modals)
  });