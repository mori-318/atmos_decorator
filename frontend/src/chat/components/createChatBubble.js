import { scrollBottom } from "./scrollBottom.js"

export const createChatBubble = (role, contents) => {
    const chatContainer = document.querySelector("#chatContainer");
    const chatBubble = document.createElement("div");
    chatBubble.className = "col-6 chatBubble";

    // デバッグ用ログ
    console.log('Role:', role);
    console.log('Contents:', contents);


    // File オブジェクトの場合（画像ファイルの場合）
    if (contents instanceof File && contents.type.startsWith("image/")) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = function (event) {
                const imageElement = document.createElement("img");
                imageElement.src = event.target.result;
                imageElement.alt = "アップロードされた画像";
                imageElement.className = "uploadedImage";

                chatBubble.appendChild(imageElement);
                chatContainer.appendChild(chatBubble);
                if (role === "user") chatBubble.classList.add("ml-auto");
                resolve();
            };
            reader.readAsDataURL(contents);
        });
    }
    // Base64形式の画像の場合
    else if (typeof contents === "string" && contents.startsWith("data:image/")) {
        const imageElement = new Image();
        imageElement.src = contents;
        imageElement.alt = "Base64で表示された画像";
        imageElement.className = "uploadedImage";

        if (role === "user") chatBubble.classList.add("ml-auto");
        chatBubble.appendChild(imageElement);
        chatContainer.appendChild(chatBubble);
    }
    // テキストメッセージの場合
    else if (contents.type === "text") {
        const textElement = document.createElement("p");
        textElement.className = "chatMessage";
        textElement.textContent = contents.content;
        if (role === "user") chatBubble.classList.add("ml-auto");
        chatBubble.appendChild(textElement);
        chatContainer.appendChild(chatBubble);
    }
    // その他のケース（エラー）
    else {
        const textElement = document.createElement("p");
        textElement.className = "chatMessage";
        textElement.textContent = "メッセージの表示に問題が発生しました";
        if (role === "user") chatBubble.classList.add("ml-auto");
        chatBubble.appendChild(textElement);
        chatContainer.appendChild(chatBubble);
    }

    scrollBottom();
};