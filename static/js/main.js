/*git commit을 위한 js 파일입니다. 파일명을 수정하셔도 되고 그냥 사용하셔도 됩니다.*/
function postDiary() {
    let title = $('#title').val()
    let content = $('#content').val()
    let image = $('#image')[0].files[0]

    let form_data = new FormData()

    form_data.append('title', title)
    form_data.append('content', content)
    form_data.append('image', image)

    $.ajax({
        type: "POST",
        url: "/diary/post",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response['msg'])
        }

    })

}