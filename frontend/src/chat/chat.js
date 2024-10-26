// クリックイベントを適切に設定
var newtalk=document.getElementById('newtalk');


var textUploadBtn = document.getElementById('textUploadBtn');

if (textUploadBtn) {
    textUploadBtn.addEventListener('click', function() {
        console.log('ok');
        const chatDisplay = document.getElementById('chatDisplay');
        const div = document.createElement('div');
        const p = document.createElement('p');
        p.textContent = "新しい文字っすンご";
        div.appendChild(p);
        chatDisplay.appendChild(div);
        // p.textContent='';
        // textUploadBtn.value='';
    }, false);
} else {
    console.error('textUploadBtn が見つかりません');
}



//console.log('a')