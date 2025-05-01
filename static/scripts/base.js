const navLinks = document.querySelectorAll(".nav-menu .nav-link");
const menuOpenButton = document.querySelector("#menu-open-button");
const menuCloseButton = document.querySelector("#menu-close-button");
const menuTitles = document.querySelectorAll('.menu-item .name');

menuOpenButton.addEventListener("click", () => {
    //Toggle mobile menu visibility
  document.body.classList.toggle("show-mobile-menu");
});

// Close menu when the close button is clicked
menuCloseButton.addEventListener("click", () => menuOpenButton.click ());

// Close menu when the nav link is clicked
navLinks.forEach(link => {
    link.addEventListener("click", () => menuOpenButton.click ());
});

// Toggle menu details when the title is clicked
menuTitles.forEach(title => {
  title.addEventListener('click', () => {
      const menuItem = title.closest('.menu-item');
      const menuDetails = menuItem.querySelector('.menu-details');

      if (menuDetails) {
          const isVisible = menuDetails.style.display === 'block';
          menuDetails.style.display = isVisible ? 'none' : 'block';
      }
  });
});

// make sure titles look clickable
document.querySelectorAll('.toggle-title').forEach(el=>{
    el.style.cursor = 'pointer';
  });
  
  // toggle the matching .menu-details div
  document.querySelectorAll('.toggle-title').forEach(title=>{
    title.addEventListener('click',()=>{
      const id = title.getAttribute('data-details-id');
      const details = document.getElementById(id);
      if(!details) return;
      details.style.display = details.style.display==='block' ? 'none' : 'block';
    });
  });

  