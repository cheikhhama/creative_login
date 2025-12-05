document.addEventListener('DOMContentLoaded', () => {
    const coins = document.querySelectorAll('.coin-card');
    const patternDisplay = document.getElementById('pattern-display');
    const totalDisplay = document.getElementById('pattern-total');
    const inputPattern = document.getElementById('input-pattern');
    const inputTotal = document.getElementById('input-total');
    const currencyDisplay = document.getElementById('currency-display');

    let pattern = [];
    let total = 0;

    coins.forEach(coin => {
        coin.addEventListener('click', () => {
            const value = parseInt(coin.dataset.value);
            pattern.push(value);
            total += value;

            patternDisplay.textContent = pattern.join(', ');
            totalDisplay.textContent = total;

            inputPattern.value = pattern.join(',');
            inputTotal.value = total;
        });
    });

    // update currency display if signup
    const currencySelect = document.getElementById('id_currency');
    if(currencySelect){
        currencySelect.addEventListener('change', (e)=>{
            currencyDisplay.textContent = e.target.value;
        });
        currencyDisplay.textContent = currencySelect.value;
    }
});
