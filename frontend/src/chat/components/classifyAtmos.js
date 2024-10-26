export const classifyAtmos = async (file) => {
    try {
        // FormDataオブジェクトを作成
        const formData = new FormData();
        formData.append("img_file", file);

        // フォームデータを使用してPOSTリクエストを送信
        const response = await axios.post("http://localhost:8000/classify_atmos", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });

        console.log(response.data);

        // atmosを評価し、結果を設定
        const classifyResult = response.data.atmos === "positive" ? "明るい写真" : "暗い写真";
        const decorateMenu = response.data.decorateMenu;

        // 成功時にオブジェクトを返す
        return { classifyResult, decorateMenu };
    } catch (error) {
        console.error("Error:", error); // エラーをコンソールに表示
        return "error"; // エラー時に"error"を返す
    }
};
