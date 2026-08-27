document.addEventListener('DOMContentLoaded', () => {
    const summaryToggle = document.querySelector('#summary-toggle');
    const summaryModal = document.querySelector('#summary-modal');

    if (summaryToggle && summaryModal) {
        const closeSummary = () => {
            summaryModal.hidden = true;
            document.body.classList.remove('modal-open');
        };
        summaryToggle.addEventListener('click', () => {
            summaryModal.hidden = false;
            document.body.classList.add('modal-open');
        });
        summaryModal.querySelectorAll('[data-summary-close]').forEach((element) => element.addEventListener('click', closeSummary));
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && !summaryModal.hidden) closeSummary();
        });
    }

    if (window.location.hash === '#summary-modal' && summaryModal) {
        summaryModal.hidden = false;
        document.body.classList.add('modal-open');
    }

    const addButton = document.querySelector('#add-referral');
    const list = document.querySelector('#referral-list');
    const template = document.querySelector('#empty-referral');
    const totalForms = document.querySelector('#id_referrals-TOTAL_FORMS');
    const emptyMessage = document.querySelector('.no-referrals');

    if (!addButton || !list || !template || !totalForms) return;

    addButton.addEventListener('click', () => {
        const index = Number(totalForms.value);
        list.insertAdjacentHTML('beforeend', template.innerHTML.replaceAll('__prefix__', index));
        totalForms.value = index + 1;
        emptyMessage.hidden = true;
    });

    list.addEventListener('click', (event) => {
        const removeButton = event.target.closest('.remove-referral');
        if (!removeButton) return;

        const row = removeButton.closest('.referral-row');
        const deleteInput = row.querySelector('input[name$="-DELETE"]');
        if (deleteInput) {
            deleteInput.checked = true;
            row.hidden = true;
        } else {
            row.remove();
            totalForms.value = list.querySelectorAll('.referral-row:not([hidden])').length;
        }

        if (!list.querySelector('.referral-row:not([hidden])')) emptyMessage.hidden = false;
    });
});
