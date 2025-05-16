document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".image-scroller").forEach(scroller => {
    const slides = scroller.querySelectorAll(".slide");
    const dots = scroller.querySelectorAll(".dot");
    let current = 0;

    function showSlide(index) {
      slides.forEach((s, i) => {
        s.classList.toggle("active", i === index);
      });
      dots.forEach((d, i) => {
        d.classList.toggle("active", i === index);
      });
      current = index;
    }

    if (dots.length) {
      dots.forEach((dot, index) => {
        dot.addEventListener("click", () => showSlide(index));
      });
    }

    // auto-advance
    setInterval(() => {
      let next = (current + 1) % slides.length;
      showSlide(next);
    }, 5000); // 5 seconden
  });
});
