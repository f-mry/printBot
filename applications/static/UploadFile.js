console.log("hello world")

const form_element = document.querySelector('form');

const input_file = document.getElementById("input_file");
const input_label = document.getElementById("input_label");

const submit_btn = document.getElementById("submit_btn");

const progress_wrapper = document.getElementById("progress_wrapper");
const progress_bar = document.getElementById("progress_bar");

function update_filename(){
    input_label.innerText = input_file.files[0].name;
}

function upload(){
    var form = new FormData(form_element);
    var url = form_element.action;

    console.log(`URL: ${url}`);

    var request = new XMLHttpRequest()

    request.addEventListener("loadstart", function(){
        input_file.disabled = true;
        submit_btn.disabled = true;
        console.log("Upload start")
    })

    request.upload.addEventListener("progress", function(e){
        var loaded = e.loaded;
        var total = e.total;

        var percent = (loaded/total)*100;

        progress_bar.style.width = `${Math.floor(percent)}%`
    })

    request.addEventListener("load", function(){
        if (request.status == 200){
            console.log("Upload success")
        }
        else{
            console.log("Upload failed")
        }
    })

    request.open("POST", url);
    request.send(form)

}





