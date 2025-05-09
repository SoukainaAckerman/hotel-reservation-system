const sideMenu = document.querySelector('aside');
const menuBtn = document.querySelector('#menu_bar');
const closeBtn = document.querySelector('#close_btn');
const themeToggler = document.querySelector('.theme-toggler');

menuBtn.addEventListener('click',()=>{
    sideMenu.style.display = "block"
});

closeBtn.addEventListener('click',()=>{
    sideMenu.style.display = "none"
});

themeToggler.addEventListener('click',()=>{
    document.body.classList.toggle('dark-theme-variables')
    themeToggler.querySelector('span:nth-child(1').classList.toggle('active')
    themeToggler.querySelector('span:nth-child(2').classList.toggle('active')
});

//  pour gérer le sous-menu Booking
const bookingMenu = document.querySelector('.booking-menu');
const bookingSubmenu = document.querySelector('.booking-submenu');

if (bookingMenu && bookingSubmenu) {
    bookingMenu.addEventListener('click', (e) => {
        e.preventDefault();
        bookingSubmenu.classList.toggle('active');
    });
}

// Initialize Charts
document.addEventListener('DOMContentLoaded', function() {
    // Sales Revenue Chart
    const salesRevenueCtx = document.getElementById('salesRevenueChart');
    if (salesRevenueCtx) {
        new Chart(salesRevenueCtx, {
            type: 'bar',
            data: {
                labels: Array.from({length: 30}, (_, i) => i + 1),
                datasets: [{
                    data: [
                        350, 400, 450, 400, 350, 400, 350, 400, 350, 400,
                        450, 350, 400, 450, 500, 400, 350, 250, 450, 400,
                        450, 500, 450, 500, 450, 400, 350, 400, 350, 300
                    ],
                    backgroundColor: '#7380ec',
                    borderRadius: 3,
                    barThickness: 6,
                    maxBarThickness: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            color: '#67748e',
                            font: {
                                size: 10
                            },
                            maxRotation: 0
                        }
                    },
                    y: {
                        grid: {
                            color: '#e9ecef',
                            drawBorder: false,
                            lineWidth: 0.5
                        },
                        ticks: {
                            color: '#67748e',
                            font: {
                                size: 10
                            },
                            maxTicksLimit: 6,
                            padding: 10
                        },
                        min: 0,
                        max: 600
                    }
                }
            }
        });
    }

    // Room Booking Chart
    const roomBookingCtx = document.getElementById('roomBookingChart');
    if (roomBookingCtx) {
        new Chart(roomBookingCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [1913, 859, 482, 138],
                    backgroundColor: [
                        '#7380ec',  // Single
                        '#41f1b6',  // Double
                        '#ffbb55',  // Delux
                        '#ff7782'   // Suit
                    ],
                    borderWidth: 0,
                    spacing: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                radius: '90%',
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
});

// Time range selector functionality
const timeRange = document.getElementById('timeRange');
timeRange.addEventListener('change', function(e) {
  // Here you would typically fetch new data based on the selected time range
  // For this example, we'll just log the selected value
  console.log('Selected time range:', e.target.value);
});

// Revenue Bar Chart
const ctxRevenue = document.getElementById('revenueBarChart');
if (ctxRevenue) {
  new Chart(ctxRevenue, {
    type: 'bar',
    data: {
      labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
      datasets: [{
        label: 'Revenue',
        data: Array.from({length: 30}, () => Math.floor(Math.random() * 1000 + 200)),
        backgroundColor: '#7d8df1',
        borderRadius: 5
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: '#777' },
          grid: { display: false }
        },
        x: {
          ticks: { display: false },
          grid: { display: false }
        }
      },
      plugins: {
        legend: { display: false }
      },
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

// Booking Pie Chart
const ctxBooking = document.getElementById('bookingChart');
if (ctxBooking) {
  new Chart(ctxBooking, {
    type: 'doughnut',
    data: {
      labels: ['Single', 'Double', 'Delux', 'Suit'],
      datasets: [{
        label: 'Room Type',
        data: [1913, 859, 482, 138],
        backgroundColor: ['#7d8df1', '#41f1b6', '#fdd76e', '#ff7782'],
        borderWidth: 0
      }]
    },
    options: {
      cutout: '65%',
      plugins: {
        legend: { display: false }
      },
      responsive: true,
      maintainAspectRatio: false
    }
  });
}
window.addEventListener("DOMContentLoaded", () => {
    // Bar Chart for Sales Revenue
    const revenueCtx = document.getElementById("revenueBarChart");
    if (revenueCtx) {
      new Chart(revenueCtx, {
        type: "bar",
        data: {
          labels: Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`),
          datasets: [{
            label: "Revenue",
            data: Array.from({ length: 30 }, () => Math.floor(Math.random() * 1000 + 300)),
            backgroundColor: "#7380ec"
          }]
        },
        options: {
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }
  
    // Doughnut Chart for Room Booking
    const bookingCtx = document.getElementById("bookingChart");
    if (bookingCtx) {
      new Chart(bookingCtx, {
        type: "doughnut",
        data: {
          labels: ["Single", "Double", "Delux", "Suit"],
          datasets: [{
            label: "Rooms",
            data: [1913, 859, 482, 138],
            backgroundColor: ["#7b8cff", "#4ADE80", "#FCD34D", "#F87171"]
          }]
        },
        options: {
          cutout: "70%",
          plugins: {
            legend: {
              position: "bottom"
            }
          }
        }
      });
    }
  });
  


