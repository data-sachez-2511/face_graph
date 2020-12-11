const database  = [{"image": "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", "id": 1, "meta": "it is test"}]
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
        if (/data:image/.test(info.image)) {
            img.src = info.image;
        } else {
            img.src = 'data:image/jpeg;base64,' + info.image;
        }
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
