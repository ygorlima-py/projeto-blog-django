document.addEventListener("DOMContentLoaded", () => {
  new Swiper(".landing-destinations-swiper", {
    slidesPerView: 3,
    spaceBetween: 36,
    loop: true,

    navigation: {
      nextEl: ".landing-destinations-next",
      prevEl: ".landing-destinations-prev",
    },

    pagination: {
      el: ".landing-destinations-pagination",
      clickable: true,
    },
  });
});