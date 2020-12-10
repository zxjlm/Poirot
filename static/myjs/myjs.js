function encodeImageFileAsURL(element) {
        var file = element.files[0];
        var reader = new FileReader();
        reader.onloadend = function () {
            base64 = reader.result;
            let x = $('#show_img')[0]
            x.src = base64
            x.removeAttribute('hidden')
        }
        reader.readAsDataURL(file);
    }