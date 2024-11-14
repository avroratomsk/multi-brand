/**
 * Вспомогательные общие функции
 */

// const bodyLock = (e) => {
//   let widthScrollBar = window.innerWidth - document.documentElement.clientWidth;
//   document.documentElement.style.marginRight = widthScrollBar + 'px';
//   document.documentElement.classList.add('_lock');
// }

// const bodyUnLock = (e) => {
//   document.documentElement.style.marginRight = '0px';
//   document.documentElement.classList.remove('_lock');
// }


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





/*******************************/



/********Burger menu**********/
const burgerButton = document.getElementById('burger-btn');
if (burgerButton) {
  burgerButton.addEventListener('mouseup', (event) => {
    const burgerBtn = event.target.closest('#burger-btn');
    console.log('click');

    if (burgerBtn) {
      let nav = document.querySelector('.nav');
      nav.classList.add('_active');
      if (nav.classList.contains('_active')) {
        bodyLock();
      } else {
        bodyUnLock();
      }
    }
  })
}

const closeMenu = document.getElementById('menu-close');
if (closeMenu) {
  closeMenu.addEventListener('click', (event) => {
    const closeBtn = event.target.closest('#menu-close');
    if (closeBtn) {
      let nav = document.querySelector('.nav');
      nav.classList.remove('_active');
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

// Функция для скролла к элементу
function scrollToElement(elementId) {
  const element = document.getElementById(elementId);
  const headerHeight = document.querySelector('.header').offsetHeight;
  if (element) {
    const elementPosition = element.getBoundingClientRect().top + window.scrollY;
    const offsetPosition = elementPosition - headerHeight;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}

// Обработчик клика на кнопки
document.querySelectorAll('[data-anchor]').forEach(button => {
  button.addEventListener('click', function (e) {
    e.preventDefault();
    const targetId = this.getAttribute('data-anchor');
    scrollToElement(targetId);
    document.querySelector('.nav').classList.remove('_active');
  });
});


document.addEventListener("DOMContentLoaded", function () {
  var phoneInputs = document.querySelectorAll('input[data-tel-input]');

  var getInputNumbersValue = function (input) {
    // Return stripped input value — just numbers
    return input.value.replace(/\D/g, '');
  }

  var onPhonePaste = function (e) {
    var input = e.target,
      inputNumbersValue = getInputNumbersValue(input);
    var pasted = e.clipboardData || window.clipboardData;
    if (pasted) {
      var pastedText = pasted.getData('Text');
      if (/\D/g.test(pastedText)) {
        // Attempt to paste non-numeric symbol — remove all non-numeric symbols,
        // formatting will be in onPhoneInput handler
        input.value = inputNumbersValue;
        return;
      }
    }
  }

  var onPhoneInput = function (e) {
    var input = e.target,
      inputNumbersValue = getInputNumbersValue(input),
      selectionStart = input.selectionStart,
      formattedInputValue = "";

    if (!inputNumbersValue) {
      return input.value = "";
    }

    if (input.value.length != selectionStart) {
      // Editing in the middle of input, not last symbol
      if (e.data && /\D/g.test(e.data)) {
        // Attempt to input non-numeric symbol
        input.value = inputNumbersValue;
      }
      return;
    }

    if (["7", "8", "9"].indexOf(inputNumbersValue[0]) > -1) {
      if (inputNumbersValue[0] == "9") inputNumbersValue = "7" + inputNumbersValue;
      var firstSymbols = (inputNumbersValue[0] == "8") ? "8" : "+7";
      formattedInputValue = input.value = firstSymbols + " ";
      if (inputNumbersValue.length > 1) {
        formattedInputValue += '(' + inputNumbersValue.substring(1, 4);
      }
      if (inputNumbersValue.length >= 5) {
        formattedInputValue += ') ' + inputNumbersValue.substring(4, 7);
      }
      if (inputNumbersValue.length >= 8) {
        formattedInputValue += '-' + inputNumbersValue.substring(7, 9);
      }
      if (inputNumbersValue.length >= 10) {
        formattedInputValue += '-' + inputNumbersValue.substring(9, 11);
      }
    } else {
      formattedInputValue = '+' + inputNumbersValue.substring(0, 16);
    }
    input.value = formattedInputValue;
  }
  var onPhoneKeyDown = function (e) {
    // Clear input after remove last symbol
    var inputValue = e.target.value.replace(/\D/g, '');
    if (e.keyCode == 8 && inputValue.length == 1) {
      e.target.value = "";
    }
  }
  for (var phoneInput of phoneInputs) {
    phoneInput.addEventListener('keydown', onPhoneKeyDown);
    phoneInput.addEventListener('input', onPhoneInput, false);
    phoneInput.addEventListener('paste', onPhonePaste, false);
  }
})


/**
 * Popup окна
 */

const bodyLock = (e) => {
  let widthScrollBar = window.innerWidth - document.documentElement.clientWidth;
  document.documentElement.style.marginRight = widthScrollBar + 'px';
  document.querySelector('.header').style.paddingRight = widthScrollBar + 'px';
  document.documentElement.classList.add('_lock');
}

const bodyUnLock = (e) => {
  document.documentElement.style.marginRight = '0px';
  document.querySelector('.header').style.paddingRight = '0px';
  document.documentElement.classList.remove('_lock');
}

const openPopup = (event) => {
  let popupBtn = event.target.closest('[data-popup]')
  if (popupBtn) {
    const popup = document.getElementById(popupBtn.dataset.popup);
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
    const popup = popupCloseBtn.closest('.popup');
    popup.classList.remove('popup_show');
    document.documentElement.classList.remove('popup-show');
    bodyUnLock();
  }
}

const popup = document.querySelectorAll('.popup');
if (popup) {
  popup.forEach(popup => popup.addEventListener('click', (e) => {
    if (!e.target.closest('.popup__content')) {
      e.currentTarget.classList.remove('popup_show');
      document.documentElement.classList.remove('popup-show');
      bodyUnLock();
    }
  }))
}

document.addEventListener('keydown', (e) => {
  if (e.keyCode === 27 && document.querySelector('.popup_show').classList.contains('popup_show')) {
    document.querySelector('.popup_show').classList.remove('popup_show');
    document.documentElement.classList.remove('popup-show');
    bodyUnLock();
  }
})

const popupBtn = document.querySelectorAll('[data-popup]');
if (popupBtn) {
  popupBtn.forEach(btn => btn.addEventListener('mouseup', openPopup));
}

const closePopupBtn = document.querySelectorAll('.popup__close');
if (closePopupBtn) {
  closePopupBtn.forEach(btn => btn.addEventListener('click', closePopup))
}