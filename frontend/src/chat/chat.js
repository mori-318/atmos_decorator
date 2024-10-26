// クリックイベントを適切に設定
var newtalk=document.getElementById('newtalk');

if(newtalk){
    
    event.preventDefault();
}


var textUploadBtn = document.getElementById('textUploadBtn');

// クリックイベントがバインドされているかどうか確認
// if (textUploadBtn) {
//     textUploadBtn.addEventListener('click', function() {
//         console.log('ok');
//         const chatDisplay = document.getElementById('chatDisplay');
//         const div = document.createElement('div');
//         const p = document.createElement('p');
//         p.textContent = "新しい文字っすンご";
//         div.appendChild(p);
//         chatDisplay.appendChild(div);
//     }, false);
// } else {
//     console.error('textUploadBtn が見つかりません');
// }
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