// EZHAN Main Logic
document.addEventListener('DOMContentLoaded', () => {
    console.log('EZHAN Website Loaded Successfully!');
    
    // Thêm hiệu ứng click cho các card
    const cards = document.querySelectorAll('.option-card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Có thể thêm hiệu ứng loading hoặc transition ở đây
        });
    });
});
