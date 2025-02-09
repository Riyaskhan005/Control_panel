function showAlert(message, type) {
    var alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    var icon = type === 'success' ? '<i class="ti ti-check"></i>' : '<i class="ti ti-alert-octagon"></i>';
    var alertText = $('<div class="alert ' + alertClass + '" role="alert">' + icon + ' ' + message + '</div>');

    $('body').append(alertText);
    alertText.css({
        position: 'fixed',
        top: '20px',
        right: '20px',
        zIndex: 9999
    });

    setTimeout(function() {
        alertText.fadeOut(function() {
            $(this).remove();
        });
    }, 3000);
}