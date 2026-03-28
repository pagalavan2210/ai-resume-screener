const fileInput = document.querySelector('input[type="file"]');
if (fileInput) {
    fileInput.addEventListener('change', function () {
        const label = this.nextElementSibling;
        if (label) label.textContent = this.files[0]?.name || 'Choose file';
    });
}
```

**`requirements.txt`:**
```
flask
spacy
PyMuPDF
scikit-learn