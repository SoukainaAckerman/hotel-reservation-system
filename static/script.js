// Theme Toggler
function initThemeToggler() {
    const themeTogglerSpan = document.querySelector('.theme-toggler span');
    if (themeTogglerSpan) {
        themeTogglerSpan.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme-variables');
            this.classList.toggle('active');
        });
    }
}

// Menu Toggle
function initMenuToggle() {
    const menuButton = document.getElementById('menu_bar');
    const aside = document.querySelector('aside');
    if (menuButton && aside) {
        menuButton.addEventListener('click', function() {
            aside.classList.toggle('active');
        });
    }
}

// Close Button
function initCloseButton() {
    const closeButton = document.getElementById('close_btn');
    const aside = document.querySelector('aside');
    if (closeButton && aside) {
        closeButton.addEventListener('click', function() {
            aside.classList.remove('active');
        });
    }
}

// Responsive Design
function initResponsiveDesign() {
    window.addEventListener('resize', function() {
        const aside = document.querySelector('aside');
        if (window.innerWidth <= 768 && aside) {
            aside.classList.remove('active');
        }
    });
}

// Booking Submenu
function initBookingSubmenu() {
    const bookingMenuButton = document.querySelector('.booking-menu');
const bookingSubmenu = document.querySelector('.booking-submenu');
    if (bookingMenuButton && bookingSubmenu) {
        bookingMenuButton.addEventListener('click', function(e) {
        e.preventDefault();
        bookingSubmenu.classList.toggle('active');
    });
}
}

// Room Navigation
function initRoomNavigation() {
    const roomsContainer = document.querySelector('.rooms-grid');
    const prevButton = document.querySelector('.prev-btn');
    const nextButton = document.querySelector('.next-btn');
    const cards = Array.from(document.querySelectorAll('.room-card'));
    let isAnimating = false;
    
    if (!roomsContainer || !prevButton || !nextButton || cards.length === 0) return;

    let currentIndex = 0;
    const cardWidth = 320; // Width of card + gap
    const visibleCards = 3; // Number of visible cards
    let autoScrollInterval;
    
    // Clone first and last cards for infinite effect
    const firstCardClone = cards[0].cloneNode(true);
    const lastCardClone = cards[cards.length - 1].cloneNode(true);
    roomsContainer.appendChild(firstCardClone);
    roomsContainer.insertBefore(lastCardClone, cards[0]);

    // Set initial position
    roomsContainer.style.transform = `translateX(-${cardWidth}px)`;

    function updateActiveCards() {
        const allCards = document.querySelectorAll('.room-card');
        allCards.forEach((card, index) => {
            card.classList.remove('active');
            if (index > currentIndex && index <= currentIndex + visibleCards) {
                card.classList.add('active');
            }
        });
    }

    function animate(from, to, duration) {
        const start = performance.now();
        isAnimating = true;

        function update(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const currentPosition = from + (to - from) * easeProgress;
            
            roomsContainer.style.transform = `translateX(${currentPosition}px)`;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                isAnimating = false;
                if (currentIndex >= cards.length) {
                    currentIndex = 0;
                    roomsContainer.style.transform = `translateX(-${cardWidth}px)`;
                } else if (currentIndex < 0) {
                    currentIndex = cards.length - 1;
                    roomsContainer.style.transform = `translateX(-${cardWidth * cards.length}px)`;
                }
            }
        }

        requestAnimationFrame(update);
    }

    function scrollNext() {
        if (isAnimating) return;
        currentIndex++;
        const from = -cardWidth * currentIndex;
        const to = -cardWidth * (currentIndex + 1);
        animate(from, to, 500);
        updateActiveCards();
    }

    function scrollPrev() {
        if (isAnimating) return;
        currentIndex--;
        const from = -cardWidth * (currentIndex + 2);
        const to = -cardWidth * (currentIndex + 1);
        animate(from, to, 500);
        updateActiveCards();
    }

    // Event Listeners
    nextButton.addEventListener('click', () => {
        clearInterval(autoScrollInterval);
        scrollNext();
        startAutoScroll();
    });

    prevButton.addEventListener('click', () => {
        clearInterval(autoScrollInterval);
        scrollPrev();
        startAutoScroll();
    });

    // Touch events
    let touchStartX = 0;
    let touchEndX = 0;

    roomsContainer.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        clearInterval(autoScrollInterval);
    }, { passive: true });

    roomsContainer.addEventListener('touchmove', (e) => {
        if (isAnimating) return;
        e.preventDefault();
        const touch = e.touches[0];
        const diff = touchStartX - touch.clientX;
        const move = -cardWidth * (currentIndex + 1) - diff;
        roomsContainer.style.transform = `translateX(${move}px)`;
    });

    roomsContainer.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].clientX;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > 50) {
            if (diff > 0) {
                scrollNext();
            } else {
                scrollPrev();
            }
        } else {
            // Return to original position if swipe wasn't long enough
            animate(
                -cardWidth * (currentIndex + 1),
                -cardWidth * (currentIndex + 1),
                300
            );
        }
        startAutoScroll();
    });

    // Auto scroll function
    function startAutoScroll() {
        if (autoScrollInterval) {
            clearInterval(autoScrollInterval);
        }
        autoScrollInterval = setInterval(scrollNext, 5000);
    }

    // Initialize
    updateActiveCards();
    startAutoScroll();

    // Pause auto-scroll when user hovers over the carousel
    roomsContainer.addEventListener('mouseenter', () => {
        clearInterval(autoScrollInterval);
    });

    roomsContainer.addEventListener('mouseleave', () => {
        startAutoScroll();
    });
}

// Initialize all functions when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initThemeToggler();
    initMenuToggle();
    initCloseButton();
    initResponsiveDesign();
    initBookingSubmenu();
    initRoomNavigation();
});

// Time range selector functionality
const timeRange = document.getElementById('timeRange');
if (timeRange) {
    timeRange.onchange = function(e) {
        console.log('Selected time range:', this.value);
    }
}

// Carousel functionality
function initRoomCarousel() {
    const container = document.querySelector('.rooms-grid');
    const cards = document.querySelectorAll('.room-card');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    if (!container || !cards.length || !prevBtn || !nextBtn) return;

    // Clone first and last cards for infinite effect
    const firstCardClone = cards[0].cloneNode(true);
    const lastCardClone = cards[cards.length - 1].cloneNode(true);
    container.appendChild(firstCardClone);
    container.insertBefore(lastCardClone, cards[0]);

    let currentIndex = 1;
    let isAnimating = false;
    const cardWidth = cards[0].offsetWidth + 20; // card width + gap
    const totalCards = cards.length + 2; // including clones

    // Set initial position
    container.style.transform = `translateX(-${cardWidth * currentIndex}px)`;

    function moveToCard(index, smooth = true) {
        if (isAnimating) return;
        isAnimating = true;
        
        container.style.transition = smooth ? 'transform 0.5s ease' : 'none';
        container.style.transform = `translateX(-${cardWidth * index}px)`;
        currentIndex = index;

        // Reset position after animation if needed
        if (smooth) {
            setTimeout(() => {
                if (currentIndex === totalCards - 1) {
                    container.style.transition = 'none';
                    currentIndex = 1;
                    container.style.transform = `translateX(-${cardWidth * currentIndex}px)`;
                } else if (currentIndex === 0) {
                    container.style.transition = 'none';
                    currentIndex = totalCards - 2;
                    container.style.transform = `translateX(-${cardWidth * currentIndex}px)`;
                }
                isAnimating = false;
            }, 500);
        } else {
            isAnimating = false;
        }
}

    // Event Listeners
    nextBtn.addEventListener('click', () => moveToCard(currentIndex + 1));
    prevBtn.addEventListener('click', () => moveToCard(currentIndex - 1));

    // Touch events for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    container.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        container.style.transition = 'none';
    });

    container.addEventListener('touchmove', (e) => {
        if (isAnimating) return;
        const touch = e.touches[0];
        const diff = touchStartX - touch.clientX;
        const move = -(cardWidth * currentIndex) - diff;
        container.style.transform = `translateX(${move}px)`;
    });

    container.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].clientX;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > 50) {
            if (diff > 0) {
                moveToCard(currentIndex + 1);
            } else {
                moveToCard(currentIndex - 1);
            }
        } else {
            moveToCard(currentIndex);
        }
    });

    // Auto scroll
    let autoScrollInterval;

    function startAutoScroll() {
        autoScrollInterval = setInterval(() => {
            moveToCard(currentIndex + 1);
        }, 5000);
    }

    function stopAutoScroll() {
        clearInterval(autoScrollInterval);
    }

    // Start auto scroll
    startAutoScroll();

    // Pause on hover
    container.addEventListener('mouseenter', stopAutoScroll);
    container.addEventListener('mouseleave', startAutoScroll);

    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const newCardWidth = cards[0].offsetWidth + 20;
            if (newCardWidth !== cardWidth) {
                moveToCard(currentIndex, false);
          }
        }, 250);
      });
    }
  
// Initialize all functions when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initRoomCarousel();
});

function changeRoomNumbers() {
  var roomType = document.getElementsByName("roomType")[0];
  var roomNumber = document.getElementsByName("roomNumber")[0];
  var selected = roomType.value;
  var prefix = "";
  
  if(selected == "standard") {
    prefix = "A";
  }
  else if(selected == "superior") {
    prefix = "B";
  }
  // ... etc
}


