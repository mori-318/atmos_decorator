export const imageDecorate = async (file, selectedDecorateMenus) => {
    try {
        // selectedDecorateMenusから余分な空白を取り除く
        selectedDecorateMenus = selectedDecorateMenus.replace(/\s+/g, "");

        // FormDataオブジェクトを作成
        const formData = new FormData();
        formData.append("img_file", file);
        formData.append("applied_filters", selectedDecorateMenus);

        console.log(formData);

        // フォームデータを使用してPOSTリクエストを送信
        const response = await axios.post("http://localhost:8000/apply_filters", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });

        console.log(response.data);

        // 成功時にオブジェクトを返す
        return response.data.imgFile;
    } catch (error) {
        console.error("Error:", error); // エラーをコンソールに表示
        return "error"; // エラー時に"error"を返す
    }
};