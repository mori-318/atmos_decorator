import { createChatBubble } from './components/createChatBubble.js';


const imgUploadButton = document.querySelector("#imgUploadButton");
const fileInput = imgUploadButton.nextElementSibling; // 隠されたファイル入力

// ファイルアップロードボタンが押されたときの処理
fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];
    if (file && file.type.startsWith("image/")) {
        createChatBubble("host", file);
    } else {
        const message = {
            type: "text",
            content: "画像をアップロードしてください"
        }
        createChatBubble("host", message);
    }
    fileInput.value = "" // fileInputを殻にする
});