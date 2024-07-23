

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    $('.addtocartbtn').click(function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.productData').find(".productid").val();
        console.log(product_id)
        var size = $(this).closest('.productData').find("#size").val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'size': size,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response.status)
                Swal.fire({
                    title: 'Success',
                    text: response.status,
                    icon: 'success',
                    timer: 1000,
                    showConfirmButton: false,
                });
            },
            error: function (xhr) {
                let response = xhr.responseJSON;
                console.log(response.status)
                Swal.fire({
                    title: 'Error',
                    text: response.status,
                    icon: 'error',
                    timer: 1000,
                    showConfirmButton: false,
                });
            }
        });

    });

    $('.addtowishlistbtn').click(function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.productData').find('.productid').val();
        console.log(product_id)
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response.status)
                Swal.fire({
                    title: 'Wishlist Status',
                    text: response.status,
                    icon: 'success',
                    timer: 1000,
                    showConfirmButton: false
                });
            },
            error: function (xhr) {
                let response = xhr.responseJSON;
                console.log(response.status)
                Swal.fire({
                    title: 'Error',
                    text: response.status,
                    icon: 'error',
                    timer: 1000,
                    showConfirmButton: false,
                });
            }
        });


    });

    $('.removewishlistbtn').click(function (e) {
        e.preventDefault();
        var product_id = $(this).siblings('.productid').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: "/delete-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response.status)
                Swal.fire({
                    title: 'Wishlist Status',
                    text: response.status,
                    icon: 'success',
                    timer: 1000,
                    showConfirmButton: false
                });
                $('.wishlistData').load(location.href + " .wishlistData")
            }
        });


    });

    $(document).on('click', '.addAddressbtn', function (e) {
        e.preventDefault();
        var formData = $('#addAddressForm').serialize();
        $.ajax({
            method: "POST",
            url: $('#addAddressForm').attr('action'),
            data: formData,
            success: function (response) {
                if (response.status === "Address added successfully") {
                    console.log(response.status)
                    $('#addAddressForm')[0].reset();

                    // Reset validation states
                    $('.invalid-feedback').text('');
                    $('.form-control').removeClass('is-invalid');
                    //Hide Modal and remove modal backdrop
                    $('#addAddressModal').modal('hide');
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();

                    Swal.fire({
                        title: 'Address Status',
                        text: response.status,
                        icon: 'success',
                        timer: 1000,
                        showConfirmButton: false
                    });
                    $('.addressData').load(location.href + " .addressData")            // Optionally reload the page or update the address list dynamically
                } else {
                    // Display errors
                    console.log("error from ajax")
                    $('.invalid-feedback').text('');  // Clear previous errors
                    $('.form-control').removeClass('is-invalid');  // Clear previous invalid classes
                    for (var field in response.errors) {
                        $('#' + field + '_error').text(response.errors[field][0]);
                        $('#' + field).addClass('is-invalid');
                    }
                }
            },
            error: function (response) {
                console.log("Error:", response);
            }

        });

    });

    $(document).on('click', '.removeAddressbtn', function (e) {
        e.preventDefault();
        var address_id = $(this).siblings('.addressid').val();
        console.log(address_id)
        var token = $('input[name=csrfmiddlewaretoken]').val();
        Swal.fire({
            title: 'Are you sure?',
            text: "Do you really want to Remove this Address?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Confirm'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "POST",
                    url: "/delete-address",
                    data: {
                        'address_id': address_id,
                        csrfmiddlewaretoken: token
                    },
                    success: function (response) {
                        Swal.fire({
                            title: 'Address Removed',
                            text: response.status,
                            icon: 'success',
                            timer: 1000,
                            showConfirmButton: false
                        });
                        $('.addresstab').load(location.href + " .addresstab")
                    }
                });
            }
        });

    });

    $('.edituserbutton').click(function (e) {
        e.preventDefault();
        // Clear previous error messages
        $('.error-message').text('');
        $('.form-control').removeClass('is-invalid');

        $.ajax({
            type: 'POST',
            url: $('#editProfileForm').attr('action'),  // Update with the correct URL
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'username': $('#username').val().trim(),
                'first_name': $('#firstname').val().trim(),
                'last_name': $('#lastname').val().trim(),
                'email': $('#email').val().trim(),
                'phone_number': $('#phone_number').val().trim()
            },
            success: function (response) {
                Swal.fire({
                    title: 'Profile Status',
                    text: 'Profile updated successfully!',
                    icon: 'success',
                    timer: 1000,
                    showConfirmButton: false,
                });
                $('.userData').load(location.href + " .userData")
                $('#editProfileModal').modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
            },
            error: function (response) {
                if (response.responseJSON && response.responseJSON.errors) {
                    const errors = response.responseJSON.errors;
                    for (let field in errors) {
                        $('#' + field + '_error').text(errors[field]);
                        $('#' + field).addClass('is-invalid');
                    }
                } else {
                    Swal.fire({
                        title: 'Error',
                        text: 'An error occurred. Please try again.',
                        icon: 'error',
                        timer: 2000,
                        showConfirmButton: false,
                    });
                }
            }
        });
    });

    $('.changepasswordbtn').click(function (e) {
        e.preventDefault();
        console.log($('#changePasswordForm').attr('action'))
        $('.error-message').text('');
        $('.form-control').removeClass('is-invalid');
        $.ajax({
            type: 'POST',
            url: $('#changePasswordForm').attr('action'), // URL for the form action
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'old_password': $('#old_password').val().trim(),
                'new_password1': $('#new_password1').val().trim(),
                'new_password2': $('#new_password2').val().trim()
            },
            success: function (response) {
                Swal.fire({
                    title: 'Password Change',
                    text: response.message,
                    icon: 'success',
                    timer: 1000,
                    showConfirmButton: false,
                });
                $('#changePasswordModal').modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
            },
            error: function (response) {
                if (response.responseJSON && response.responseJSON.errors) {
                    const errors = response.responseJSON.errors;
                    for (let field in errors) {
                        $('#' + field + '_error').text(errors[field]);
                        $('#' + field).addClass('is-invalid');
                    }
                } else {
                    Swal.fire({
                        title: 'Error',
                        text: 'An error occurred. Please try again.',
                        icon: 'error',
                        timer: 1000,
                        showConfirmButton: false,
                    });
                }
            }
        });


    });

    $(document).on('click', '.editAddressbtn', function (e) {
        e.preventDefault();
        var addressCard = $(this).closest('.addressData');
        var addressId = addressCard.find('.addressid').val();
        var addressText = addressCard.find('.card-text').text().split(',');

        $('#editAddressModal #edit_address_id').val(addressId);
        $('#editAddressModal #edit_house_no').val(addressText[0].trim());
        $('#editAddressModal #edit_street').val(addressText[1].trim());
        $('#editAddressModal #edit_landmark').val(addressText[2].trim());
        $('#editAddressModal #edit_city').val(addressText[3].trim());
        $('#editAddressModal #edit_pincode').val(addressText[4].trim());

        if (addressCard.find('.text-success').length > 0) {
            $('#editAddressModal #edit_primary_yes').prop('checked', true);
        } else {
            $('#editAddressModal #edit_primary_no').prop('checked', false);
        }

        $('#editAddressModal').modal('show');
    });

    $(document).on('click', '.cancelproductbtn', function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.orderData').find('.product_id').val();
        var order_id = $(this).closest('.orderData').find('.order_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        Swal.fire({
            title: 'Are you sure?',
            text: "Do you really want to cancel this product?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, cancel it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "POST",
                    url: "/cancel-product",
                    data: {
                        'order_id': order_id,
                        'product_id': product_id,
                        csrfmiddlewaretoken: token
                    },
                    success: function (response) {
                        Swal.fire({
                            title: 'Product Status',
                            text: response.status,
                            icon: 'success',
                            timer: 1000,
                            showConfirmButton: false
                        });
                        $('.orderproducttab').load(location.href + " .orderproducttab");

                    }
                });
            }
        });
    });
    $(document).on('click', '.returnproductbtn', function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.orderData').find('.product_id').val();
        var order_id = $(this).closest('.orderData').find('.order_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        Swal.fire({
            title: 'Are you sure?',
            text: "Do you really want to Return this product?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Confirm'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "POST",
                    url: "/return-product",
                    data: {
                        'order_id': order_id,
                        'product_id': product_id,
                        csrfmiddlewaretoken: token
                    },
                    success: function (response) {
                        Swal.fire({
                            title: 'Product Status',
                            text: response.status,
                            icon: 'success',
                            timer: 1000,
                            showConfirmButton: false
                        });
                        $('.orderproducttab').load(location.href + " .orderproducttab");

                    }
                });
            }
        });
    });


    $(document).on('click', '.ordercancelbtn', function (e) {
        e.preventDefault();
        var order_id = $(this).closest('.orderdetailtab').find('.order_id').val();
        console.log(order_id)
        var token = $('input[name=csrfmiddlewaretoken]').val();
        Swal.fire({
            title: 'Are you sure?',
            text: "Do you really want to cancel this Order? Note: All the items associated with this order will also get Cancelled",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, cancel it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "POST",
                    url: "/cancel-order",
                    data: {
                        'order_id': order_id,
                        csrfmiddlewaretoken: token
                    },
                    success: function (response) {
                        Swal.fire({
                            title: 'Order Status Updation',
                            text: response.status,
                            icon: 'success',
                            timer: 1000,
                            showConfirmButton: false
                        });
                        var orderCard = $('.orderdetailtab').filter(function () {
                            return $(this).find('.order_id').val() == order_id;
                        });

                        orderCard.find('.ordercancelbtn').remove();
                        orderCard.find('.orderdetailcontent h5 span')
                            .removeClass('text-primary')
                            .addClass('text-danger')
                            .text('Cancelled');
                    }
                });
            }
        });

    });

    const totalPrice = parseFloat($("#totalprice-data").data("totalprice"));
    $('.applycouponbutton').on('click', function (e) {
        e.preventDefault();
        console.log("Apply Coupon clicked")
        var applycouponurl = $('#apply-coupon-url').data('url');
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

        var coupon_code = $('#coupon_code').val();
        $.ajax({
            url: applycouponurl,
            method: "POST",
            data: {
                'coupon_code': coupon_code,
                'total_price': totalPrice,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (response) {
                if (response.status === 'success') {
                    $('#discount').text(response.discount + '%');
                    $('#total').text('$' + response.discounted_price.toFixed(2));
                    $('#total_price').val(response.discounted_price.toFixed(2));
                    $('#coupon_error').text('');
                    $('#applied_coupon_container').html(`
                        <div class="card applied-coupon-card">
                            <div class="card-body">
                                <h6 class="card-title">Applied Coupon: ${response.coupon_code}</h6>
                                <p class="card-text">Discount: ${response.discount}%</p>
                                <button type="button" class="btn btn-danger btn-sm" id="remove_coupon">Remove Coupon</button>
                            </div>
                        </div>
                    `);
                } else {
                    $('#coupon_error').text(response.message);
                }
            }
        });
    });

    $(document).on('click', '#remove_coupon', function () {
        $('#discount').text('0%');
        $('#applied_coupon_container').html('');
        $('#total').text('$' + totalPrice.toFixed(2));
        $('#total_price').val(totalPrice.toFixed(2));
        $('#coupon_error').text('');
    });

    $('.razorpaybutton').click(function (e) {
        e.preventDefault();
        var address = $("input[name='selected_address']:checked").val();
        var first_name = $("input[name='first_name']").val();
        var last_name = $("input[name='last_name']").val();
        var email = $("input[name='email']").val();
        var phone = $("input[name='phone']").val();
        var total_price = $("input[name='total_price']").val();
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        if (!address) {
            Swal.fire({ icon: 'error', text: "Please Select the Delivery Address", timer: 1000 })
        }
        else {
            console.log(total_price)
            var options = {
                "key": "rzp_test_poghBnnNNEGliw", // Enter the Key ID generated from the Dashboard
                "amount": 1 * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Eleganza Vogue", //your business name
                "description": "Thank you for Shopping with us",
                "image": "https://example.com/your_logo",
                // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (responseid) {
                    $.ajax({
                        type: "POST",
                        url: "/place-order",
                        data: {
                            'selected_address': address,
                            'payment_method': "RazorPay",
                            'payment_id': responseid.razorpay_payment_id,
                            'total_price': total_price,
                            csrfmiddlewaretoken: csrftoken
                        },
                        success: function (successresponse) {
                            Swal.fire({
                                title: 'Order Status',
                                text: successresponse.status,
                                icon: 'success',
                                showConfirmButton: true
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.href = '/userdetail'; // Change this to the correct URL for the user profile
                                }
                            });;

                        }
                    });
                },
                "prefill": { 
                    "name": '',
                    "email": '',
                    "contact":''  
                },
                "method":{
                    'upi':true
                },
                "theme": {
                    "color": "#3399cc"
                }
            };
            var rzp1 = new Razorpay(options);
            rzp1.open();
        }
    });





    //Search Switch
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });

    /*------------------
        Navigation
    --------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Accordin Active
    --------------------*/
    $('.collapse').on('shown.bs.collapse', function () {
        $(this).prev().addClass('active');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).prev().removeClass('active');
    });

    //Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("active");
        $(".offcanvas-menu-overlay").addClass("active");
    });

    $(".offcanvas-menu-overlay").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("active");
        $(".offcanvas-menu-overlay").removeClass("active");
    });

    /*-----------------------
        Hero Slider
    ------------------------*/
    $(".hero__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='arrow_left'><span/>", "<span class='arrow_right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        autoplayTimeout: 5000
    });

    /*--------------------------
        Select
    ----------------------------*/
    // $("select").niceSelect();

    /*-------------------
        Radio Btn
    --------------------- */
    $(".product__color__select label, .shop__sidebar__size label, .product__details__option__size label").on('click', function () {
        $(".product__color__select label, .shop__sidebar__size label, .product__details__option__size label").removeClass('active');
        $(this).addClass('active');
    });

    /*-------------------
        Scroll
    --------------------- */
    $(".nice-scroll").niceScroll({
        cursorcolor: "#0d0d0d",
        cursorwidth: "5px",
        background: "#e5e5e5",
        cursorborder: "",
        autohidemode: true,
        horizrailenabled: false
    });

    /*------------------
        CountDown
    --------------------*/
    // For demo preview start

    /*------------------
        Magnific
    --------------------*/

    /*-------------------
        Quantity change
    --------------------- */

    /*------------------
        Achieve Counter
    --------------------*/
    $('.cn_num').each(function () {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 4000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });



})(jQuery);

function showSection(sectionId) {
    document.querySelectorAll('.btn-option').forEach(button => {
        button.classList.remove('selected');
    });
    document.getElementById(`btn-${sectionId}`).classList.add('selected');

    let productTags = {
        'best-sellers': ['Sale', 'Hot', 'Limited'],
        'new-arrivals': ['New', 'Trending', 'Exclusive']
    };

    document.querySelectorAll('.product-card .badge').forEach((badge, index) => {
        badge.textContent = productTags[sectionId][index % productTags[sectionId].length];
        if (sectionId === 'best-sellers') {
            badge.classList.remove('badge-secondary');
            badge.classList.add('badge-danger');
        } else {
            badge.classList.remove('badge-danger');
            badge.classList.add('badge-secondary');
        }
    });
}


