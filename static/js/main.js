document.getElementById('predictionForm').onsubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    
    // Check all inputs for validity
    const inputs = form.querySelectorAll('input, select');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.checkValidity()) {
            isValid = false;
            input.classList.add('invalid');
            const event = new Event('input');
            input.dispatchEvent(event);
        }
    });
    
    if (!isValid) {
        return;
    }
    
    // Continue with existing submission code
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.querySelector('.loading');
    
    // Reset and show loading
    resultDiv.className = 'result';
    resultDiv.innerHTML = '';
    loadingDiv.style.display = 'block';
    
    try {
        const formData = new FormData(form);
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        handlePredictionResponse(data, resultDiv, loadingDiv);
    } catch (error) {
        handleError(resultDiv, loadingDiv);
    }
};

function handlePredictionResponse(data, resultDiv, loadingDiv) {
    loadingDiv.style.display = 'none';
    
    if (data.success) {
        resultDiv.className = `result show ${data.prediction.toLowerCase().replace(' ', '-')}`;
        resultDiv.innerHTML = `
            <div class="prediction-result">
                <h3>Prediction Result</h3>
                <p class="prediction ${data.prediction.toLowerCase()}">${data.prediction}</p>
                <p class="confidence">Confidence: ${data.confidence}%</p>
                <div class="summary">
                    <h4>Summary</h4>
                    <p>Total Claim: $${data.summary.total_claim.toLocaleString()}</p>
                    <p>Severity: ${data.summary.severity}</p>
                    <p>Witnesses: ${data.summary.witnesses}</p>
                </div>
                <div class="risk-factors">
                    <h4>Risk Factors</h4>
                    <ul>
                        ${data.risk_factors.high_claim_amount ? '<li>High Claim Amount</li>' : ''}
                        ${data.risk_factors.multiple_vehicles ? '<li>Multiple Vehicles</li>' : ''}
                        ${data.risk_factors.bodily_injuries ? '<li>Bodily Injuries</li>' : ''}
                    </ul>
                </div>
                <p class="timestamp">Prediction made at: ${data.timestamp}</p>
            </div>
        `;
    } else {
        resultDiv.className = 'result show error';
        resultDiv.innerHTML = `Error: ${data.error}`;
    }
    
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

function handleError(resultDiv, loadingDiv) {
    loadingDiv.style.display = 'none';
    resultDiv.className = 'result show error';
    resultDiv.innerHTML = 'Error making prediction';
}

// Form validation and tooltips
function initializeForm() {
    document.querySelectorAll('.form-group').forEach((group, index) => {
        group.classList.add('animate__animated', 'animate__fadeInLeft');
        group.style.animationDelay = `${index * 0.1}s`;
    });

    initializeTooltips();
    initializeValidation();
    initializeProgressBar();
}

function initializeTooltips() {
    document.querySelectorAll('.tooltip-icon').forEach(icon => {
        icon.addEventListener('mouseenter', (e) => {
            const tooltip = e.target.nextElementSibling;
            tooltip.style.visibility = 'visible';
            tooltip.style.opacity = '1';
        });
        
        icon.addEventListener('mouseleave', (e) => {
            const tooltip = e.target.nextElementSibling;
            tooltip.style.visibility = 'hidden';
            tooltip.style.opacity = '0';
        });
    });
}

function initializeValidation() {
    document.querySelectorAll('input, select').forEach(input => {
        input.addEventListener('change', updateProgress);
        input.addEventListener('input', validateInput);
    });
}

function initializeProgressBar() {
    updateProgress();
    window.addEventListener('scroll', updateProgressBarPosition);
}

function updateProgress() {
    const form = document.getElementById('predictionForm');
    const inputs = form.querySelectorAll('input, select');
    const filled = Array.from(inputs).filter(input => input.value).length;
    const progress = (filled / inputs.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
}

function validateInput(e) {
    const input = e.target;
    
    // Skip validation for select elements
    if (input.tagName.toLowerCase() === 'select') {
        input.classList.remove('invalid');
        input.setCustomValidity('');
        const tooltip = input.parentElement.querySelector('.validation-tooltip');
        if (tooltip) tooltip.remove();
        return;
    }
    
    // Only validate number inputs
    if (input.type === 'number') {
        const value = parseFloat(input.value);
        const min = parseFloat(input.getAttribute('min'));
        const max = parseFloat(input.getAttribute('max'));
        const step = parseFloat(input.getAttribute('step')) || 1;
        
        let isValid = true;
        let errorMessage = '';

        // Check if value is a number
        if (isNaN(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid number';
        }
        // Check min/max constraints
        else if (min !== null && value < min) {
            isValid = false;
            errorMessage = `Minimum value is ${min}`;
        }
        else if (max !== null && value > max) {
            isValid = false;
            errorMessage = `Maximum value is ${max}`;
        }
        // Check step constraints
        else if (step && (value % step !== 0)) {
            isValid = false;
            errorMessage = `Please enter in increments of ${step}`;
        }

        // Update UI to show validation state
        input.classList.toggle('invalid', !isValid);
        input.setCustomValidity(errorMessage);
        
        // Update tooltip with error message
        const tooltip = input.parentElement.querySelector('.validation-tooltip');
        if (!isValid) {
            if (!tooltip) {
                const newTooltip = document.createElement('div');
                newTooltip.className = 'validation-tooltip';
                newTooltip.textContent = errorMessage;
                input.parentElement.appendChild(newTooltip);
            } else {
                tooltip.textContent = errorMessage;
            }
        } else if (tooltip) {
            tooltip.remove();
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeForm);
