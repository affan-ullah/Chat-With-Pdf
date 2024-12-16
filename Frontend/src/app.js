document.addEventListener('DOMContentLoaded', function() {

    // File Upload Handling
    document.getElementById('uploadBtn').addEventListener('click', function() {
        const files = document.getElementById('pdfInput').files;
        if (files.length === 0) {
            alert('Please select at least one PDF file.');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('pdfs', files[i]);
        }

        fetch('http://localhost:5000/ingest', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error during file upload:', error);
            alert('Error uploading files.');
        });
    });

    // Query Handling
    document.getElementById('queryBtn').addEventListener('click', function() {
        const query = document.getElementById('queryInput').value.trim();
        if (!query) {
            alert('Please enter a query.');
            return;
        }

        fetch('http://localhost:5000/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('responseOutput').innerHTML = `<strong>Response:</strong><br>${data.response}`;
        })
        .catch(error => {
            console.error('Error during query submission:', error);
            alert('Error submitting query.');
        });
    });

    // Comparison Handling
    document.getElementById('compareBtn').addEventListener('click', function() {
        const compareQuery = document.getElementById('compareInput').value.trim();
        if (!compareQuery) {
            alert('Please enter a comparison query.');
            return;
        }

        fetch('http://localhost:5000/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: compareQuery })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('comparisonOutput').innerHTML = `<strong>Comparison Results:</strong><br>${JSON.stringify(data.comparison, null, 2)}`;
        })
        .catch(error => {
            console.error('Error during comparison submission:', error);
            alert('Error submitting comparison query.');
        });
    });

});
