function setCityValue(element, side) {
    const cityName = element.textContent;
    
    const input = document.querySelector(`.distance-form__${side}-wrapper .form__input`);
    
    input.value = cityName;
    
    if (side === 'left') {
        const from_input = document.getElementById('from-city-slug');
        from_input.value = cityName;
    } else if (side === 'right') {
        const to_input = document.getElementById('to-city-slug');
        to_input.value = cityName;
    }

    
    const list = element.parentElement;
    list.style.display = 'none';
}