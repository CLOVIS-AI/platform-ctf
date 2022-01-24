(function ($) {

	"use strict"

	// ISOTOPE
	if (isExists('.p-grid-isotope')) {
		// init Isotope
		var $grid = $('.p-grid-isotope').isotope({
			itemSelector: '.p-item',
			percentPosition: true,
			masonry: {
				columnWidth: '.grid-sizer',
				horizontalOrder: true,
			}
		})

		// layout Isotope after each image loads
		$grid.imagesLoaded().progress(function () {
			$grid.isotope('layout')
		})
	}

	// DROPDOWN MENU
	var winWidth = $(window).width()
	dropdownMenu(winWidth)

	$(window).on('resize', function () {
		winWidth = $(window).width()
		dropdownMenu(winWidth)

	})

	// REVOLUTION SLIDER
	if (isExists('#rev_slider_28_1')) {
		var tpj = jQuery
		var revapi28

		if (tpj("#rev_slider_28_1").revolution == undefined) {
			revslider_showDoubleJqueryError("#rev_slider_28_1")
		} else {
			revapi28 = tpj("#rev_slider_28_1").show().revolution({
				sliderType: "standard",
				jsFileLocation: "revolution/js/",
				sliderLayout: "fullscreen",
				dottedOverlay: "none",
				delay: 5000,
				navigation: {
					keyboardNavigation: "off",
					keyboard_direction: "horizontal",
					mouseScrollNavigation: "off",
					mouseScrollReverse: "default",
					onHoverStop: "off",
					arrows: {
						style: "uranus",
						enable: true,
						hide_onmobile: false,
						hide_onleave: false,
						tmp: '',
						left: {
							h_align: "left",
							v_align: "center",
							h_offset: 20,
							v_offset: 0
						},
						right: {
							h_align: "right",
							v_align: "center",
							h_offset: 20,
							v_offset: 0
						}
					},
					bullets: {
						enable: true,
						hide_onmobile: false,
						style: "hermes",
						hide_onleave: false,
						direction: "horizontal",
						h_align: "center",
						v_align: "bottom",
						h_offset: 0,
						v_offset: 20,
						space: 5,
						tmp: ''
					}
				},
				responsiveLevels: [1240, 1024, 778, 480],
				visibilityLevels: [1240, 1024, 778, 480],
				gridwidth: [1240, 1024, 778, 480],
				gridheight: [868, 768, 960, 720],
				lazyType: "none",
				shadow: 0,
				spinner: "off",
				stopLoop: "off",
				stopAfterLoops: -1,
				stopAtSlide: -1,
				shuffle: "off",
				autoHeight: "off",
				fullScreenAutoWidth: "off",
				fullScreenAlignForce: "off",
				fullScreenOffsetContainer: "",
				fullScreenOffset: "130px",
				hideThumbsOnMobile: "off",
				hideSliderAtLimit: 0,
				hideCaptionAtLimit: 0,
				hideAllCaptionAtLilmit: 0,
				debugMode: false,
				fallbacks: {
					simplifyAll: "off",
					nextSlideOnWindowFocus: "off",
					disableFocusListener: false,
				}
			})
		}
	}

	$('[data-menu]').on('click', function () {
		var mainMenu = $(this).data('menu')
		$(mainMenu).toggleClass('visible-menu')
	})

	if (isExists('.imglist')) {
		$('[data-fancybox="photo"]').fancybox({
			image: {
				preload: false
			},
			loop: true,
			buttons: [
				"zoom",
				"slideShow",
				"fullScreen",
				"download",
				"delete",
				"close"
			],
			lang: "fr",
			i18n: {
				fr: {
					CLOSE: "Fermer",
					NEXT: "Suivant",
					PREV: "Précédent",
					ERROR: "Le contenu demandé n'a pas pu être chargé. <br/> Veuillez réessayer ultérieurement.",
					PLAY_START: "Démarrer le diaporama",
					PLAY_STOP: "Mettre en pause le diaporama",
					FULL_SCREEN: "Plein écran",
					THUMBS: "Miniatures",
					DOWNLOAD: "Télécharger",
					DELETE: "Demander la suppression",
					SHARE: "Partager",
					ZOOM: "Zoom"
				}
			},
			btnTpl: {
				download: '<a download="PixEirb ' + $(".album-name").text() + '" data-fancybox-download class="fancybox-button fancybox-button--download" title="{{DOWNLOAD}}" href="javascript:;">' +
						'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.62 17.09V19H5.38v-1.91zm-2.97-6.96L17 11.45l-5 4.87-5-4.87 1.36-1.32 2.68 2.64V5h1.92v7.77z"/></svg>' +
						"</a>",
				delete: '<button data-fancybox-delete class="fancybox-button fancybox-button--delete" title="{{DELETE}}">' +
						'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m10.1488,12.61707l0,3.70241c0,0.34062 -0.27645,0.61707 -0.61707,0.61707s-0.61707,-0.27645 -0.61707,-0.61707l0,-3.70241c0,-0.34062 0.27645,-0.61707 0.61707,-0.61707s0.61707,0.27645 0.61707,0.61707zm4.31948,-0.61707c-0.34062,0 -0.61707,0.27645 -0.61707,0.61707l0,3.70241c0,0.34062 0.27645,0.61707 0.61707,0.61707s0.61707,-0.27645 0.61707,-0.61707l0,-3.70241c0,-0.34062 -0.27645,-0.61707 -0.61707,-0.61707zm-2.46827,0c-0.34062,0 -0.61707,0.27645 -0.61707,0.61707l0,3.70241c0,0.34062 0.27645,0.61707 0.61707,0.61707s0.61707,-0.27645 0.61707,-0.61707l0,-3.70241c0,-0.34062 -0.27645,-0.61707 -0.61707,-0.61707zm2.67376,-5.32098c-0.54425,-0.11354 -0.84723,-0.86945 -0.73369,-1.4137l-3.21061,-0.67014c-0.11354,0.54487 -0.69297,1.11689 -1.2366,1.00274l-3.41115,-0.67816l-0.25238,1.20822l12.08898,2.52936l0.25238,-1.20822l-3.49693,-0.7701zm2.87986,2.85271l0,9.87309l-11.10723,0l0,-9.87309l11.10723,0zm-1.23414,8.63895l0,-7.40482l-8.63895,0l0,7.40482l8.63895,0z"/></svg>' +
						"</button>"
			},
			afterShow: function (instance, current) {
				$("[data-fancybox-download]").attr('download', $("[data-fancybox-download]").attr('download') + " " + (current.index + 1))
			}
		})
	}

	$('button[data-toggle="tooltip"]').tooltip({
		html: true
	})

})(jQuery)


function dropdownMenu(winWidth) {
	if (winWidth > 767) {
		$('.main-menu li.drop-down').on('mouseover', function () {
			var $this = $(this),
					menuAnchor = $this.children('a')
			menuAnchor.addClass('mouseover')
		}).on('mouseleave', function () {
			var $this = $(this),
					menuAnchor = $this.children('a')
			menuAnchor.removeClass('mouseover')
		})
	} else {
		$('.main-menu li.drop-down > a').on('click', function () {
			if ($(this).attr('href') == '#') return false
			if ($(this).hasClass('mouseover')) {
				$(this).removeClass('mouseover')
			} else {
				$(this).addClass('mouseover')
			}
			return false
		})
	}
}

function isExists(elem) {
	if ($(elem).length > 0) {
		return true
	}
	return false
}

$('body').on('click', '[data-fancybox-delete]', function () {
	$('#askForRemoval').modal('toggle')
})

function confirmAskForRemoval() {
	$.ajax({
		url: 'picManagement.php',
		type: 'POST',
		data: {
			id: $.fancybox.getInstance().$trigger[0].children[0].id,
			login: document.getElementById("login").value,
			name: document.getElementById("name").value,
			motive: document.getElementById("motive").value
		},
		success: function (resp) {
			$('#askForRemoval').modal('hide')
			showAlertRemoval(resp)
		}
	})

	document.getElementById("login").value = ''
	document.getElementById("name").value = ''
	document.getElementById("motive").value = ''
}

function showAlertRemoval(resp) {
	$("#alertRemovalWrap").empty()
	$("#alertRemovalWrap").append(resp)
	$("#alertRemoval").show()
	setTimeout(function () {
		$("#alertRemoval").hide()
	}, 2000)
}

function zoomRemoveRequestImage(event) {
	var modal = document.getElementById("modal-remove-request")
	var modalPhoto = document.getElementById("modalPhoto")

	modal.style.display = "block"
	$(modalPhoto.setAttribute("src", "../photos/" + event.target.getAttribute('src').split("thumbnails/").pop()))
	$('#caption').text(event.target.getAttribute('alt'))
}

function closeSpanOnClick() {
	var modal = document.getElementById("modal-remove-request")
	modal.style.display = "none"
}

function updateThumbnail(new_thumbnail) {
	// Change colors
	var old_thumbnail = document.getElementById("thumbnail").value
	document.getElementById(old_thumbnail).className = "card list-group-item"
	document.getElementById(new_thumbnail).className += " text-white bg-dark"

	// Updating thumbnail value
	document.getElementById("thumbnail").value = new_thumbnail

	var new_thumbnail_infos = document.getElementById(new_thumbnail).getElementsByTagName('button')[0].getAttribute('data-original-title')
	document.getElementById("thumbnail-photo").src = new_thumbnail_infos.split("'")[1]
	document.getElementById("thumbnail-photo").alt = "Photo " + new_thumbnail
}

function isSelected(photo_id) {
	return $('#photo_id').find('.photo-checkbox').is(':checked')
}

