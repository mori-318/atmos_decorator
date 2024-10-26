import { createChatBubble } from "./components/createChatBubble.js";
import { scrollBottom } from "./components/scrollBottom.js";

window.onload = function () {
    const imgUploadButton = document.querySelector("#imgUploadButton");
    const textUploadButton = document.querySelector("#textUploadButton");
    const textBox = document.querySelector("#userInput");

    const fileInput = imgUploadButton.nextElementSibling; // 隠されたファイル入力
    let file = null; // 画像ファイルを格納する変数

    // ファイルアップロードボタンが押されたときの処理
    fileInput.addEventListener("change", async function () {
        file = fileInput.files[0]; // アップロードされたファイルを格納
        if (file && file.type.startsWith("image/")) {
            createChatBubble("host", {
                type: "text",
                content: "画像がアップロードされました",
            });
            await createChatBubble("host", file);
            createChatBubble("host", {
                type: "text",
                content: "画像の雰囲気分類中. . .",
            });
            textBox.placeholder = "画像がアップロードされました"; // プレースホルダーを変更
        } else {
            createChatBubble("host", {
                type: "text",
                content: "画像をアップロードしてください",
            });
        }
        fileInput.value = ""; // fileInputを空にする
        scrollBottom(); // 下までスクロールする
    });
};