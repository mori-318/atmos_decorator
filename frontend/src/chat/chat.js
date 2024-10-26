import { createChatBubble } from "./components/createChatBubble.js";
import { classifyAtmos } from "./components/classifyAtmos.js";
import { imageDecorate } from "./components/imageDcorate.js";
import { downloadBase64Image } from "./components/dawnloadBase64Image.js";

window.onload = function () {
    const newChatButton = document.querySelector("#newChatButton");
    const imgUploadButton = document.querySelector("#imgUploadButton");
    const textUploadButton = document.querySelector("#textUploadButton");
    const textBox = document.querySelector("#userInput");

    const fileInput = imgUploadButton.nextElementSibling; // 隠されたファイル入力
    const textInput = textUploadButton.nextElementSibling;
    const newChat = newChatButton.nextElementSibling;

    let file = null; // 画像ファイルを格納する変数
    let decoratedImageFile = null; // 加工した画像を格納する変数

    // ファイルアップロードボタンが押されたときの処理
    fileInput.addEventListener("change", async function () {
        file = fileInput.files[0]; // アップロードされたファイルを格納

        // 変数の初期化
        decoratedImageFile = null;

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

            const { classifyResult, decorateMenus } = await classifyAtmos(file);
            if (classifyAtmos !== "error") {
                createChatBubble("host", {
                    type: "text",
                    content: `分類結果は ${classifyResult} でした!`,
                });

                createChatBubble("host", {
                    type: "text",
                    content: `雰囲気の加工法を "${decorateMenus.join(
                        ", "
                    )}" の中から選んで、入力してください※ もし、適用したい雰囲気加工法が複数ある場合は、コンマ区切りで入力してください`,
                });
            } else {
                createChatBubble("host", {
                    type: "text",
                    content: `分類に失敗しました。もう一度試してください. . .`,
                });

                file = null;
            }

            textBox.placeholder = "画像がアップロードされました"; // プレースホルダーを変更
        } else {
            createChatBubble("host", {
                type: "text",
                content: "画像をアップロードしてください",
            });
        }
        fileInput.value = ""; // fileInputを空にする
    });

    // ユーザー入力アップロードボタンが押されたときの処理
    textInput.addEventListener("click", async function () {
        let text = textBox.value;
        createChatBubble("user", {
            type: "text",
            content: text,
        });

        // 画像加工が終了している場合
        if (decoratedImageFile !== null) {
            // textから余分な空白を取り除く
            text = text.replace(/\s+/g, "");
            if (text.includes("はい")) {
                createChatBubble("host", {
                    type: "text",
                    content: "画像のダウンロードが開始されました。",
                });
                // ダウンロードリンクを作成
                try {
                    downloadBase64Image(
                        decoratedImageFile,
                        "frcorated_image.png"
                    );
                    createChatBubble("host", {
                        type: "text",
                        content: "画像のダウンロードが完了しました。",
                    });
                } catch (error) {
                    console.error(
                        "ダウンロードリンクの作成に失敗しました:",
                        error
                    );
                    createChatBubble("host", {
                        type: "text",
                        content:
                            "ダウンロードリンクの作成に失敗しました。もう一度試してください。",
                    });
                }
            } else {
                createChatBubble("host", {
                    type: "text",
                    content:
                        "ダウンロードはキャンセルされました。画面右上のアイコンから新しい会話を始めることが出来ます",
                });
            }
        } else if (file !== null) {
            createChatBubble("host", {
                type: "text",
                content: "画像の雰囲気加工中. . .",
            });
            decoratedImageFile = await imageDecorate(file, text); // スコープの修正
            if (decoratedImageFile !== "error") {
                createChatBubble("host", decoratedImageFile);
                createChatBubble("host", {
                    type: "text",
                    content:
                        "画像の雰囲気加工が完了しました。加工した画像をダウンロードしますか？(はい or いいえ)",
                });
            } else {
                createChatBubble("host", {
                    type: "text",
                    content:
                        "加工された画像が無効です。もう一度試してください。",
                });
                decoratedImageFile = null; // 成功しなかった場合は null に戻す
            }
        } else {
            createChatBubble("host", {
                type: "text",
                content: "先に、使用する画像をアップロードしてください",
            });
        }
        textBox.value = "";
    });

    // newChatButtonが押されたときの処理
    newChat.addEventListener("click", function () {
        window.location.reload(); // ページをリロード
    });
};
