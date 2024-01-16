function handleEnableDisable(itemId) {
    var currentValue = parseInt($(`.id_qty_${itemId}`).val());
    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 98;

    $(`.decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`.increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

function updateQuantity(itemId, newQuantity) {
    $.ajax({
        type: 'POST',
        url: '/update_quantity/',  // Reemplaza con la URL correcta en tu aplicación
        data: {
            item_id: itemId,
            quantity: newQuantity,
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function (response) {
            // Maneja la respuesta del servidor si es necesario
            console.log(response);
        },
        error: function (error) {
            console.error('Error al actualizar la cantidad', error);
        }
    });
}

// Ensure proper enabling/disabling of all inputs on page load
var allQtyInputs = $('.qty_input');
for (var i = 0; i < allQtyInputs.length; i++) {
    var itemId = $(allQtyInputs[i]).data('item_id');
    handleEnableDisable(itemId);
}

// Check enable/disable every time the input is changed
$('.qty_input').change(function () {
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
});

// Increment quantity on plus button click
$(document).on('click', '.increment-qty', function (e) {
    e.preventDefault();
    var itemId = $(this).data('item_id');
    var inputField = $(`.qty_input.id_qty_${itemId}`);
    var currentValue = parseInt(inputField.val());

    if (currentValue < 99) {
        var newQuantity = currentValue + 1;
        inputField.val(newQuantity);
        handleEnableDisable(itemId);
        updateQuantity(itemId, newQuantity);
    }
});

// Decrement quantity on minus button click
$(document).on('click', '.decrement-qty', function (e) {
    e.preventDefault();
    var itemId = $(this).data('item_id');
    var inputField = $(`.qty_input.id_qty_${itemId}`);
    var currentValue = parseInt(inputField.val());

    if (currentValue > 1) {
        var newQuantity = currentValue - 1;
        inputField.val(newQuantity);
        handleEnableDisable(itemId);
        updateQuantity(itemId, newQuantity);
    }
});