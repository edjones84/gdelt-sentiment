const form = document.getElementById('queryForm');
const queryInput = document.getElementById('queryInput');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const query = queryInput.value;

    try {
        const response = await fetch(`http://localhost:8000/endpoint?queryInput=${encodeURIComponent(query)}`);
        const data = await response.json();

        console.log('Response Data:', data); // Log the response data for debugging purposes

        resultDiv.innerHTML = '';

        if (Array.isArray(data.scores)) {
            if (data.scores.length > 0) {
                data.scores.forEach(item => {
                    const p = document.createElement('p');
                    p.textContent = `Title: ${item.title}, Compound Score: ${item.compound}`;
                    resultDiv.appendChild(p);
                });
            } else {
                const p = document.createElement('p');
                p.textContent = 'No results found.';
                resultDiv.appendChild(p);
            }
        } else {
            const p = document.createElement('p');
            p.textContent = 'Invalid response format.';
            resultDiv.appendChild(p);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});