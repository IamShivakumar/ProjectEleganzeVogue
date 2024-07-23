/*
Author       : Dreamguys
Template Name: PreClinic - Medical and Hospital Admin Template
Version      : 1.0
*/
$(document).ready(function ($) {

	// Variables declarations
	var $wrapper = $('.main-wrapper');
	var $pageWrapper = $('.page-wrapper');
	var $slimScrolls = $('.slimscroll');
	var $sidebarOverlay = $('.sidebar-overlay');

	// Sidebar
	var Sidemenu = function () {
		this.$menuItem = $('#sidebar-menu a');
	};



	function init() {
		var $this = Sidemenu;
		$('#sidebar-menu a').on('click', function (e) {
			if ($(this).parent().hasClass('submenu')) {
				e.preventDefault();
			}
			if (!$(this).hasClass('subdrop')) {
				$('ul', $(this).parents('ul:first')).slideUp(350);
				$('a', $(this).parents('ul:first')).removeClass('subdrop');
				$(this).next('ul').slideDown(350);
				$(this).addClass('subdrop');
			} else if ($(this).hasClass('subdrop')) {
				$(this).removeClass('subdrop');
				$(this).next('ul').slideUp(350);
			}
		});
		$('#sidebar-menu ul li.submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
	}
	// Sidebar Initiate
	init();

	// Sidebar overlay
	function sidebar_overlay($target) {
		if ($target.length) {
			$target.toggleClass('opened');
			$sidebarOverlay.toggleClass('opened');
			$('html').toggleClass('menu-opened');
			$sidebarOverlay.attr('data-reff', '#' + $target[0].id);
		}
	}

	// Mobile menu sidebar overlay
	$(document).on('click', '#mobile_btn', function () {
		var $target = $($(this).attr('href'));
		sidebar_overlay($target);
		$wrapper.toggleClass('slide-nav');
		$('#chat_sidebar').removeClass('opened');
		return false;
	});

	// Chat sidebar overlay
	$(document).on('click', '#task_chat', function () {
		var $target = $($(this).attr('href'));
		console.log($target);
		sidebar_overlay($target);
		return false;
	});

	// Sidebar overlay reset
	$sidebarOverlay.on('click', function () {
		var $target = $($(this).attr('data-reff'));
		if ($target.length) {
			$target.removeClass('opened');
			$('html').removeClass('menu-opened');
			$(this).removeClass('opened');
			$wrapper.removeClass('slide-nav');
		}
		return false;
	});

	// Select 2
	if ($('.select').length > 0) {
		$('.select').select2({
			minimumResultsForSearch: -1,
			width: '100%'
		});
	}

	// Floating Label
	if ($('.floating').length > 0) {
		$('.floating').on('focus blur', function (e) {
			$(this).parents('.form-focus').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
		}).trigger('blur');
	}

	// Right Sidebar Scroll
	if ($('#msg_list').length > 0) {
		$('#msg_list').slimscroll({
			height: '100%',
			color: '#878787',
			disableFadeOut: true,
			borderRadius: 0,
			size: '4px',
			alwaysVisible: false,
			touchScrollStep: 100
		});
		var msgHeight = $(window).height() - 124;
		$('#msg_list').height(msgHeight);
		$('.msg-sidebar .slimScrollDiv').height(msgHeight);
		$(window).resize(function () {
			var msgrHeight = $(window).height() - 124;
			$('#msg_list').height(msgrHeight);
			$('.msg-sidebar .slimScrollDiv').height(msgrHeight);
		});
	}

	// Left Sidebar Scroll
	if ($slimScrolls.length > 0) {
		$slimScrolls.slimScroll({
			height: 'auto',
			width: '100%',
			position: 'right',
			size: '7px',
			color: '#ccc',
			wheelStep: 10,
			touchScrollStep: 100
		});
		var wHeight = $(window).height() - 60;
		$slimScrolls.height(wHeight);
		$('.sidebar .slimScrollDiv').height(wHeight);
		$(window).resize(function () {
			var rHeight = $(window).height() - 60;
			$slimScrolls.height(rHeight);
			$('.sidebar .slimScrollDiv').height(rHeight);
		});
	}

	// Page wrapper height
	var pHeight = $(window).height();
	$pageWrapper.css('min-height', pHeight);
	$(window).resize(function () {
		var prHeight = $(window).height();
		$pageWrapper.css('min-height', prHeight);
	});

	// Datetimepicker
	if ($('.datetimepicker').length > 0) {
		$('.datetimepicker').datetimepicker({
			format: 'DD/MM/YYYY'
		});
	}

	// Datatable
	if ($('.datatable').length > 0) {
		$('.datatable').DataTable({
			"bFilter": false,
		});
	}

	// Bootstrap Tooltip
	if ($('[data-toggle="tooltip"]').length > 0) {
		$('[data-toggle="tooltip"]').tooltip();
	}

	// Mobile Menu
	$(document).on('click', '#open_msg_box', function () {
		$wrapper.toggleClass('open-msg-box');
		return false;
	});

	// Lightgallery
	if ($('#lightgallery').length > 0) {
		$('#lightgallery').lightGallery({
			thumbnail: true,
			selector: 'a'
		});
	}

	// Incoming call popup


	// Summernote
	if ($('.summernote').length > 0) {
		$('.summernote').summernote({
			height: 200,
			minHeight: null,
			maxHeight: null,
			focus: false
		});
	}

	// Check all email

	// Dropfiles
	if ($('#drop-zone').length > 0) {
		var dropZone = document.getElementById('drop-zone');
		var uploadForm = document.getElementById('js-upload-form');
		var startUpload = function (files) {
			console.log(files);
		};
		uploadForm.addEventListener('submit', function (e) {
			var uploadFiles = document.getElementById('js-upload-files').files;
			e.preventDefault();
			startUpload(uploadFiles);
		});
		dropZone.ondrop = function (e) {
			e.preventDefault();
			this.className = 'upload-drop-zone';
			startUpload(e.dataTransfer.files);
		};
		dropZone.ondragover = function () {
			this.className = 'upload-drop-zone drop';
			return false;
		};
		dropZone.ondragleave = function () {
			this.className = 'upload-drop-zone';
			return false;
		};
	}

	// Small Sidebar
	if (screen.width >= 992) {
		$(document).on('click', '#toggle_btn', function () {
			if ($('body').hasClass('mini-sidebar')) {
				$('body').removeClass('mini-sidebar');
				$('.subdrop + ul').slideDown();
			} else {
				$('body').addClass('mini-sidebar');
				$('.subdrop + ul').slideUp();
			}
			return false;
		});
		$(document).on('mouseover', function (e) {
			e.stopPropagation();
			if ($('body').hasClass('mini-sidebar') && $('#toggle_btn').is(':visible')) {
				var targ = $(e.target).closest('.sidebar').length;
				if (targ) {
					$('body').addClass('expand-menu');
					$('.subdrop + ul').slideDown();
				} else {
					$('body').removeClass('expand-menu');
					$('.subdrop + ul').slideUp();
				}
				return false;
			}
		});
	}

	$('#addCouponForm').on('submit', function (e) {
		e.preventDefault();
		var formData = $('#addCouponForm').serialize();
		$.ajax({
			method: "POST",
			url: $('#addCouponForm').attr('action'),  // Ensure this matches your URL name
			data: formData,
			success: function (response) {
				if (response.status) {
					// Clear input fields
					console.log("Coupon created")
					$('#code').val('');
					$('#description').val('');
					$('#discount').val('');
					// Optionally, you can close the modal here
					$('#addCouponModal').modal('hide');
					// Reload the page to show the new coupon
					location.reload();
				} else {
					// Display errors
					console.log("Errors",response.errors);
					$('.invalid-feedback').text('');  // Clear previous errors
					$('.form-control').removeClass('is-invalid');  // Clear previous invalid classes
					if (response.errors) {
						for (var field in response.errors) {
							$('#' + field + 'Error').text(response.errors[field][0]);
							$('#' + field).addClass('is-invalid');
						}
					}
				}
			},
		});
	});

	$('.productReturnApproveBtn').click(function (e) { 
		e.preventDefault();
		var button=$(this);
		var order_id= button.closest('tr').data('order-id')
		var product_id=button.closest('tr').data('product-id')
		var status=button.val()
        var token = $('input[name=csrfmiddlewaretoken]').val();
		console.log(order_id,product_id,status);
		$.ajax({
			type: "POST",
			url: $('input[name=approveReturnUrl]').val(),
			data: {
				'order_id':order_id,
				'product_id':product_id,
				'status':status,
				'csrfmiddlewaretoken':token
			},
			success: function (response) {
				console.log(response.success)
				if (response.success) {
                    $('#view_order-' + order_id).modal('hide')
					location.reload();
                } else {
                    alert('Failed to approve return.');
                }
			}
		});
		
	});
});
