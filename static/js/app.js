$(function(){
    $('#add-objs').on('click', function(){
        $('#act-objs > table > tbody').append('<tr><td class="center-align"><input type="text" name="obj-name"></td><td><label class="secondary-content"><input type="checkbox" class="obj-check"/><span></span></label><input type="hidden" name="obj-check" value="false"/></td><td class="center-align"><a class="btn-small red del-objs"><i class="material-icons">delete</i></a></td></tr>')
        $('.del-objs').last().on('click', function(){
            $(this).closest('tr').remove()
        })
        $('.obj-check').last().on('change', function(){
            $(this).parent('label').siblings('input').val($(this).prop("checked"))
        })
    })
    $('#save-act').on('click', function(){
        $('#act-form').submit()
    })
    $('.del-obj').on('click', function(e){
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
    $('.obj-saved').on('change', function(){
        changeCheckObj($(this).val(), $(this).prop("checked"), $(this))
    })
});

function changeCheckObj(id, status_check, chck){
    $.ajax({
        method: "POST",
        url: "ajax/actividad/objetivo/editarcheck",
        data: { csrfmiddlewaretoken: getCSRFTokenValue(), id: id, status_check: status_check}
    }).done(function (result) {
        if (result.status === 'success') {
            toastSuccess(result.text)
            let badge = chck.closest('li').find('div.collapsible-header > span')
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

function registerUser(){
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

function getCSRFTokenValue(){
    var token = $('input[name="csrfmiddlewaretoken"]').val()
    return token
}