document.addEventListener('DOMContentLoaded', () => {
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
