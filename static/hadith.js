document.addEventListener('DOMContentLoaded', function() {
    loadDailyHadith();
});

async function loadDailyHadith() {
    try {
        console.log('Starting to fetch hadith');
        const response = await fetch('/get-daily-hadith');
        console.log('Fetch response:', response);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Hadith data loaded:', data);
        
        // Update DOM elements
        const textElement = document.querySelector('.hadith-text');
        const sourceElement = document.querySelector('.source');
        const categoryElement = document.querySelector('.category');
        
        if (textElement) textElement.textContent = data.text;
        if (sourceElement) sourceElement.textContent = data.source;
        if (categoryElement) categoryElement.textContent = data.title;
        
    } catch (error) {
        console.error('Error loading hadith:', error);
        const textElement = document.querySelector('.hadith-text');
        if (textElement) {
            textElement.textContent = 'عذراً، حدث خطأ في تحميل الحديث';
        }
    }
}

function shareHadith(platform) {
    const hadithText = document.querySelector('.hadith-text')?.textContent || '';
    const source = document.querySelector('.source')?.textContent || '';
    
    const shareText = `${hadithText}\n[${source}]`;
    
    const shareUrls = {
        whatsapp: `https://wa.me/?text=${encodeURIComponent(shareText)}`,
        facebook: `https://www.facebook.com/sharer/sharer.php?quote=${encodeURIComponent(shareText)}`,
        twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}`
    };
    
    window.open(shareUrls[platform], '_blank');
}

function copyHadith() {
    const hadithText = document.querySelector('.hadith-text')?.textContent || '';
    const source = document.querySelector('.source')?.textContent || '';
    
    const textToCopy = `${hadithText}\n[${source}]`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        const button = document.querySelector('.hadith-share .fa-copy')?.parentElement;
        if (button) {
            button.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy"></i>';
            }, 2000);
        }
    });
} 
