var textUploadBtn = document.getElementById('textUploadBtn');

// クリックイベントがバインドされているかどうか確認

if (textUploadBtn) {
    textUploadBtn.addEventListener('click', function() {
        console.log('ok');
        const chatDisplay = document.getElementById('chatDisplay');
        const div = document.createElement('div');
        const p = document.createElement('p');
        p.textContent = "新しい文字っすンご";
        div.appendChild(p);
        div.classList.add("userChat", "col-12", "col-md-6", "col-sm-12", "ml-auto");
        chatDisplay.appendChild(div);
    }, false);
} else {
    console.error('textUploadBtn が見つかりません');
}




//console.log('a')