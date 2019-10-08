$(function () {
    $('.add-saved-files').on('click', function () {
        $(this).parent().next('.cont-file').show()
    })
    $('.del-new-files').on('click', function () {
        $(this).closest('.cont-file').hide()
    })
    $('input[name="evidencias"]').on('change', function (e) {
        showFiles($(this), e.target.files)
    })
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
        tbody.append('<tr><td class=""><input type="text"></td><td><label class="secondary-content"><input type="checkbox" class="" value=""><span></span></label></td><td class="center-align"><a class="btn-small green save-new-obj" href="#"><i class="material-icons">check</i></a>&nbsp;<a class="btn-small red del-new-obj" href="#"><i class="material-icons">clear</i></a></td></tr>')
        let btns = tbody.children('tr').last().children('td').last().children('a')
        $(btns[0]).on('click', function (e) {
            e.preventDefault()
            let input = $(this).closest('tr').children('td').first().children('input')
            let checkbox = $($(this).closest('tr').children('td')[1]).find('input')
            let id_act = $(this).closest('.act-objs').attr('data-id')
            let badge = $(this).closest('li').find('div.collapsible-header > span.badge')
            if (input.val().trim().length === 0) {
                toastWarning('Debe de agregar un nombre de objetivo')
            }
            else {
                addNewObj(input, checkbox, id_act, badge, $(this))
            }
        })
        $(btns[1]).on('click', function (e) {
            e.preventDefault()
            $(this).closest('tr').remove()
        })
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
    $('.del-file').on('click', function (e) {
        e.preventDefault()
        Swal.fire({
            title: '¿Está seguro(a) de eliminar esta evidencia?',
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
                    toastWarning('Debe de agregar un nombre de actividad')
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
                    toastWarning('Debe de agregar un nombre de objetivo')
                }
            }
        })
    })
    $('.edit-dir').on('click', function (e) {
        e.preventDefault()
        alert('editando direcciónnnnn')
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
    $('.del-dir').on('click', function (e) {
        e.preventDefault()
        Swal.fire({
            title: '¿Está seguro(a) de eliminar esta dirección?',
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
    $('.add-comment').on('click', function (e) {
        e.preventDefault()
        Swal.fire({
            title: 'Comentarios de la actividad',
            html: `<div class="input-field"><textarea id="txta-comment" class="materialize-textarea">${$(this).attr('data-comment')}</textarea></div>`,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Guardar'
        }).then((result) => {
            if (result.value) {
                let new_comment = $('#txta-comment').val()
                if (new_comment != $(this).attr('data-comment')) {
                    editComment($(this).attr('href'), new_comment, $(this))
                }
                else {
                    toastWarning('El comentario es el mismo, no se guardó ningún cambio')
                }
            }
        })
    })
    $('.show-comment').on('click', function (e) {
        e.preventDefault()
        Swal.fire({
            title: 'Comentarios de la actividad',
            html: `<h6>${$(this).attr('data-comment')}</h6>`,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Cerrar'
        })
    })
    $('.cancel-act').on('click', function(){
       changeStatusAct($(this), $(this).attr('data-url'), $(this).prop('checked'))
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

function changeStatusAct(element, url, status) {
    $.ajax({
        method: "POST",
        url: url,
        data: { csrfmiddlewaretoken: getCSRFTokenValue(), status: status}
    }).done(function (result) {
        if (result.status === 'success') {
            toastSuccess(result.text)
            $(element).closest('.collapsible-body').siblings('.collapsible-header').toggleClass('cancelled')
        }
        else if (result.status === 'error') {
            toastError(result.text)
            status ? $(element).prop('checked', false) : $(element).prop('checked', true)
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

function editComment(url, comment, element) {
    $.ajax({
        method: "POST",
        url: url,
        data: { csrfmiddlewaretoken: getCSRFTokenValue(), comment: comment }
    }).done(function (result) {
        if (result.status === 'success') {
            toastSuccess(result.text)
            $(element).attr('data-comment', comment)
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

function showFiles(ele, files) {
    let ulFiles = ele.closest('.file-field').next('.collection')
    let max_size = 5242880 //5 megabytes
    ulFiles.empty()
    for (let i = 0; i < files.length; i++) {
        if (files[i].size <= max_size) {
            ulFiles.append(`<li class="collection-item">${files[i].name}</li>`)
        }
        else {
            ulFiles.append(`<li class="collection-item red-text">${files[i].name} - Excede el peso permitido</li>`)
            toastWarning('Archivos inválidos detectados. Por favor vuelva a elegirlos correctamente')
        }
    }
}

function getCSRFTokenValue() {
    var token = $('input[name="csrfmiddlewaretoken"]').val()
    return token
}

//form validators
function formRegisUser() {
    document.querySelector('#saveUser').addEventListener('click', function (e) {
        e.preventDefault()
        let formUser = document.querySelector('#formUser')
        let direction = formUser.querySelector('#id_direccion')
        let name = formUser.querySelector('#id_first_name')
        let last_name = formUser.querySelector('#id_last_name')
        let username = formUser.querySelector('#id_username')
        let password = formUser.querySelector('#id_password')
        if (direction.value === '0' || direction.value === '') {
            toastWarning('Debe de seleccionar una dirección')
        }
        else if (name.value.trim().length === 0) {
            toastWarning('Debe de ingresar su nombre')
        }
        else if (last_name.value.trim().length === 0) {
            toastWarning('Debe de ingresar su apellido')
        }
        else if (username.value.trim().length === 0) {
            toastWarning('Debe de ingresar un usuario')
        }
        else if (password.value.trim().length === 0) {
            toastWarning('Debe de ingresar una contraseña')
        }
        else {
            name.value = name.value.trim()
            last_name.value = last_name.value.trim()
            username.value = username.value.trim()
            password.value = password.value.trim()
            formUser.submit()
        }
    })
}

function formLogin() {
    document.querySelector('#accessLogin').addEventListener('click', function (e) {
        e.preventDefault()
        let formLogin = document.querySelector('#formLogin')
        let username = formLogin.querySelector('#username')
        let password = formLogin.querySelector('#password')
        if (username.value.trim().length === 0) {
            toastWarning('Debe de ingresar un usuario')
        }
        else if (password.value.trim().length === 0) {
            toastWarning('Debe de ingresar una contraseña')
        }
        else {
            username.value = username.value.trim()
            password.value = password.value.trim()
            formLogin.submit()
        }
    })
}

function formActivity() {
    document.querySelector('#save-act').addEventListener('click', function () {
        let formAct = document.querySelector('#act-form')
        let activity_name = formAct.querySelector('#act-name')
        let objs = formAct.querySelectorAll('#act-objs > table > tbody tr ')
        if (activity_name.value.trim().length === 0) {
            toastWarning('Debe de ingresar un nombre de actividad')
        }
        else if (objs.length === 0) {
            toastWarning('Debe de agregar al menos un objetivo en la actividad')
        }
        else {
            let verify = true
            if (objs.length > 0) {
                for (let i = 0; i < objs.length; i++) {
                    if (objs[i].querySelector('td').querySelector('input').value.trim().length === 0) {
                        objs[i].querySelector('td').querySelector('input').value = objs[i].querySelector('td').querySelector('input').value.trim()
                        verify = false
                        toastWarning('Debe de agregar un nombre al objetivo')
                        break
                    }
                }
                if (verify) {
                    for (let i = 0; i < objs.length; i++) {
                        objs[i].querySelector('td').querySelector('input').value = objs[i].querySelector('td').querySelector('input').value.trim()
                    }
                    activity_name.value = activity_name.value.trim()
                    formAct.submit()
                }
            }
        }
    })
}

function formDirection() {
    document.querySelector('#save-dir').addEventListener('click', function () {
        let formDir = document.querySelector('#dir-form')
        let name = formDir.querySelector('#id_nombre')
        let codename = formDir.querySelector('#id_codename')
        if (name.value.trim().length === 0) {
            toastWarning('Debe de ingresar un nombre de dirección')
        }
        else if (codename.value.trim().length === 0) {
            toastWarning('Debe de ingresar un codename')
        }
        else {
            name.value = name.value.trim()
            codename.value = codename.value.trim()
            formDir.submit()
        }
    })
}

function editUser() {
    document.querySelector('#change-avatar').addEventListener('click', function () {
        document.querySelector('#avatar-form').submit()
    })
    document.querySelector('#edit-name-user').addEventListener('click', function () {
        let form = document.querySelector('#name-user-form')
        let name = form.querySelector('#name')
        let last_name = form.querySelector('#last_name')
        if (name.value.trim().length === 0) {
            toastWarning('Debe de ingresar su nombre')
        }
        else if (last_name.value.trim().length === 0) {
            toastWarning('Debe de ingresar su apellido')
        }
        else {
            name.value = name.value.trim()
            last_name.value = last_name.value.trim()
            form.submit()
        }
    })
    document.querySelector('#change-pass').addEventListener('click', function (e) {
        e.preventDefault()
        let form = document.querySelector('#pass-form')
        let currentpass = form.querySelector('#current_pass')
        let newpass = form.querySelector('#new_pass')
        if (currentpass.value.trim().length === 0) {
            toastWarning('Debe ingresar su contraseña actual')
        }
        else if (newpass.value.trim().length === 0) {
            toastWarning('Debe de ingresar la nueva contraseña')
        }
        else {
            currentpass.value = currentpass.value.trim()
            newpass.value = newpass.value.trim()
            form.submit()
        }
    })
}












