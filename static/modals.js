async function showPrayerTimes(event) {
    event.preventDefault();
    const modal = document.getElementById('prayerTimesModal');
    const container = modal.querySelector('.prayer-times-container');
    
    try {
        // Get prayer times from your API
        const response = await fetch('/get-prayer-times');
        const times = await response.json();
        
        container.innerHTML = `
            <div class="prayer-time">
                <span class="prayer-name">الفجر</span>
                <span class="prayer-time-value">${times.fajr}</span>
            </div>
            <div class="prayer-time">
                <span class="prayer-name">الظهر</span>
                <span class="prayer-time-value">${times.dhuhr}</span>
            </div>
            <div class="prayer-time">
                <span class="prayer-name">العصر</span>
                <span class="prayer-time-value">${times.asr}</span>
            </div>
            <div class="prayer-time">
                <span class="prayer-name">المغرب</span>
                <span class="prayer-time-value">${times.maghrib}</span>
            </div>
            <div class="prayer-time">
                <span class="prayer-name">العشاء</span>
                <span class="prayer-time-value">${times.isha}</span>
            </div>
            <div class="location-info">
                <i class="fas fa-map-marker-alt"></i>
                <span>${times.city || 'جاري تحديد الموقع...'}</span>
            </div>
        `;
        
        modal.style.display = 'flex';
    } catch (error) {
        console.error('Error fetching prayer times:', error);
    }
}

async function showCalendar(event) {
    event.preventDefault();
    const modal = document.getElementById('calendarModal');
    const container = modal.querySelector('.date-display');
    
    try {
        // Get Hijri date from your API
        const response = await fetch('/get-hijri-date');
        const date = await response.json();
        
        container.innerHTML = `
            <div class="hijri-date">${date.hijri}</div>
            <div class="gregorian-date">${date.gregorian}</div>
        `;
        
        modal.style.display = 'flex';
    } catch (error) {
        console.error('Error fetching calendar:', error);
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
} 