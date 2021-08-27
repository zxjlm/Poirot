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
                if (response['code'] === 300) {
                    toastr.warning(response['msg'])
                } else {
                    const label = $('#pic_res')[0];
                    label.innerText = response['data']['raw_out']['ocr_result'][0]['simPred']
                    toastr.success('image data crack success', 'requests success')
                }
            },
        });
    }
}

function post_font_data() {

    const files = $('#font-file')[0].files;
    const label = $('#image-groups')[0];
    const textarea = $('#json-textarea')[0];

    label.innerHTML = '<div class="progress" style="margin-top: 100px">\n' +
        '        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="0"\n' +
        '             aria-valuemin="0" aria-valuemax="100" style="width: 0%" id="crack-progress"></div>\n' +
        '    </div>'
    textarea.setAttribute('hidden', true)

    if (files.length > 0) {
        toastr.info('start to crack font, please wait for prompting.')

        var fd = new FormData()
        fd.append('font_file', files[0])
        fd.append('type', 'html')

        const socket = io();

        //socket.on('connect', function () {
        // socket.emit('my_event', {data: 'I\'m connected!'});
        // toastr.success('connect success', '', {timeOut: 500})
        //});

        socket.on('my_response', function (msgs, cb) {

            if (msgs['data'].length > 0) {
                let progress = $('#crack-progress')[0];
                progress.style['width'] = msgs['width']
            }

            msgs['data'].forEach(function (msg) {
                toastr.success(msg, '', {timeOut: 1000})
            })
            if (cb)
                cb();
        });

        $.ajax({
            url: font_url,
            type: 'post',
            data: fd,
            timeout: 400 * 1000,
            contentType: false,
            processData: false,
            async: true,
            success: function (response) {
                if (response['code'] === 300) {
                    toastr.warning(response['msg'])
                } else if (response['code'] === 200) {
                    label.innerHTML = response['html'];

                    json_res = response['font_dict']
                    document.getElementById('myTextArea').value = JSON.stringify(response['font_dict'], undefined, 4);
                    textarea.removeAttribute('hidden');
                    toastr.success('font data crack success', 'requests success')
                } else {
                    toastr.error(response['msg'])
                }
            },
            error: function () {
                alert('error')
            },
            complete: function () {
                socket.emit('disconnect_request');
                socket.close()
            }
        });
    } else {
        toastr.error('没有文件是不行的')
    }
}

function post_digit_data() {
    const files = $('#font-file')[0].files;
    const label = $('#image-groups')[0];
    const textarea = $('#json-textarea')[0];

    label.innerHTML = '<div class="progress" style="margin-top: 100px">\n' +
        '        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="0"\n' +
        '             aria-valuemin="0" aria-valuemax="100" style="width: 0%" id="crack-progress"></div>\n' +
        '    </div>'
    textarea.setAttribute('hidden', true)

    if (files.length > 0) {
        toastr.info('start to crack font, please wait for prompting.')

        var fd = new FormData()
        fd.append('font_file', files[0])
        fd.append('type', 'html')

        $.ajax({
            url: digit_url,
            type: 'post',
            data: fd,
            timeout: 400 * 1000,
            contentType: false,
            processData: false,
            async: true,
            success: function (response) {
                if (response['code'] === 300) {
                    toastr.warning(response['msg'])
                } else if (response['code'] === 200) {
                    label.innerHTML = response['html'];

                    json_res = response['font_dict']
                    document.getElementById('myTextArea').value = JSON.stringify(response['font_dict'], undefined, 4);
                    textarea.removeAttribute('hidden');
                    toastr.success('font data crack success', 'requests success')
                } else {
                    toastr.error(response['msg'])
                }
            },
            error: function () {
                alert('error')
            },
            complete: function () {
            }
        });
    } else {
        toastr.error('没有文件是不行的')
    }
}