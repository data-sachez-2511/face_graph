// const database  = window.database || [];
// //
// const list = [
//     {
//         image: 'base_64',
//         id: 101,
//         meta: '{"name": "sanek"}'
//     },
//     {
//         image: 'base_64',
//         id: 102,
//         meta: '{ opa: "sanek2" }'
//     }
// ]
const imageInput = document.getElementById('img_src');
const modalLoading = document.querySelector('.modal_loading');

let fr; // Variable to store the file reader
let is_img_ready = false;
let imageCache = null;
let rawImage = null

let max_face_size = 256

const drawDisclaimer = (info) => {
    // рисуем простой дисклеймер и возвращаем его
    return `
        <div class="disclaimer">
            <p>Meta = ${ info.meta }</p>
            <p>id = ${ info.id }</p>
        </div> 
    `
}

const addDisclaimer = (element, info) => {
    if (element instanceof HTMLElement) {
        // вешаем слушатель на изображние
        element.addEventListener('click', () => {
            // добавляем класс active что бы потом видеть на какое изображение мы нажимали
            element.classList.add('acitve')
            // запускаем обработку такую же как при нажатии кнопок в интерфейса
            // первый аргумент - текущее изображение
            // второй аргумент - действие - поиск похожих
            processImage(element, 'query');
        });
        // получаем дисклеймер с нашей информацией
        const disclaimer = drawDisclaimer(info);
        // добавляем дисклеймер к изображению
        element.insertAdjacentHTML('afterend', disclaimer);
    }
}

// const writeToDataBase = (data) => {
//     if (!data) return;
//
//     const localData = JSON.parse(localStorage.getItem('imageDataBase')) || [];
//
//     const newData = {
//         id: localData.length,
//         meta: {
//             name: 'User#' + localData.length
//         },
//         image: data,
//     }
//
//     localData.push(newData);
//
//     localStorage.setItem('imageDataBase', JSON.stringify(localData));
//
//     return 'Success';
// }
//
// const detectFace = (data) => {
//     if (!data) return;
//
//     const localData = JSON.parse(localStorage.getItem('imageDataBase')) || [];
//
//
//
//     return [{
//         id: localData.length,
//         meta: 'User#' + localData.length,
//         image: data,
//     }]; // lol
// }
//
// const findSimilarFaces = (data) => {
//     if (!data) return;
//     return database
// }

const readImage = (image = null) => {
    const imageData = image ? image : imageInput;

    if (!imageData.files[0]) {
        alert('Please select an Image first!')
        return;
    }

    fr = new FileReader();
    fr.onload = updateImage;
    fr.readAsDataURL(imageData.files[0])
}

const toggleDatabaseWindow = () => {
    // находим две обертки кнопок и инпута id
    const databaseWrapper = document.querySelector('.database-wrapper');
    const inputsWrapper = document.querySelector('.inputs-wrapper');

    if (databaseWrapper && inputsWrapper) {
        // если оба есть то переключаем их состояние
        databaseWrapper.classList.toggle('is-active');
        inputsWrapper.classList.toggle('is-active');
    }
}

const showStatusAddtoDatabase = (status = 'good') => {
    // нужно для того что бы перевести статут в нужный класс
    const results = {
        good: 'is-success',
        bad: 'is-unsuccessful'
    }
    // поле трех кнопок
    const inputsWrapper = document.querySelector('.inputs-wrapper');
    // показываем результат
    inputsWrapper.classList.add(results[status]);

    setTimeout(() => {
        // спустя 1500 мс удаляем класс
        inputsWrapper.classList.remove(results[status]);
    }, 1500)
}

function updateImage() {
    rawImage = fr.result;
    console.log('start updateImage');
    const img = new Image();
    const wrapperLocalCanvas = document.querySelector('.canvas-wrapper_local');

    console.log('wrapperLocalCanvas = ', wrapperLocalCanvas);

    wrapperLocalCanvas.innerHTML = ''

    const newLocal = document.createElement('canvas');

    wrapperLocalCanvas.insertAdjacentElement('afterbegin', newLocal);

    newLocal.id = 'local_canvas';

    img.onload = function() {
        const max_dim = img.width < img.height ? img.height: img.width;
        const scale = max_face_size / max_dim;
        newLocal.width  = Math.floor( scale * img.width );
        newLocal.height = Math.floor( scale * img.height );
        const ctx = newLocal.getContext("2d");
        ctx.drawImage(img,0,0, newLocal.width, newLocal.height);
        //alert(canvas.toDataURL("image/png"));
    };
    const src = imageCache ? imageCache : fr.result;

    img.src = src;
    imageCache = null;
    is_img_ready = true;
}

function loadProcessedImage(data) {
    const container = document.querySelector('.list-container');
    const newListImages = document.createElement('div');
    newListImages.classList.add('canvas-wrapper')
    newListImages.classList.add('canvas-wrapper_processed')

    const placeForCanvas = newListImages;

    placeForCanvas.innerHTML = ''

    console.log('loadProcessedImage');

    if (!data) return;

    const renderImage = (info) => {

        console.log('info = ', info);

        if (!placeForCanvas || !info) return;

        const newCanvasWrapper = document.createElement('div');
        const newCanvas = document.createElement('canvas');

        newCanvasWrapper.insertAdjacentElement('afterbegin', newCanvas);
        newCanvasWrapper.classList.add('canvas_wrapper_item')

        const img = new Image();

        img.onload = function() {
            const localCanvas = document.getElementById('local_canvas');
            const max_dim = img.width < img.height ? img.height: img.width;
            const scale = max_face_size / max_dim;
            newCanvas.width  = Math.floor( scale * img.width );
            newCanvas.height = Math.floor( scale * img.height );
            const ctx = newCanvas.getContext('2d');

            ctx.drawImage(
                img,
                0,
                0,
                newCanvas.width,
                newCanvas.height
                );
        };
        img.src = info.image;
        // img.src = info.image;

        newCanvas.setAttribute('User-meta', info.meta);
        newCanvas.setAttribute('User-id', info.id);
        newCanvas.classList.add('image-disclaimer')

        addDisclaimer(newCanvas, info);

        placeForCanvas.insertAdjacentElement('afterbegin', newCanvasWrapper);
    }

    if (typeof data === 'object') {
        console.log('data === object')
        data.forEach((image) => {
            console.log('iteration')
            renderImage(image);
        })
    } else {
        console.log('else')
        const tempResult = {
            image: data,
            id: 0,
            meta: 'ddd'
        }
        renderImage(tempResult);
    }
    container.insertAdjacentElement('beforeend',newListImages)
}

function processImage(element = null,action = 'query') {
    if (!is_img_ready) {
        alert('No image to process!');
        return;
    }
    // если по какой то причине не удалось обработать изображение то остановить код
    if (!document.getElementById('local_canvas')) return;
    // переводим изображение
    const image_data = rawImage;

    // если действие было открыть модальное, значит нам нужно лишь поменять интерфейс на добавление id
    // и дальше оостановить код return; то есть ниже уже не пойдет.
    if (action === 'open-modal') {
        toggleDatabaseWindow();
        return;
    }
    /*
    mapOperations
    response

    нужны для эмуляции сервера при тестировании логики кода
    если нужно подебажить то расскоментируй строки:

    1; 51-88; 262-293 и закомментируй 304-348
     */


    /*
    const mapOperations = {
        add: writeToDataBase,
        detect: detectFace,
        query: findSimilarFaces,
    }
    const response = new Promise((resolutionFunc) => {
        setTimeout(() => {
            let result = null;
            if (action === 'add') {
                result = 'Succsess'
            } else {
                result = mapOperations[action](image_data)
            }
            // console.log('result = ', result);
            resolutionFunc(result)
        }, 1500)

    })

    response.then((result) => {
        modalLoading.classList.toggle('is-active');
        if (action === 'add') {
            toggleDatabaseWindow();
            showStatusAddtoDatabase('good')
        }

        if (result === 'Succsess') {
            return;
        }
        loadProcessedImage(result);
    })
    */


    // открываем окно загрузки перед отправкой запроса
    modalLoading.classList.toggle('is-active');

    // берем инпут который отвечает за id при добавлении в базу
    const imageIdElement = document.querySelector('#database-id');
    // если инпут есть &&(и) в инпуте есть значение то берем его, если нету то null
    const imageId = (imageIdElement && imageIdElement.value) || null;

    $.ajax({
        url: "http://localhost:5000/process_image",
        method: "POST",
        contentType: 'application/json',
        crossDomain: true,
        data: JSON.stringify({
            image_data: {
                id: imageId,
                data: image_data
            },
            msg: 'This is image data',
            operation: action
        }),
        success: function (data) {
            // закрыть окно загрузки
            modalLoading.classList.toggle('is-active');

            if (action === 'add') {
                toggleDatabaseWindow();
                // показать визуально что все успешно прошло
                showStatusAddtoDatabase('good')
            }

            // обработаем результат который получили от сервера
            let parsed = null
            try {
                parsed = JSON.parse(data);
            } catch (e) {
                console.log('error = ', e)
            }
            // есть сервер вернул Success значит просто вывести сообщение
            if (data === 'Success') {
                alert('Добавлено успешно')
            } else {
                // если это какая то инфомрация другая то выввести изображение
                loadProcessedImage(parsed);
            }
        },
        error: function (err) {
            console.log('error =  ', err)
            // показать визуально что произошла ошибка
            showStatusAddtoDatabase('bad')

        }
    });
}
// слушатель на инпуте изображения, как только добавляем изображение сразу вызывается функция обработки его
imageInput.addEventListener('input', () => {
    readImage();
})
// находим все элементы с атрибутом data-action и для каждого ставим слушатель
// в слушателе вызываем processImage
// первый аргумент - изображение и там null
// второй аргумент - действие, берем его и самого значения прописаного в data-action
// например data-action="add"

document.querySelectorAll('[data-action]').forEach((button) => {
    button.addEventListener('click', () => {
        processImage(null,button.dataset.action)
    })
})
