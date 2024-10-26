var textUploadBtn = document.getElementById('textUploadButton');

if (textUploadBtn) {
    textUploadBtn.addEventListener('click', function() {
        console.log('ok');
        const chatDisplay = document.getElementById('border-chat');
        const div = document.createElement('div');
        const p = document.createElement('p');
        p.textContent = "新しい文字っすンご";
        div.appendChild(p);
        chatDisplay.appendChild(div);
    }, false);
} else {
    console.error('textUploadBtn が見つかりません');
}



//console.log('a')