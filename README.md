# VNN -Visualize Neural Network-
## About
良いモデルの裏付け

## Process
1. index.html表示
2. inputから画像ファイル取得
3. app.jsからバイナリデータの状態でajaxでPOST
    - POST後はページ遷移をせず下部に表示される
4. Python(Flask)側で受け取ったデータをget_answerに流す
5. get_answerで配列に変換し, 画素値の取得, グレイスケールへ変換を行いpredictionに流す
6. predictionで学習済みモデルを読み込み、kerasで検証
    - TODO: 検証前の処理を明らかにする。何が返ってくるのか
7. 検証結果の表示。数値 + 判別結果 + Grad-cam


## Functions 
### hello.py
- result()
    - formから画像を取得
    - そのままget_result(req)に流す
    - get_answer()から帰ってきたものをjsに返す
    - 
- get_answer()
    - base64デコード(画像として読み込む)
        - load_image or pil
    - 前処理？？？
        - 前処理はpredict.pyでやろう！
    - arrayに変換
    - gradcam()に流す
    - gradcam()から帰ってきたもの(heatmap, result)をリサイズ
    - imgと重ね合わせる
    - base64にエンコード
    - result()に返却
    
### predict.py
- gradcam()
    - 前処理
    - 推論
    - 勾配の出力
    - ヒートマップ化
    - そのままget_answer()に返却

