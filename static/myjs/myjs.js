function encodeImageFileAsURL(element) {
    const file = element.files[0];
    const reader = new FileReader();
    reader.onloadend = function () {
        base64 = reader.result;
        let x = $('#show_img')[0]
        x.src = base64
        x.removeAttribute('hidden')
    }
    reader.readAsDataURL(file);
}

function prettyPrint() {
    try {
        const ugly = document.getElementById('myTextArea').value;
        const obj = JSON.parse(ugly);
        document.getElementById('myTextArea').value = JSON.stringify(obj, undefined, 4);
    } catch (e) {
        console.log('json format error', e)
    }

}

function value_update(id) {
    let key = id.ariaLabel.replace('res-', '')
    json_res[key] = id.value;
    document.getElementById('myTextArea').value = JSON.stringify(json_res, undefined, 4);
    toastr.success(key + ' value change to ' + id.value, 'value change success')
}


function get_static_page(url, id) {
    $.ajax({
        url: url,
        type: 'get',
        contentType: false,
        processData: false,
        success: function (response) {
            const label = $('#' + id)[0];
            label.innerHTML = response
        },
    });
}

function post_pic_data() {
    if (base64) {
        const fd = new FormData();
        fd.append('img', base64)
        $.ajax({
            url: pic_url,
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                const label = $('#pic_res')[0];
                label.innerText = response['data']['raw_out']['ocr_result'][0]['simPred']
                toastr.success('image data crack success', 'requests success')
            },
        });
    }
}

function post_font_data() {
    toastr.info('start to crack font, please wait for prompting.')
    const files = $('#font-file')[0].files;
    const label = $('#image-groups')[0];
    const textarea = $('#json-textarea')[0];

    if (files.length > 0) {
        var fd = new FormData()
        fd.append('font_file', files[0])
        fd.append('type', 'html')
        $.ajax({
            url: font_url,
            type: 'post',
            data: fd,
            timeout: 400 * 1000,
            contentType: false,
            processData: false,
            async: true,
            success: function (response) {
                label.innerHTML = response['html'];

                json_res = response['font_dict']
                document.getElementById('myTextArea').value = JSON.stringify(response['font_dict'], undefined, 4);
                textarea.removeAttribute('hidden');
                toastr.success('font data crack success', 'requests success')
            },
            error: function () {
                alert('error')
            }
        });
    }
}