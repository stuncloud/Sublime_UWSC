Sublime UWSC
============

UWSC・[UWSCR](https://github.com/stuncloud/UWSCR)向けの入力補完およびシンタックスハイライトを行うパッケージ

入力補完 (UWSC/UWSCR)
--------

以下の入力補完を行います

- 組み込み関数
- 組み込み定数
- 特殊変数
- 特殊文字 (<#CR>、<#DBL>、<#TAB>)
- ブロック構文

シンタックスハイライト (UWSC/UWSCR)
----------------------

`.uws`ファイルに書かれたスクリプトに色付けを行います

ヘルプ参照 (UWSCのみ)
----------

スクリプト中の関数名にカーソルを合わせるか、選択状態にして`uwsc_help`コマンドを実行すると該当関数のヘルプを開きます  
この機能を有効にするには`Preferences.sublime-settings`の`uwsc_path`でUWSCのインストールディレクトリを指定しておく必要があります  

     "uwsc_path": "C:\\Program Files (x86)\\UWSC"

配列にすることで複数のパスを指定出来ます

     "uwsc_path":
     [
         "C:\\Program Files (x86)\\UWSC",
         "C:\\Program Files\\UWSC"
     ]
この場合は上から順に参照し、最初に見つかった`uwsc.chm`を開きます  
複数のPCで利用する場合などに有用です

