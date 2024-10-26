const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// srcフォルダ内の静的ファイルを提供する設定
app.use(express.static(path.join(__dirname), {
    setHeaders: (res, filePath) => {
        if (filePath.endsWith('.css')) {
            res.setHeader('Content-Type', 'text/css');
        }
        if (filePath.endsWith('.js')) {
            res.setHeader('Content-Type', 'application/javascript');
        }
    }
}));

// ルーティング設定
app.get('/', (req, res) => {
    res.render(path.join(__dirname, 'home', 'home.ejs'));
});

app.get('/chat/', (req,res) => {
    res.render(path.join(__dirname, 'chat', 'chat.ejs'))
})

// サーバーの起動
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});