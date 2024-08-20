function setRequired(...fields) {
    document.getElementById('phoneNumberMessage').removeAttribute('required');
    document.getElementById('phoneMessage').removeAttribute('required');
    document.getElementById('phoneNumberFile').removeAttribute('required');
    document.getElementById('fileUrl').removeAttribute('required');
    document.getElementById('fileName').removeAttribute('required');

    fields.forEach(function(fieldId) {
        document.getElementById(fieldId).setAttribute('required', 'required');
    });
}
