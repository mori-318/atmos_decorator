export const createChatBubble = (role, contents) => {
    const chatContainer = document.querySelector("#chatContainer");
    const chatBubble = document.createElement("div");
    chatBubble.className = "col-6 chatBubble";

    // contents が画像の場合
    if (contents instanceof File && contents.type.startsWith("image/")) {
        return new Promise((resolve) => { // Promiseを返す
            const reader = new FileReader();
            reader.onload = function (event) {
                const imageElement = document.createElement("img");
                imageElement.src = event.target.result;
                imageElement.alt = "アップロードされた画像";
                imageElement.className = "uploadedImage";

                chatBubble.appendChild(imageElement);
                chatContainer.appendChild(chatBubble);
                resolve(); // 画像が読み込まれたらPromiseを解決
            };
            reader.readAsDataURL(contents); // ファイルを読み込む
        });
    }
    // contents がテキストメッセージの場合
    else if (contents.type === "text") {
        const textElement = document.createElement("p");
        textElement.className = "chatMessage";
        textElement.textContent = contents.content; // メッセージ内容を設定
        if (role === "user") chatBubble.classList.add("ml-auto");
        chatBubble.appendChild(textElement);
        chatContainer.appendChild(chatBubble);
    }
};