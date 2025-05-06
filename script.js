document.addEventListener('DOMContentLoaded', () => {
    console.log('Finance Tracker is ready!');
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (event) => {
            alert('Form submitted successfully!');
        });
    }
});
