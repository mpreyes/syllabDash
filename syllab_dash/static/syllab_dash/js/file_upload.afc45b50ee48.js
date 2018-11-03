

document.getElementById('files').addEventListener('change', function(e) {

    var list = document.getElementById('filelist');

    list.innerHTML = '';

    for (var i = 0; i < this.files.length; i++) {
      list.innerHTML +=  this.files[i].name + '\n';
    }
    if (list.innerHTML == '') list.style.display = 'none';
    else list.style.display = 'block';
  });

