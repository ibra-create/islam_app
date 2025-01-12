// Prayer Times and Calendar functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getPrayerTimes, handleLocationError);
    } else {
        handleLocationError();
    }

    // Update Hijri date
    updateHijriDate();
});

async function getPrayerTimes(position) {
    const { latitude, longitude } = position.coords;
    
    try {
        // Get city name
        const geocodeResponse = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`);
        const locationData = await geocodeResponse.json();
        document.getElementById('city-name').textContent = locationData.address.city || locationData.address.town || locationData.address.state;

        // Get prayer times
        const date = new Date();
        const prayerTimesResponse = await fetch(`https://api.aladhan.com/v1/timings/${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()}?latitude=${latitude}&longitude=${longitude}&method=2`);
        const prayerData = await prayerTimesResponse.json();

        // Update prayer times
        const timings = prayerData.data.timings;
        document.getElementById('fajr-time').textContent = timings.Fajr;
        document.getElementById('dhuhr-time').textContent = timings.Dhuhr;
        document.getElementById('asr-time').textContent = timings.Asr;
        document.getElementById('maghrib-time').textContent = timings.Maghrib;
        document.getElementById('isha-time').textContent = timings.Isha;

        // Check for next prayer and set reminder
        setNextPrayerReminder(timings);
    } catch (error) {
        console.error('Error fetching prayer times:', error);
        handleLocationError();
    }
}

function updateHijriDate() {
    const date = new Date();
    fetch(`https://api.aladhan.com/v1/gToH?date=${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()}`)
        .then(response => response.json())
        .then(data => {
            const hijri = data.data.hijri;
            document.getElementById('hijri-date').textContent = 
                `${hijri.day} ${hijri.month.ar} ${hijri.year}`;
            document.getElementById('gregorian-date').textContent = 
                date.toLocaleDateString('ar-SA', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        })
        .catch(error => {
            console.error('Error fetching Hijri date:', error);
            document.getElementById('hijri-date').textContent = 'خطأ في تحميل التاريخ';
        });
}

function setNextPrayerReminder(timings) {
    const now = new Date();
    const prayers = Object.entries(timings);
    const mainPrayers = prayers.filter(([name]) => 
        ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'].includes(name));

    for (const [name, time] of mainPrayers) {
        const prayerTime = new Date();
        const [hours, minutes] = time.split(':');
        prayerTime.setHours(hours, minutes, 0);

        if (prayerTime > now) {
            const timeUntilPrayer = prayerTime - now;
            setTimeout(() => {
                showPrayerNotification(name);
            }, timeUntilPrayer);
            break;
        }
    }
}

function showPrayerNotification(prayerName) {
    if (Notification.permission === "granted") {
        new Notification("حان وقت الصلاة", {
            body: `حان الآن موعد صلاة ${prayerName}`,
            icon: "/static/images/prayer-icon.png"
        });
    } else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                showPrayerNotification(prayerName);
            }
        });
    }
}

function handleLocationError() {
    document.getElementById('city-name').textContent = 'تعذر تحديد الموقع';
    const timeElements = document.querySelectorAll('.prayer-time-value');
    timeElements.forEach(el => el.textContent = '--:--');
} 