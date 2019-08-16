const progress = document.getElementById("progress");
const progress_wrapper = document.getElementById('progress_wrapper');
const progress_status = document.getElementById('progress_status');

const submit_btn = document.getElementById('submit_btn') ;

const file_input = document.getElementById('file_input');
const file_input_label = document.getElementById('file_input_label');

const formElem = document.querySelector('form');

function upload(){
    var form = new FormData(formElem)
    var url = formElem.action

    var request = new XMLHttpRequest()

    request.addEventListener("loadstart", function(){
        file_input.disabled = true
        submit_btn.disabled = true
        console.log("upload start")
    })

    request.upload.addEventListener("progress", function(e){
        var loaded = e.loaded;
        var total = e.total;
        console.log(loaded);

        var percent = (loaded/total)*100;

        progress.style.width = `${Math.floor(percent)}%`;
        progress_status.innerText = `${Math.floor(percent)}%`;
    })


    request.addEventListener("load", function(){
        if (request.status == 200){
            progress_status.innerText = "Upload Complete";
            // progress.classList.remove("btn-primary")
            progress.classList.add("bg-success")
        }
        else{
            progress_status.innerText = "Upload Failed";
            // progress.classList.remove("btn-primary")
            progress.classList.add("bg-danger")
        }
    })

    request.responseType = "json";

    request.open("POST",url);
    request.send(form);
}

formElem.addEventListener("submit", function(e){
    e.preventDefault()
    upload()
})

function update_filename(){
    file_input_label.innerText = file_input.files[0].name;
}


