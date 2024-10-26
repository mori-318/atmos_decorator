import { createChatBubble } from "./components/createChatBubble.js";
import { classifyAtmos } from "./components/classifyAtmos.js";
import { imageDecorate } from "./components/imageDcorate.js";

window.onload = function () {
    const imgUploadButton = document.querySelector("#imgUploadButton");
    const textUploadButton = document.querySelector("#textUploadButton");
    const textBox = document.querySelector("#userInput");

    const fileInput = imgUploadButton.nextElementSibling; // 隠されたファイル入力
    const textInput = textUploadButton.nextElementSibling; // 隠されたテキスト入力
    let file = null; // 画像ファイルを格納する変数
    let isClassifyFinished = false; //画像の雰囲気分類が終わったを格納する変数


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

            const {classifyResult, decorateMenu} = await classifyAtmos(file);
            if (classifyAtmos !== "error") {
                createChatBubble("host", {type:"text", content: `分類結果は ${classifyResult} でした!`})
                createChatBubble("host", {type:"text", content: `加工法を "${decorateMenu.join(", ")}" の中から選んで、入力してください`})
                createChatBubble("host", {type:"text", content: "※ もし、適用したい加工法が複数ある場合は、コンマ区切りで入力してください"})
                isClassifyFinished = true;
            }else {
                createChatBubble("host", {type:"text", content: `分類に失敗しました。もう一度試してください. . .`})
                isClassifyFinished = false;
            }

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


    // ユーザー入力アップロードボタンが押されたときの処理
    textInput.addEventListener("click", async function () {
        const text = textBox.value;
        createChatBubble("user", {
            type: "text",
            content: text,
        });

        // 画像分類が終了している場合
        if (isClassifyFinished) {
            decoratedImage = await imageDecorate(file, text)
        }
    });
};