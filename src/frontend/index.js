// const database  = window.database || [];
//
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
const modal = document.querySelector('.modal');

let fr; // Variable to store the file reader
let is_img_ready = false;
let imageCache = null;

const drawDisclaimer = (info) => {
    return `
        <div class="disclaimer">
            <p>Meta = ${ info.meta }</p>
            <p>id = ${ info.id }</p>
        </div> 
    `
}

const addDisclaimer = (element, info) => {
    if (element instanceof HTMLElement) {
        element.addEventListener('click', () => {
            element.classList.add('acitve')
            processImage(element, 'query');
        });
        const disclaimer = drawDisclaimer(info);

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
//         name: 'User#' + localData.length,
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

function updateImage() {
    console.log('start updateImage');
    const img = new Image();
    const wrapperLocalCanvas = document.querySelector('.canvas-wrapper_local');

    console.log('wrapperLocalCanvas = ', wrapperLocalCanvas);

    wrapperLocalCanvas.innerHTML = ''

    const newLocal = document.createElement('canvas');

    wrapperLocalCanvas.insertAdjacentElement('afterbegin', newLocal);

    newLocal.id = 'local_canvas';

    img.onload = function() {
        newLocal.width  = 250;
        newLocal.height = 300;
        const ctx = newLocal.getContext("2d");
        ctx.drawImage(img,0,0, 250, 300);
        //alert(canvas.toDataURL("image/png"));
    };
    const src = imageCache ? imageCache : fr.result;

    console.log('src = ', src);

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
            newCanvas.width  = 250;
            newCanvas.height = 300;
            const ctx = newCanvas.getContext('2d');

            ctx.drawImage(
                img,
                0,
                0,
                250,
                300
                );
        };
        img.src = 'data:image/jpeg;base64,' + data;
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
            meta: ''
        }
        renderImage(tempResult);
    }
    container.insertAdjacentElement('beforeend',newListImages)
}


async function processImage(element = null,action = 'query') {
    if (!is_img_ready) {
        alert('No image to process!');
        return;
    }
    //Send the image to the server and wait for a response
    if (!document.getElementById('local_canvas')) return;

    const image_data = document.getElementById('local_canvas')
        .toDataURL('image/jpeg');

    const op = action;
    // console.log('action = ' , op);
    // const mapOperations = {
    //     add: writeToDataBase,
    //     detect: detectFace,
    //     query: findSimilarFaces,
    // }

    modal.classList.toggle('is-active');

    $.ajax({
        url: "http://localhost:5000/process_image",
        method: "POST",
        contentType: 'application/json',
        crossDomain: true,
        data: JSON.stringify({
            image_data: image_data,
            msg: 'This is image data',
            operation: op
        }),
        success: function (data) {
            modal.classList.toggle('is-active');

            let parsed = null
            try {
                parsed = JSON.parse(data);
            } catch (e) {
                console.log('error = ', e)
            }
            if (data === 'Success') {
                alert('Добавлено успешно')
            } else {
                loadProcessedImage(parsed);
            }
        },
        error: function (err) {
            console.log('error =  ', err)
        }
    });
}

imageInput.addEventListener('input', () => {
    readImage();
})
document.querySelectorAll('[data-action]').forEach((button) => {
    button.addEventListener('click', () => {
        processImage(null,button.dataset.action)
    })
})
