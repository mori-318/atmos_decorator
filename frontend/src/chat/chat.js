document.addEventListener('DOMContentLoaded', function () {
    var
        dropArea = document.getElementById('dropArea'),
        output = document.getElementById('output'),

        // 画像の最大ファイルサイズ（20MB）
        maxSize = 20 * 1024 * 1024;

    // ドロップされたファイルの整理
    function organizeFiles(files) {
        var
            length = files.length,
            i = 0, file;

        for (; i < length; i++) {
            // file には Fileオブジェクト というローカルのファイル情報を含むオブジェクトが入る
            file = files[i];

            // 画像以外は無視
            if (!file || file.type.indexOf('image/') < 0) {
                continue;
            }

            // 指定したサイズを超える画像は無視
            if (file.size > maxSize) {
                continue;
            }

            // 画像出力処理へ進む
            outputImage(file);
        }
    }

    // 画像の出力
    function outputImage(blob) {
        var
            // 画像要素の生成
            image = new Image(),

            // File/BlobオブジェクトにアクセスできるURLを生成
            blobURL = URL.createObjectURL(blob);

        // src にURLを入れる
        image.src = blobURL;

        // 画像読み込み完了後
        image.addEventListener('load', function () {
            // File/BlobオブジェクトにアクセスできるURLを開放
            URL.revokeObjectURL(blobURL);

            // #output へ出力
            output.appendChild(image);
        });
    }

    // ドラッグ中の要素がドロップ要素に重なった時
    dropArea.addEventListener('dragover', function (ev) {
        ev.preventDefault();

        // ファイルのコピーを渡すようにする
        ev.dataTransfer.dropEffect = 'copy';

        dropArea.classList.add('dragover');
    });

    // ドラッグ中の要素がドロップ要素から外れた時
    dropArea.addEventListener('dragleave', function () {
        dropArea.classList.remove('dragover');
    });

    // ドロップ要素にドロップされた時
    dropArea.addEventListener('drop', function (ev) {
        ev.preventDefault();
v
        dropArea.classList.remove('dragover');
        output.textContent = '';

        // ev.dataTransfer.files に複数のファイルのリストが入っている
        organizeFiles(ev.dataTransfer.files);
    });

    // #dropArea がクリックされた時
    dropArea.addEventListener('click', function () {
        fileInput.click();
    });

    // ファイル参照で画像を追加した場合
    fileInput.addEventListener('change', function (ev) {
        output.textContent = '';

        // ev.target.files に複数のファイルのリストが入っている
        organizeFiles(ev.target.files);

        // 値のリセット
        fileInput.value = '';
    });
});
