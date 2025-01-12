// Theme Toggle
function toggleTheme() {
    document.body.dataset.theme = 
        document.body.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', document.body.dataset.theme);
}

// Large Text Toggle
function toggleLargeText() {
    document.body.dataset.largeText = 
        document.body.dataset.largeText === 'true' ? 'false' : 'true';
    localStorage.setItem('largeText', document.body.dataset.largeText);
}

// High Contrast Toggle
function toggleContrast() {
    document.body.dataset.highContrast = 
        document.body.dataset.highContrast === 'true' ? 'false' : 'true';
    localStorage.setItem('highContrast', document.body.dataset.highContrast);
}

// Next Prayer Countdown
function updateNextPrayer(prayerTimes) {
    const now = new Date();
    let nextPrayer = null;
    let remainingTime = null;

    // Calculate next prayer and remaining time
    // Add your prayer time comparison logic here

    // Update DOM
    document.querySelector('.prayer-name').textContent = nextPrayer;
    document.querySelector('.countdown-timer').textContent = remainingTime;
    updateProgressBar(prayerTimes, nextPrayer);
}

// Update Progress Bar
function updateProgressBar(prayerTimes, nextPrayer) {
    // Calculate progress percentage
    // Add your progress calculation logic here
    
    document.querySelector('.progress').style.width = `${progress}%`;
}

// Islamic Dates
function updateIslamicDates() {
    // Use hijri-js to get Islamic date
    const hijriDate = new Hijri(new Date());
    document.getElementById('hijri-date').textContent = hijriDate.toString('ar');
    
    // Update upcoming events
    updateUpcomingEvents(hijriDate);
}

// Upcoming Events
function updateUpcomingEvents(hijriDate) {
    const events = getIslamicEvents(hijriDate);
    const upcomingEventsElement = document.getElementById('upcoming-events');
    upcomingEventsElement.innerHTML = events
        .map(event => `<div class="event">${event.name}: ${event.date}</div>`)
        .join('');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load saved preferences
    const theme = localStorage.getItem('theme') || 'light';
    const largeText = localStorage.getItem('largeText') || 'false';
    const highContrast = localStorage.getItem('highContrast') || 'false';

    document.body.dataset.theme = theme;
    document.body.dataset.largeText = largeText;
    document.body.dataset.highContrast = highContrast;

    // Start updates
    updateIslamicDates();
    setInterval(updateIslamicDates, 60000); // Update every minute
}); 