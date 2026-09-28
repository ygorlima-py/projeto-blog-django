document.addEventListener("DOMContentLoaded", () => {
  new Swiper(".landing-destinations-swiper", {
    slidesPerView: 1,
    spaceBetween: 16,
    loop: true,

    breakpoints: {
      640: {
        slidesPerView: 2,
        spaceBetween: 24,
      },
      960: {
        slidesPerView: 3,
        spaceBetween: 36,
      },
    },

    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },

    navigation: {
      nextEl: ".landing-destinations-next",
      prevEl: ".landing-destinations-prev",
    },

    pagination: {
      el: ".landing-destinations-pagination",
      clickable: true,
    },
  });

  new Swiper(".landing-stories-swiper", {
    slidesPerView: "auto",
    spaceBetween: 32,
    loop: true,

    autoplay: {
      delay: 4000,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },

    navigation: {
      nextEl: ".landing-stories-next",
      prevEl: ".landing-stories-prev",
    },

    pagination: {
      el: ".landing-stories-pagination",
      clickable: true,
    },
  });
});
