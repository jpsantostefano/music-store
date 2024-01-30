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

// Remove item and reload on click
$('.remove-item').click(function(e) {
    var csrfToken = "{{ csrf_token }}";
    var itemId = $(this).attr('id').split('remove_')[1];
    var url = `/cart/remove/${itemId}/`;
    var data = {'csrfmiddlewaretoken': csrfToken};

    $.post(url, data)
     .done(function() {
         location.reload();
     });
})


//Update
$('.update-link').click(function(e)) {
    var form = $(this).prev('update-form');
    form.submit();
}

