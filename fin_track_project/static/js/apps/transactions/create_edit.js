document.addEventListener('DOMContentLoaded', function () {
    const typeInputs = document.querySelectorAll('input[name="transaction_type"]');
    const categorySelect = document.getElementById('id_category');
    
    if (!categorySelect || typeInputs.length === 0) {
        console.warn('Elementos não encontrados');
        return;
    }

    function filterCategories() {
        const selectedType = document.querySelector('input[name="transaction_type"]:checked')?.value;
        if (!selectedType) return;
        const allOptions = categorySelect.querySelectorAll('option');
        allOptions.forEach(option => {
            const dataType = (option.getAttribute('data-type') || '').trim();
            if (!dataType) {
                option.style.display = '';
                return;
            }

            let shouldShow = false;

            if (selectedType === 'despesa') {
                shouldShow = dataType === 'despesa';
            } else if (selectedType === 'receita') {
                shouldShow = dataType === 'receita';
            }
            option.style.display = shouldShow ? '' : 'none';
        });
    }
    
    typeInputs.forEach(input => {
        input.addEventListener('change', filterCategories);
    });
    
    filterCategories();
});