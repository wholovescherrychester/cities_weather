// Плэйсхолдер для инпутов
const FormInput = document.querySelectorAll(".form__input");

FormInput.forEach(el => showPlaceholder(el));


function showPlaceholder(el) {
    attr = el.getAttribute('placeholder')

    el.addEventListener("focus",() => {
        el.setAttribute("placeholder","");
    })
    
    el.addEventListener("blur",() => {
        el.setAttribute("placeholder",attr);
    })

}


// Выбор двух городов
function checkMinCities(event) {
    const cityInputs = document.querySelectorAll('.home-form-box .form__input');
    const filledCities = Array.from(cityInputs).filter(input => input.value.trim() !== '');

    if (filledCities.length < 2) {
            alert('Нужно выбрать 2 города!');
            event.preventDefault();
        }
    return true;
}