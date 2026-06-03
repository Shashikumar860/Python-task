// Main JavaScript for Movie Ticket Booking Application

document.addEventListener('DOMContentLoaded', function() {
    // 1. Interactive Seat Booking Logic
    const seatContainer = document.querySelector('.seat-rows');
    if (seatContainer) {
        initSeatBooking();
    }

    // 2. Alert Dismissal Logic
    const alertCloses = document.querySelectorAll('.flash-close');
    alertCloses.forEach(btn => {
        btn.addEventListener('click', function() {
            const message = this.closest('.flash-message');
            if (message) {
                message.style.opacity = '0';
                setTimeout(() => message.remove(), 300);
            }
        });
    });

    // 3. Admin Panel Tab Switching
    const adminTabs = document.querySelectorAll('.admin-tab');
    if (adminTabs.length > 0) {
        initAdminTabs();
    }
});

/**
 * Handle seat click events, validation, pricing summaries
 */
function initSeatBooking() {
    const seats = document.querySelectorAll('.seat:not(.occupied)');
    const selectedSeatsInput = document.getElementById('selected-seats-input');
    const selectedSeatsDisplay = document.getElementById('selected-seats-display');
    const ticketCountDisplay = document.getElementById('ticket-count-display');
    const totalPriceDisplay = document.getElementById('total-price-display');
    const checkoutSubmitBtn = document.getElementById('checkout-submit-btn');
    
    let selectedSeats = [];
    let totalPrice = 0.00;

    seats.forEach(seat => {
        seat.addEventListener('click', function() {
            const seatId = this.getAttribute('data-seat-id');
            const seatPrice = parseFloat(this.getAttribute('data-price'));

            if (this.classList.contains('selected')) {
                // Deselect seat
                this.classList.remove('selected');
                selectedSeats = selectedSeats.filter(id => id !== seatId);
                totalPrice -= seatPrice;
            } else {
                // Select seat
                this.classList.add('selected');
                selectedSeats.push(seatId);
                totalPrice += seatPrice;
            }

            // Keep array sorted A-Z/1-9 for neatness
            selectedSeats.sort();

            // Update UI
            if (selectedSeats.length > 0) {
                selectedSeatsDisplay.textContent = selectedSeats.join(', ');
                ticketCountDisplay.textContent = `${selectedSeats.length} Ticket${selectedSeats.length > 1 ? 's' : ''}`;
                totalPriceDisplay.textContent = `₹${Math.round(totalPrice)}`;
                selectedSeatsInput.value = selectedSeats.join(',');
                checkoutSubmitBtn.disabled = false;
            } else {
                selectedSeatsDisplay.textContent = 'None';
                ticketCountDisplay.textContent = '0 Tickets';
                totalPriceDisplay.textContent = '₹0';
                selectedSeatsInput.value = '';
                checkoutSubmitBtn.disabled = true;
            }
        });
    });

    // Form submission validation
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            if (selectedSeats.length === 0) {
                e.preventDefault();
                alert('Please select at least one seat before booking!');
            }
        });
    }
}

/**
 * Tab switcher helper for Admin Panel
 */
function initAdminTabs() {
    const tabs = document.querySelectorAll('.admin-tab');
    const contents = document.querySelectorAll('.admin-tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            // Toggle tab header active classes
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            // Toggle tab content active classes
            contents.forEach(c => {
                c.classList.remove('active');
                if (c.id === `tab-${targetTab}`) {
                    c.classList.add('active');
                }
            });
        });
    });

    // Check URL query parameters on page load to see if a specific tab should be active
    const urlParams = new URLSearchParams(window.location.search);
    const activeTabParam = urlParams.get('tab');
    if (activeTabParam) {
        const matchingTab = document.querySelector(`.admin-tab[data-tab="${activeTabParam}"]`);
        if (matchingTab) {
            matchingTab.click();
        }
    }
}

