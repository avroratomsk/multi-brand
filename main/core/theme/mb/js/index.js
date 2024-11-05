// import "./import/modules";
// import "./import/components";
// import "./import/inputMask";
// import "./import/script";

// new VenoBox({
//   selector: ".index-gallery__item"
// });


/**
 * Вспомогательные общие функции
 */

const bodyLock = (e) => {
  let widthScrollBar = window.innerWidth - document.documentElement.clientWidth;
  document.documentElement.style.marginRight = widthScrollBar + 'px';
  document.documentElement.classList.add('_lock');
}

const bodyUnLock = (e) => {
  document.documentElement.style.marginRight = '0px';
  document.documentElement.classList.remove('_lock');
}


// Создание правильной ссылка номера телефона
const regNum = document.querySelectorAll('a[href^="tel:"]');
if (regNum) {
  regNum.forEach(num => {
    let number = formatPhoneNumber(num.href);
    num.href = `tel:${number}`;
  })
}

function formatPhoneNumber(phoneNumber) {

  // Убираем все лишние символы (скобки, пробелы, тире)
  let cleanedNumber = phoneNumber.replace('tel:', '').replace(/[\s\-\(\)]/g, '');

  // Если номер уже начинается на +7, ничего не делаем
  if (cleanedNumber.startsWith('+7')) {
    return cleanedNumber;
  }

  // Если номер начинается на 8, заменяем на +7
  if (cleanedNumber.startsWith('8')) {
    return '+7' + cleanedNumber.slice(1);
  }

  // В остальных случаях добавляем +7 к началу
  return '+7' + cleanedNumber;
}

/**
 * Функции отвечающие за открытие и закрытие мини-корзины
 */

const showCart = document.querySelectorAll('.show-cart');
if (showCart) {
  showCart.forEach(btn => {
    btn.addEventListener('click', showMiniCart);
  })
}

function showMiniCart(e) {
  document.querySelector('#mini-cart').classList.add('_show');
  bodyLock();
}

const closeCart = document.getElementById('close-cart');
if (closeCart) {
  closeCart.addEventListener('click', closeMiniCart);
}

function closeMiniCart(e) {
  document.querySelector('#mini-cart').classList.remove('_show');
  bodyUnLock();
}



/**
 * Работа с добавление в корзину без перезагрузки страницы
 */

let addToCartButton = document.querySelectorAll('.add-to-cart');
if (addToCartButton) {
  addToCartButton.forEach(btn => {
    btn.addEventListener('click', addCartProduct)
  })
}

function addCartProduct(e) {
  e.preventDefault();
  let csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
  // Элементы которые меняются
  let productCount = 0;
  let goodsInCartCount = document.getElementById('mini-cart-count');
  if (goodsInCartCount) {
    productCount = parseInt(goodsInCartCount.innerText, 0);
  }

  let productId = e.target.dataset.productId;
  let variation = {}
  const selectElem = document.querySelectorAll('select');
  selectElem.forEach(elem => {
    if (elem.dataset.name == 'Цвета') {
      elemName = elem.dataset.name.slice(0, -1);
      variation[elemName] = elem.value;
    } else if (elem.dataset.name == 'Размеры') {
      elemName = elem.dataset.name.slice(0, -1);
      variation[elemName] = elem.value;
    } else {
      elemName = elem.dataset.name;
      variation[elemName] = elem.value;
    }
  });

  let addToCartUrl = e.target.getAttribute('href');
  // "/cart/cart_add-test/"
  fetch(addToCartUrl, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({ "productId": productId, "variation": variation })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Error")
      }

      return response.json()
    })
    .then(data => {
      // Уведомление добавления в корзину
      const notificationModal = document.getElementById('notification-modal');
      notificationModal.querySelector('.success__body').innerHTML = '<div class="success__body-inner"><p class="success__name">Товар добавлен</p></div>';
      notificationModal.classList.add("show");

      // Закрытие уведомления после 5 секунд
      setTimeout(function () {
        notificationModal.classList.remove("show");
      }, 5000);

      const showCartBody = document.querySelectorAll(".show-cart");
      if (showCartBody) {
        showCartBody.forEach(btn => {
          let countElem = btn.querySelector('.count-product-cart');
          if (countElem) {
            countElem.innerText = data.cart_total_count;
          } else {
            let span = document.createElement('span');
            span.className = 'count-product-cart';
            span.innerText = data.cart_total_count;
            btn.appendChild(span);
          }
        })
      }
      document.getElementById('mini-cart_noempty').innerHTML = '<h4 class="mini-cart__title">Корзина<span>(</span><strong id="mini-cart-count">' + data.cart_total_count + '</strong><span>)</span></h4><div class="mini-cart__inner" id="cart-item">{% include "components/cart-item.html" %}</div><div class="mini-cart__links"><a href="/orders/create/" class="mini-cart__link">Оформить заказ</a></div>';


      // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
      const cartItemsContainer = document.getElementById('cart-item');
      cartItemsContainer.innerHTML = data.cart_items_html;


    })
    .catch(error => {
      console.log(error);
    })
}

$(document).on("click", ".remove-from-cart", function (e) {
  // Блокируем его базовое действие
  e.preventDefault();

  // Берем элемент счетчика в значке корзины и берем оттуда значение
  var goodsInCartCount = $("#mini-cart-count");
  var cartCount = parseInt(goodsInCartCount.text() || 0);

  // Получаем id корзины из атрибута data-cart-id
  var cart_id = $(this).data("cart-id");
  // Из атрибута href берем ссылку на контроллер django
  var remove_from_cart = $(this).attr("href");
  console.log(remove_from_cart);
  console.log($("[name=csrfmiddlewaretoken]").val());
  // делаем post запрос через ajax не перезагружая страницу
  $.ajax({
    type: "POST",
    url: remove_from_cart,
    data: {
      cart_id: cart_id,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {
      // Уменьшаем количество товаров в корзине (отрисовка)
      cartCount -= data.quantity_deleted;
      goodsInCartCount.text(cartCount);

      if (cartCount == 0) {
        // $('#show-cart .no-empty').remove();
        $('#mini-cart_noempty').html('<div class="mini-cart__empty"><p class="mini-cart__empty-text">Пусто</p><a href="{% url "category" %}"class="mini-cart__empty-link">Перейти в каталог</a></div>')
        // $('#mini-cart .mini-cart__links').remove()
      }
      // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
      var cartItemsContainer = $("#cart-item");
      cartItemsContainer.html(data.cart_items_html);
    },

    error: function (data) {
      console.log("Ошибка при добавлении товара в корзину");
    },
  });
});


/**
 * Popup окна
 */

const openPopup = (event) => {
  let popupBtn = event.target.closest('[data-popup]')
  if (popupBtn) {
    popup = document.getElementById(popupBtn.dataset.popup);
    document.documentElement.classList.add('popup-show');
    popup.classList.add('popup_show');

    let nameOrder = popupBtn.dataset.order;

    if (nameOrder) {
      let fieledHidden = popup.querySelector('input[name="service"]');
      console.log(fieledHidden);
      fieledHidden.value = nameOrder;
    }

    bodyLock();
  }
}

const closePopup = (event) => {
  let popupCloseBtn = event.target.closest('.popup__close');
  if (popupCloseBtn) {
    popup = popupCloseBtn.closest('.popup');
    popup.classList.remove('popup_show');
    document.documentElement.classList.remove('popup-show');
    bodyUnLock();
  }
}

const popupBtn = document.querySelectorAll('[data-popup]');
if (popupBtn) {
  popupBtn.forEach(btn => btn.addEventListener('mouseup', openPopup));
}

const closePopupBtn = document.querySelectorAll('.popup__close');
if (closePopupBtn) {
  closePopupBtn.forEach(btn => btn.addEventListener('click', closePopup))
}


/*******************************/



/********Burger menu**********/
const burgerButton = document.getElementById('burger-btn');
if (burgerButton) {
  burgerButton.addEventListener('mouseup', (event) => {
    const burgerBtn = event.target.closest('#burger-btn');
    console.log('click');

    if (burgerBtn) {
      let nav = document.querySelector('.nav');
      nav.classList.toggle('_active');
      if (nav.classList.contains('_active')) {
        bodyLock();
      } else {
        bodyUnLock();
      }
    }
  })
}

/************Формы обратной связи*************/

// Функция для поиска английских букв в поле ввода
function containsEnglishLetters(str) {
  const regex = /[a-zA-Z]/;
  return regex.test(str);
}


// Функция для нахождения ссылки в поле ввода
function containsLink(input) {
  const regex = /(https?:\/\/[^\s]+)/g;
  return regex.test(input);
}

// Валидация полей формы
function validateForm(fieldsArray) {
  if (containsEnglishLetters(fieldsArray.name)) {
    return false;
  }

  if (containsLink(fieldsArray.message)) {
    return false;
  }

  if (containsLink(fieldsArray.reviews)) {
    return false;
  }

  return true;
}

// Отправка формы
function sendForm(form, popupName = 'default') {
  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const eventForm = event.target;
    const formData = new FormData(eventForm);
    const csrfToken = eventForm.querySelector('[name=csrfmiddlewaretoken]').value;

    let dataObj = {}
    for (let [key, value] of formData.entries()) {
      dataObj[key] = value;
    }

    if (validateForm(dataObj)) {
      fetch(form.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          form.reset();
          if (popupName != 'default') {
            document.documentElement.classList.remove('popup-show')
            bodyUnLock();
            document.getElementById(popupName).classList.remove('popup_show');
          }
          document.getElementById('success').classList.add('notification_show');
        })
        .catch(error => {
          console.log(error);
        });
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  const consultationForm = document.getElementById('consultation');
  if (consultationForm) {
    sendForm(consultationForm, 'consultation-form');
  }

  const callBackForm = document.getElementById('callback-form');
  if (callBackForm) {
    sendForm(callBackForm, 'callback');
  }

  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    sendForm(contactForm);
  }

  const orderService = document.getElementById('order-service-form');
  if (orderService) {
    sendForm(orderService, 'order-service');
  }

  const reviewsForm = document.getElementById('reviews-form');
  if (reviewsForm) {
    sendForm(reviewsForm, 'reviews');
  }
});

const header = document.querySelector('.header');
let positionTopHeader = header.getBoundingClientRect().top;

window.addEventListener('scroll', () => {
  let scrollY = window.scrollY || window.pageYOffset;
  // header--sticky

  if (scrollY >= positionTopHeader) {
    header.classList.add('header--sticky');
  } else {
    header.classList.remove('header--sticky');
  }
})