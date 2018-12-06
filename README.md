# VNN -Visualize Neural Network-
## About
良いモデルの裏付け

## Process
1. index.html表示
2. inputから画像ファイル取得
3. test.jsでbase64に変換. ajaxでPOST
    - POST後はページ遷移をせず下部に表示される
4. Python(Flask)側で受け取ったデータをデコードしてget_answerに流す
5. get_answerで画素値の取得, グレイスケールへ変換を行いpredictionに流す
6. predictionで学習済みモデルを読み込み、kerasで検証
    - TODO: 検証前の処理を明らかにする。何が返ってくるのか
7. 検証結果の表示。数値 + 判別結果 + Grad-cam


