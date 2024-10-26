const chatContainer = document.querySelector("#chatContainer");

export const scrollBottom = () => {
    // 一番下までスクロールする
    chatContainer.scrollTop = chatContainer.scrollHeight;
};