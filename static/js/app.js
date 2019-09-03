$(function () {
    $('#add-objs').on('click', function () {
        $('#act-objs > table > tbody').append('<tr><td class="center-align"><input type="text" name="obj-name"></td><td><label class="secondary-content"><input type="checkbox" class="obj-check"/><span></span></label><input type="hidden" name="obj-check" value="false"/></td><td class="center-align"><a class="btn-small red del-objs"><i class="material-icons">delete</i></a></td></tr>')
        $('.del-objs').last().on('click', function () {
            $(this).closest('tr').remove()
        })
        $('.obj-check').last().on('change', function () {
            $(this).parent('label').siblings('input').val($(this).prop("checked"))
        })
    })
    $('.add-saved-objs').on('click', function () {
        let tbody = $(this).parent().siblings('.act-objs').find('table').find('tbody')
        tbody.append('<tr><td class=""><input type="text"></td><td><label class="secondary-content"><input type="checkbox" class="" value=""><span></span></label></td><td class="center-align"><a class="btn-small green save-new-obj" href="#"><i class="material-icons">check</i></a>&nbsp;<a class="btn-small red del-new-obj" href="#"><i class="material-icons">delete</i></a></td></tr>')
        let btns = tbody.children('tr').last().children('td').last().children('a')
        $(btns[0]).on('click', function (e) {
            e.preventDefault()
            let input = $(this).closest('tr').children('td').first().children('input')
            let checkbox = $($(this).closest('tr').children('td')[1]).find('input')
            let id_act = $(this).closest('.act-objs').attr('data-id')
            let badge = $(this).closest('li').find('div.collapsible-header > span.badge')
            addNewObj(input, checkbox, id_act, badge, $(this))
        })
        $(btns[1]).on('click', function (e) {
            e.preventDefault()
            $(this).closest('tr').remove()
        })
    })
    $('#save-act').on('click', function () {
        $('#act-form').submit()
    })
    $('.del-act').on('click', function (e) {
        e.preventDefault()
        Swal.fire({
            title: '¿Está seguro(a) de eliminar esta actividad?',
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí'
        }).then((result) => {
            if (result.value) {
                location.href = $(this).attr('href')
            }
        })
    })
    $('.edit-act').on('click', function (e) {
        e.preventDefault()
        let span = $(this).closest('li').find('.collapsible-header > span.act-name')
        Swal.fire({
            title: 'Editar actividad',
            html: `<input type="text" id="act-new-name" value="${span.text()}" >`,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Guardar'
        }).then((result) => {
            if (result.value) {
                let new_name = $('#act-new-name').val()
                if (new_name.length > 0) {
                    if (new_name != span.text()) {
                        editActName($(this).attr('href'), new_name, span)
                    }
                    else {
                        toastWarning('El nombre es el mismo, no se guardó ningún cambio')
                    }
                }
                else {
                    toastWarning('El nombre de la actividad no debe estar vacío')
                }
            }
        })
    })
    $('.edit-obj').on('click', function (e) {
        e.preventDefault()
        let td = $(this).closest('tr').children('td').first()
        Swal.fire({
            title: 'Editar objetivo',
            html: `<input type="text" id="obj-new-name" value="${td.text()}" >`,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Guardar'
        }).then((result) => {
            if (result.value) {
                let new_name = $('#obj-new-name').val()
                if (new_name.length > 0) {
                    if (new_name != td.text()) {
                        editObjName($(this).attr('href'), new_name, td)
                    }
                    else {
                        toastWarning('El nombre es el mismo, no se guardó ningún cambio')
                    }
                }
                else {
                    toastWarning('El nombre de la actividad no debe estar vacío')
                }
            }
        })
    })
    $('.del-obj').on('click', function (e) {
        e.preventDefault()
        Swal.fire({
            title: '¿Está seguro(a) de eliminar este objetivo?',
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí'
        }).then((result) => {
            if (result.value) {
                location.href = $(this).attr('href')
            }
        })
    })
    $('.obj-saved').on('change', function () {
        changeCheckObj($(this).val(), $(this).prop("checked"), $(this))
    })
});

function changeCheckObj(id, status_check, chck) {
    $.ajax({
        method: "POST",
        url: "ajax/actividad/objetivo/editarcheck",
        data: { csrfmiddlewaretoken: getCSRFTokenValue(), id: id, status_check: status_check }
    }).done(function (result) {
        if (result.status === 'success') {
            toastSuccess(result.text)
            let badge = chck.closest('li').find('div.collapsible-header > span.badge')
            badge.text(result.percent + '%')
            badge.css("background-color", result.color)
        }
        else if (result.status === 'error') {
            toastError(result.text)
        }
    }).fail(function () {
        console.log('Ha ocurrido un error inesperado :(')
    })
}

function editActName(url, name, span) {
    $.ajax({
        method: "POST",
        url: url,
        data: { csrfmiddlewaretoken: getCSRFTokenValue(), new_name: name }
    }).done(function (result) {
        if (result.status === 'success') {
            toastSuccess(result.text)
            span.text(name)
        }
        else if (result.status === 'error') {
            toastError(result.text)
        }
    }).fail(function () {
        console.log('Ha ocurrido un error inesperado :(')
    })
}

function editObjName(url, name, td) {
    $.ajax({
        method: "POST",
        url: url,
        data: { csrfmiddlewaretoken: getCSRFTokenValue(), new_name: name }
    }).done(function (result) {
        if (result.status === 'success') {
            toastSuccess(result.text)
            td.text(name)
        }
        else if (result.status === 'error') {
            toastError(result.text)
        }
    }).fail(function () {
        console.log('Ha ocurrido un error inesperado :(')
    })
}

function addNewObj(input, checkbox, act_id, badge, btn) {
    $.ajax({
        method: "POST",
        url: 'ajax/actividad/objetivo/agregar',
        data: { csrfmiddlewaretoken: getCSRFTokenValue(), obj_name: input.val(), obj_check: checkbox.prop("checked"), act_id: act_id }
    }).done(function (result) {
        if (result.status === 'success') {
            toastSuccess(result.text)
            input.after(input.val()).remove()
            checkbox.addClass('obj-saved').val(result.obj_value)
            checkbox.on('change', function () {
                changeCheckObj($(this).val(), $(this).prop("checked"), $(this))
            })
            badge.text(result.percent + '%')
            badge.css("background-color", result.color)
            let parent_td = btn.parent()
            parent_td.empty()
            parent_td.append(`<a class="btn-small red del-obj" href="${result.delete_url}"><i class="material-icons">delete</i></a>&nbsp;<a class="btn-small blue edit-obj" href="${result.edit_url}"><i class="material-icons">edit</i></a>`)
            let btns = parent_td.children('a')
            console.log(btns)
            $(btns[0]).on('click', function (e) {
                e.preventDefault()
                Swal.fire({
                    title: '¿Está seguro(a) de eliminar este objetivo?',
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Sí'
                }).then((result) => {
                    if (result.value) {
                        location.href = $(this).attr('href')
                    }
                })
            })
            $(btns[1]).on('click', function (e) {
                e.preventDefault()
                let td = $(this).closest('tr').children('td').first()
                Swal.fire({
                    title: 'Editar objetivo',
                    html: `<input type="text" id="obj-new-name" value="${td.text()}" >`,
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Guardar'
                }).then((result) => {
                    if (result.value) {
                        let new_name = $('#obj-new-name').val()
                        if (new_name.length > 0) {
                            if (new_name != td.text()) {
                                editObjName($(this).attr('href'), new_name, td)
                            }
                            else {
                                toastWarning('El nombre es el mismo, no se guardó ningún cambio')
                            }
                        }
                        else {
                            toastWarning('El nombre de la actividad no debe estar vacío')
                        }
                    }
                })
            })
        }
        else if (result.status === 'error') {
            toastError(result.text)
        }
    }).fail(function () {
        console.log('Ha ocurrido un error inesperado :(')
    })
}

function registerUser() {
    let img = document.getElementById('avatar');
    let file = document.getElementById('id_avatar');
    let fileReader = new FileReader();
    file.addEventListener('change', function (e) {
        fileReader.readAsDataURL(e.target.files[0]);
        fileReader.addEventListener('load', function () {
            img.src = fileReader.result;
            img.classList.remove('avatar-filter')
        });
    });
}

function getCSRFTokenValue() {
    var token = $('input[name="csrfmiddlewaretoken"]').val()
    return token
}