// Funciones para product_detail.html

// Manejo de eventos para incrementar la cantidad
$(document).on('click', '.increment-qty', function (e) {
    e.preventDefault();
    var inputField = $(this).siblings('.qty_input');
    var currentValue = parseInt(inputField.val());

    if (currentValue < 99) {
        var newQuantity = currentValue + 1;
        inputField.val(newQuantity);
    }
});

// Manejo de eventos para decrementar la cantidad
$(document).on('click', '.decrement-qty', function (e) {
    e.preventDefault();
    var inputField = $(this).siblings('.qty_input');
    var currentValue = parseInt(inputField.val());

    if (currentValue > 1) {
        var newQuantity = currentValue - 1;
        inputField.val(newQuantity);
    }
});

// Manejo de eventos para agregar al carrito desde la página de detalles del producto
$(document).on('click', '#add-to-cart-btn', function (e) {
    e.preventDefault();
    var itemId = $('#add-to-cart-form').find('.qty_input').data('item_id');
    var quantity = $('#add-to-cart-form').find('.qty_input').val();

    // Realiza una solicitud AJAX para agregar el producto al carrito.
    // Ajusta la URL y los datos según tu aplicación.
    $.ajax({
        type: 'POST',
        url: '/cart_add/' + itemId + '/',
        data: {
            quantity: quantity,
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function (response) {
            // Maneja la respuesta del servidor si es necesario
            console.log(response);
        },
        error: function (error) {
            console.error('Error al agregar el artículo al carrito', error);
        }
    });
});

/***********CART SUMMARY */
$(document).on('click', '.update-cart', function(e){
    e.preventDefault();
    // grab the product id
    var productid = $(this).data('index');

    $.ajax({
    type: 'POST',
    url: '{% url "cart_update" %}',
    data: {
      product_id: $(this).data('index'),
      product_qty: $('#select' + productid + ' option:selected').text(),
      csrfmiddlewaretoken: '{{ csrf_token }}',
      action: 'post'
    },
    success: function(json){
        
        location.reload();
    },

    error: function(xhr, errmsg, err){

    }


    });

})

// Delete Item From Cart

$(document).ready(function() {
    $('.remove-item-btn').click(function(e) {
        e.preventDefault();
        var itemId = $(this).data('item_id');
        console.log("Intentando eliminar el ítem con ID:", itemId); // Depuración: Imprime el ID del ítem a eliminar

        var url = `/cart/remove/${itemId}/`; // Asegúrate de que esta URL sea correcta
        var csrfToken = getCookie('csrftoken'); // Función para obtener el token CSRF

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'item_id': itemId
            },
            success: function(response) {
                console.log("Respuesta del servidor:", response); // Depuración: Imprime la respuesta del servidor
                if(response.deleted){
                    // Elimina la fila del ítem de la tabla
                    $(`#item-row-${itemId}`).remove();
                    // Actualiza información como el total, etc.
                    console.log("Ítem eliminado del DOM con ID:", itemId); // Depuración: Confirma la eliminación en el DOM
                }
            },
            error: function(xhr, status, error) {
                // Manejo de errores
                console.error("Error en la solicitud AJAX:", status, error);
            }
        });
    });
});

// Función para obtener el valor de una cookie por nombre
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



//Update

