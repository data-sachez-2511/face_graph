const initialDataBase = JSON.parse(localStorage.getItem('imageDataBase')) || [];

window.database = initialDataBase;
