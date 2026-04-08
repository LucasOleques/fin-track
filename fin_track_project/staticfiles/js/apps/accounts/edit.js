const typeSelect = document.getElementById('id_type');
const creditLimitGroup = document.getElementById('credit_limit_group');

function toggleCreditLimit() {
    if (typeSelect.value === 'cartao') {
        creditLimitGroup.style.display = 'block';
    } else {
        creditLimitGroup.style.display = 'none';
    }
}

typeSelect.addEventListener('change', toggleCreditLimit);