// JavaScript function to update the slider value display

function updateSliderValue(sliderId, displayId) {
    // Get the slider element and its associated display span
    const slider = document.getElementById(sliderId);
    const display = document.getElementById(displayId);
    
    // Update the span's content to match the slider's current value
    if (slider && display) {
        display.textContent = slider.value;
    }
}

