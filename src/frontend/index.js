const imageInput = document.getElementById('img_src');
const modalLoading = document.querySelector('.modal_loading');

let fr; // Variable to store the file reader
let is_img_ready = false;
let imageCache = null;
let rawImage = null;
let lastActive = null;
let currentLayer = 0;

let max_face_size = 112
const changeButtons = (action) => {
    if (action === 'upload') {
        document.querySelector('#detect_button').classList.remove('hidden')
        document.querySelector('#link_button').classList.remove('hidden')

        document.querySelector('#add_button').classList.add('hidden')
        document.querySelector('#find_button').classList.add('hidden')
    }

    if (action === 'select-face') {
        document.querySelector('#detect_button').classList.add('hidden')
        document.querySelector('#link_button').classList.add('hidden')

        document.querySelector('#add_button').classList.remove('hidden')
        document.querySelector('#find_button').classList.remove('hidden')
    }
}
const drawDisclaimer = (info) => {
    // рисуем простой дисклеймер и возвращаем его
    return `
        <div class="disclaimer">
            <p>id = ${info.id}</p>
        </div> 
    `
}

const drawDisclaimer1 = (info) => {
    // рисуем простой дисклеймер и возвращаем его
    return `
        <div class="disclaimer">
            <p>id = ${info.id}</p>
            <p>prob = ${info.prob}</p>
        </div> 
    `
}

const drawDisclaimer2 = (info) => {
    // рисуем простой дисклеймер и возвращаем его
    return `
        <div class="disclaimer">
            <p>id = ${info.id}</p>
        </div> 
    `
}

function removeElementsByClass(className) {
    var elements = document.getElementsByClassName(className);
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }
}

const addDisclaimer = (element, info, action) => {
    if (element instanceof HTMLElement) {
        element.addEventListener('click', () => {
            console.log('click on face');
            if (document.querySelector('.active')) {
                document.querySelector('.active').classList.remove('active');
            }
            element.classList.add('active')
            let type_ = element.parentElement.parentElement.classList[2];
            if (type_ === 'canvas-wrapper_detections') {
                changeButtons('select-face')
            } else {
                let layer = parseInt(type_.match(/\d+/)[0], 10);
                console.log('layer: ', layer)
                console.log('current layer: ', currentLayer)
                for (var i = layer + 1; i < currentLayer; i++)
                    removeElementsByClass('canvas-wrapper_layer_' + i);
                processImage(element, 'neighbors', info['id']);
            }
        });
        if (action === "query") {
            const disclaimer = drawDisclaimer1(info);
            element.insertAdjacentHTML('afterend', disclaimer);
        }
        if (action === "neighbors") {
            const disclaimer = drawDisclaimer2(info);
            element.insertAdjacentHTML('afterend', disclaimer);

        }
    }

}


const readImage = () => {
    const imageData = imageInput;

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
    console.log('databaseWrapper: ', databaseWrapper)
    console.log('inputsWrapper: ', inputsWrapper)
    if (databaseWrapper && inputsWrapper) {
        console.log('EST!')
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

function updateImage(image = null) {
    rawImage = fr.result;
    console.log('start updateImage');
    const img = new Image();
    const wrapperLocalCanvas = document.querySelector('.canvas-wrapper_local');

    console.log('wrapperLocalCanvas = ', wrapperLocalCanvas);

    wrapperLocalCanvas.innerHTML = ''

    const newLocal = document.createElement('canvas');

    wrapperLocalCanvas.insertAdjacentElement('afterbegin', newLocal);

    newLocal.id = 'local_canvas';

    img.onload = function () {
        const max_dim = img.width < img.height ? img.height : img.width;
        const scale = max_face_size / max_dim;
        newLocal.width = Math.floor(scale * img.width);
        newLocal.height = Math.floor(scale * img.height);
        const ctx = newLocal.getContext("2d");
        ctx.drawImage(img, 0, 0, newLocal.width, newLocal.height);
        //alert(canvas.toDataURL("image/png"));
    };
    let src = null;

    if (image instanceof HTMLElement) {
        src = image.toDataURL("image/jpeg");
    } else {
        src = fr.result;
    }
    // console.log('src = ', src);

    img.src = src;
    imageCache = null;
    is_img_ready = true;
}

function loadProcessedImage(data, action) {
    const container = document.querySelector('.list-container');
    const newListImages = document.createElement('div');
    newListImages.classList.add('canvas-wrapper')
    newListImages.classList.add('canvas-wrapper_scrolled')
    if (action === "detect")
        newListImages.classList.add('canvas-wrapper_detections')
    // if(action === 'query')
    //     newListImages.classList.add('canvas-wrapper_finders')
    if (action === 'query' || action === 'neighbors') {
        newListImages.classList.add('canvas-wrapper_layer_' + currentLayer)
        currentLayer++;
    }
    const placeForCanvas = newListImages;

    placeForCanvas.innerHTML = ''

    console.log('loadProcessedImage');

    if (!data) return;

    const renderImage = (info) => {
        // console.log('info = ', info);

        if (!placeForCanvas || !info) return;

        if (typeof info === "string") {
            info = {
                image: 'data:image/jpeg;base64,' + info,
                id: 0,
                meta: ''
            }
        }

        const newCanvasWrapper = document.createElement('div');
        const newCanvas = document.createElement('canvas');

        newCanvasWrapper.insertAdjacentElement('afterbegin', newCanvas);
        newCanvasWrapper.classList.add('canvas_wrapper_item')

        const img = new Image();

        img.onload = function () {
            const localCanvas = document.getElementById('local_canvas');
            const max_dim = img.width < img.height ? img.height : img.width;
            const scale = max_face_size / max_dim;
            newCanvas.width = Math.floor(scale * img.width);
            newCanvas.height = Math.floor(scale * img.height);
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
        addDisclaimer(newCanvas, info, action);
        placeForCanvas.insertAdjacentElement('afterbegin', newCanvasWrapper);
    }

    if (typeof data === 'object') {
        // console.log('data === object')
        data.forEach((image) => {
            // console.log('iteration')
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
    container.insertAdjacentElement('beforeend', newListImages)
}

function processImage(element = null, action = 'query', id = null) {
    if (!is_img_ready) {
        alert('No image to process!');
        return;
    }
    // если по какой то причине не удалось обработать изображение то остановить код
    if (!document.getElementById('local_canvas')) return;
    console.log('before selector');

    // переводим изображение
    // console.log('rawImage: ', rawImage)
    // console.log('lastActive: ', lastActive)
    const image_data = lastActive ? lastActive : rawImage;

    // console.log('image_data = ', image_data);
    // если действие было открыть модальное, значит нам нужно лишь поменять интерфейс на добавление id
    // и дальше оостановить код return; то есть ниже уже не пойдет.
    if (action === 'open-modal') {
        toggleDatabaseWindow();
        return;
    }

    // открываем окно загрузки  отправкой запроса
    modalLoading.classList.toggle('is-active');

    // берем инпут который отвечает за id при добавлении в базу
    const imageIdElement = document.querySelector('#database-id');
    // если инпут есть &&(и) в инпуте есть значение то берем его, если нету то null
    let imageId = null;
    if (action == 'neighbors') {
        imageId = id;
    } else {
        imageId = (imageIdElement && imageIdElement.value) || null;
    }
    // console.log('rawImage: ', rawImage)
    // console.log('lastActive: ', lastActive)
    // console.log('image_data: ', image_data);
    console.log('id: ', imageId);
    // action = action === "open-modal" ? 'add' : action;

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
                parsed = data
            }
            // console.log('parsed = ', parsed);
            // if (parsed) alert(parsed['message'])
            // есть сервер вернул Success значит просто вывести сообщение
            if (data === 'Success') {
                alert('Добавлено успешно')
            } else if (parsed && parsed.result) {
                // если это какая то инфомрация другая то выввести изображение
                loadProcessedImage(parsed.result, action);
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
    changeButtons('upload')
    readImage()
});

document.querySelectorAll('[data-action]').forEach((button) => {
    button.addEventListener('click', () => {
        const active = document.querySelector('.list-container .active');

        console.log('active: ', active)
        console.log('button.dataset.action: ', button.dataset.action)

        console.log('button.dataset.action = ', button.dataset.action);
        if (active) {
            lastActive = active.toDataURL("image/jpeg");
        }

        updateImage(active);

        const list = document.querySelector('.list-container');
        list.innerHTML = '';

        processImage(lastActive, button.dataset.action, null)
    })
})
document.querySelector('#add_button').addEventListener('click', () => {
    toggleDatabaseWindow();
});