function showProgress() {
    var progressContainer = document.getElementById('progress-container');
    var progressBarFill = document.querySelector('.progress-bar-fill');

    progressContainer.style.display = 'block';

    var width = 0;
    var interval = setInterval(function() {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            progressBarFill.style.width = width + '%';
            progressBarFill.innerHTML = width + '%';
        }
    }, 50);
}
