document.addEventListener("DOMContentLoaded", () => {
    const storyViewer = document.querySelector(".story-viewer");

    if (!storyViewer) {
        return;
    }

    const slides = Array.from(
        storyViewer.querySelectorAll(".story-slide")
    );

    const progressBars = Array.from(
        storyViewer.querySelectorAll(".story-progress-bar")
    );

    const previousButton = storyViewer.querySelector(
        "[data-story-previous]"
    );

    const nextButton = storyViewer.querySelector(
        "[data-story-next]"
    );

    const pauseButton = storyViewer.querySelector(
        "[data-story-pause]"
    );

    const SLIDE_DURATION_MS = 5000;

    let currentSlideIndex = 0;
    let slideTimerId = null;
    let isPaused = false;
    let remainingTimeMs = SLIDE_DURATION_MS;
    let playbackStartedAt = 0;

    function restartElementAnimations(activeSlide) {
        const allElements = storyViewer.querySelectorAll(".story-element");
        const activeElements = activeSlide.querySelectorAll(".story-element");

        allElements.forEach((element) => {
            element.classList.remove("is-visible");
        });

        activeElements.forEach((element) => {
            const animation = element.dataset.animation || "none";
            const delayMs =
                Number.parseInt(element.dataset.delayMs, 10) || 0;

            element.dataset.animation = animation;

            element.style.setProperty(
                "--story-animation-delay",
                `${delayMs}ms`
            );
        });


        void activeSlide.offsetWidth;

        activeElements.forEach((element) => {
            element.classList.add("is-visible");
        });
    }

    function resetProgressBars(activeIndex) {
        progressBars.forEach((progressBar, index) => {
            progressBar.style.transition = "none";
            progressBar.style.width = index < activeIndex ? "100%" : "0%";
        });
    }

    function startActiveProgress(durationMs) {
        const activeProgressBar = progressBars[currentSlideIndex];

        if (!activeProgressBar) {
            return;
        }

        void activeProgressBar.offsetWidth;

        activeProgressBar.style.transition =
            `width ${durationMs}ms linear`;

        activeProgressBar.style.width = "100%";
    }

    function startPlayback() {
        window.clearTimeout(slideTimerId);

        if (isPaused) {
            return;
        }

        playbackStartedAt = performance.now();
        startActiveProgress(remainingTimeMs);

        if (slides.length <= 1) {
            return;
        }

        slideTimerId = window.setTimeout(() => {
            showSlide(currentSlideIndex + 1);
        }, remainingTimeMs);
    }

    function restartPlayback() {
        window.clearTimeout(slideTimerId);

        remainingTimeMs = SLIDE_DURATION_MS;

        resetProgressBars(currentSlideIndex);

        if (!isPaused) {
            startPlayback();
        }
    }

    function updatePauseButton() {
        if (!pauseButton) {
            return;
        }

        const icon = pauseButton.querySelector("i");

        pauseButton.setAttribute("aria-pressed", String(isPaused));
        pauseButton.setAttribute(
            "aria-label",
            isPaused ? "Continuar story" : "Pausar story"
        );

        if (icon) {
            icon.classList.toggle("fa-pause", !isPaused);
            icon.classList.toggle("fa-play", isPaused);
        }
    }

    function pausePlayback() {
        if (isPaused) {
            return;
        }

        const elapsedTime = performance.now() - playbackStartedAt;

        remainingTimeMs = Math.max(
            0,
            remainingTimeMs - elapsedTime
        );

        isPaused = true;

        window.clearTimeout(slideTimerId);
        slideTimerId = null;

        const activeProgressBar = progressBars[currentSlideIndex];

        if (activeProgressBar) {
            const currentWidth =
                activeProgressBar.getBoundingClientRect().width;

            activeProgressBar.style.transition = "none";
            activeProgressBar.style.width = `${currentWidth}px`;
        }

        updatePauseButton();
    }

    function resumePlayback() {
        if (!isPaused) {
            return;
        }

        isPaused = false;
        updatePauseButton();

        if (remainingTimeMs <= 0) {
            showSlide(currentSlideIndex + 1);
            return;
        }

        startPlayback();
    }

    function showSlide(requestedIndex) {
        if (slides.length === 0) {
            return;
        }

        const normalizedIndex =
            (requestedIndex + slides.length) % slides.length;

        slides.forEach((slide, index) => {
            const isActive = index === normalizedIndex;

            slide.classList.toggle("is-active", isActive);
            slide.setAttribute("aria-hidden", String(!isActive));
        });

        currentSlideIndex = normalizedIndex;

        restartElementAnimations(slides[currentSlideIndex]);
        restartPlayback();
    }

    if (previousButton) {
        previousButton.addEventListener("click", () => {
            showSlide(currentSlideIndex - 1);
        });
    }

    if (nextButton) {
        nextButton.addEventListener("click", () => {
            showSlide(currentSlideIndex + 1);
        });
    }

    if (pauseButton) {
        pauseButton.addEventListener("click", () => {
            if (isPaused) {
                resumePlayback();
            } else {
                pausePlayback();
            }
        });
    }

    updatePauseButton();
    const ctaLinks = storyViewer.querySelectorAll(".story-element--cta");
    ctaLinks.forEach((ctaLink) => {
        ctaLink.addEventListener("click", (event) => {
            event.stopPropagation();
        });
    });
    showSlide(currentSlideIndex);
});
