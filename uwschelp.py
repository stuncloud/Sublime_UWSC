# coding: utf-8
import sublime
import sublime_plugin


class UwscHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        point = self.view.sel()[0].begin()
        if self.view.scope_name(point).find('source.uwsc') == -1:
            return
        word = self.view.word(point)
        name = self.view.substr(word).upper()
        help = self.get_help(name)
        window = self.view.window()
        output_view = window.get_output_panel("textarea")
        window.run_command("show_panel", {"panel": "output.textarea"})
        output_view.set_read_only(False)
        if int(sublime.version()) < 3000:
            edit = output_view.begin_edit()
            output_view.insert(edit, output_view.size(), help)
            output_view.end_edit(edit)
        else:
            output_view.insert(edit, output_view.size(), help)
        output_view.set_read_only(True)

    def get_help(self, word):
        if word in self.helps:
            w = self.helps[word]
            if type(w).__name__ == 'function':
                return w(self.helps)
            else:
                return w
        else:
            return u'UwscHelp: %s が見つかりませんでした' % word
    helps = {
'GETID': u'''
// 指定ウィンドウの ID を返す
戻値 = GETID( タイトル, [クラス名, 待ち時間秒, MDI子タイトル] )
引数
 タイトル： 識別したいウィンドウのタイトル （タイトルの一部分だけでもOK）
 クラス名： 区別に必要でなければ省略して構いません （前方一致でのみ部分指定可）
 待ち時間秒： 確認できるまで指定された秒数待ちます （0.01～）
         0： 0.1～10秒まで状況や負荷により自動判断 （デフォルト）
        -1： 無期限待ち
 MDI子タイトル： MDIウィンドウ中の子ウィンドウタイトル
戻値
 そのウィンドウを識別するID （NGの時は -1）
 ※ GETID は始めに完全一致のウィンドウを探します
   見つからなければ次に部分一致のウィンドウを探します
 ※ 特別なウィンドウの指定
   GETID(GET_ACTIVE_WIN)    // アクティブウィンドウを返します
      GET_FROMPOINT_WIN   // マウスカーソル下のウィンドウ
      GET_FROMPOINT_OBJ   // マウスカーソル下のオブジェクト
      GET_THISUWSC_WIN   // UWSC自身
      GET_LOGPRINT_WIN   // ログ表示用ウィンドウ
      GET_BALLOON_WIN   // ふきだし用ウィンドウ（GET_FUKIDASI_WIN でも可）
      GET_FORM_WIN     // フォーム画面ウィンドウ
      GET_SCHEDULE_WIN   // スケジュール"指定Windowが現れた時"でキャッチしたウィンドウ（'別プロセス実行'時はNG）
''',
'CLKITEM': u'''
// アイテムのクリック
// (ボタン,メニュー,チェックボックス,ラジオボタン,リストボックス,コンボボックス,タブコントロール,ビューリスト,ツールバー)
戻値 = CLKITEM( ID, アイテム名, [種別, On/Off, 番号] )
引数
 ID： Windowを識別するID
 アイテム名： ボタン、チェックボックス、ラジオボタンのキャプションの文字
        もしくは リストボックス、コンボボックスの選択名
        もしくは タブ名
        もしくは メニュー項目名
        もしくは ツリービュー項目、リストビュー項目
        もしくは ツールバー上のボタン名
 種別： チェックするアイテム種別
     CLK_BTN     // ボタン、チェックボックス、ラジオボタン
     CLK_LIST    // リストボックス、コンボボックス
     CLK_TAB     // タブコントロール
     CLK_MENU    // メニュー
     CLK_TREEVIEW  // ツリービュー （CLK_TREEVEW でも可）
     CLK_LISTVIEW  // リストビュー （CLK_LSTVEW でも可）
     CLK_TOOLBAR   // ツールバー
     CLK_ACC     // アクセシビリティ用インターフェース経由によるクリック
     追加オプション
     CLK_SHORT    // 文字省略指定： 部分一致にて検索 （例：CLK_LIST or CLK_SHORT）
     CLK_BACK    // バックグランド実行： ウィンドウをアクティブ化しません
     CLK_MUSMOVE   // マウス移動： マウスをその場所に移動します（CLK_MOUSEMOVE でも可）
     CLK_RIGHTCLK  // 右クリック： アイテムにより右クリックの動作をします
     CLK_LEFTCLK   // 左クリック： アイテムにより左クリックの動作をします
     CLK_DBLCLK   // ダブルクリック： 2段目のクリック動作（1段目としてCLK_LEFTCLK が必要）
     CLK_FROMLAST  // 後ろからサーチ： CLK_ACC 指定時にアイテムを後ろからサーチ
     CLK_CONTINUE  // 前回地点からサーチ： CLK_ACC 指定時に前回の実行地点からサーチ
 On/Off：チェックボックス,メニューでのチェック、およびクリック動作 True=On、False=Off（デフォルトはOn）
 番号： 同名のアイテム名がある場合のオブジェクト順番 （左上から数えたオブジェクト順番[１から指定]）
戻値
 TRUE：正常、 FALSE：処理不能

 ※ アイテム名の最後に付く ニーモニック[(&A)、(&B)...、(&C):等]は要りません
 ※ 種別：省略時は BTN ->LIST ->TAB ->MENU ->TREEVEW ->LSTVEW ->TOOLBAR ->ACC の順でサーチ
 ※ メニュー,ツリービュー： \ にてパス指定表記可（例：TOP\TEMP\FILE ）ぶつかる物がなければパス指定は不要
 ※ リストボックス： 複数選択の場合は タブにて アイテム名を繋げる
''',
'CHKBTN': u'''
// ボタン類（チェックボックス、ラジオボタン）の状態を返す
戻値 = CHKBTN( ID, アイテム名, [番号, ACC指定] )
引数
 ID： Windowを識別するID
 アイテム名： ボタン、チェックボックス、ラジオボタンのキャプションの文字
 番号： 同名がある場合のオブジェクト順番 （左上から数えた順番[１から指定]）
 ACC指定：
    FALSE： APIによる （デフォルト）
    TRUE： アクセシビリティ用インターフェースを利用
    2：   アクセシビリティ用インターフェースを利用（ウィンドウをアクティブ化しない）
戻値
 -1： 存在しないか無効状態
 0 ： OFF
 1 ： ON
 2 ： チェックボックスにて淡色状態
''',
'CTRLWIN': u'''
// Window コントロール
CTRLWIN( ID, 命令 )
引数
 ID： Windowを識別するID
 命令
  CLOSE     // 終了
  CLOSE2    // 終了（QUIT）
  ACTIVATE   // アクティブ
  HIDE     // 非表示
  SHOW     // 表示
  MIN      // アイコン化
  MAX      // 最大化
  NORMAL    // サイズ戻す
  TOPMOST    // 最前面に固定
  NOTOPMOST  // 最前面固定を解除
  TOPNOACTV  // 最前面にするがアクティブ化はしない
''',
'SENDSTR': u'''
// 文字列の送信
SENDSTR( ID, 文字列, [番号, 送信モード, ACC指定] )
引数
 ID： Windowを識別するID
    （ID = 0 であれば クリップボードへ）
 文字列： 送りたい文字列
 番号： 左上から数えたエディトコントロールの順番 （１から指定、マイナスを付けた場合にはDisable状態のものもカウント）
     （0:デフォルトはフォーカスを持ったエディトコントロール）
 送信モード：
    FALSE： 追加 （デフォルト）
    TRUE： 置き換え
    2：   一文字ずつ送信 （PostMessage,WM_CHAR）
 ACC指定：
    FALSE： APIによる （デフォルト）
    TRUE： アクセシビリティ用インターフェースを利用
    2：   アクセシビリティ用インターフェースを利用（ウィンドウをアクティブ化しない）
''',
'GETSTR': u'''
// 文字列の取得
戻値 = GETSTR( ID, [番号, 種別, マウス移動] )
引数
 ID： Windowを識別するID
    （ID = 0 であれば クリップボードから）
 番号： 左上から数えたコントロールの順番 （１から指定、マイナスを付けた場合にはDisable状態のものもカウント）
     （0:デフォルトはフォーカスを持ったコントロール）
     （ステータスバー指定時はパーツ）
 種別：
    STR_EDIT (0)    // エディトコントロール （デフォルト）
    STR_STATIC (1)   // スタティクコントロール
    STR_STATUS (2)   // ステータスバー
    STR_ACC_EDIT (3)  // アクセシビリティ用インターフェース経由でのエディト内文字
    STR_ACC_STATIC (4) // アクセシビリティ用インターフェース経由でのスタティク文字
 マウス移動：
    FALSE： マウス移動なし（デフォルト）
    TRUE： マウスをその場所に移動させる
戻値
 取得した文字列
 （指定物が存在しない場合には EMPTYを返す）
''',
'GETITEM': u'''
// キャプション文字やリスト等を全て取得する
戻値 = GETITEM( ID, 種別, [番号, リストビュー列, ディセーブルフラグ] )
引数
 ID： Windowを識別するID
 種別： (複数指定可)
   ITM_BTN     // ボタン、チェックボックス、ラジオボタン
   ITM_LIST    // リストボックス、コンボボックス
   ITM_TAB     // タブコントロール
   ITM_MENU    // メニュー
   ITM_TREEVIEW  // ツリービュー （ITM_TREEVEW でも可）
   ITM_LISTVIEW  // リストビュー （ITM_LSTVEW でも可）
   ITM_EDIT    // エディトボックス
   ITM_STATIC   // スタティク
   ITM_STATUSBAR  // ステータスバー
   ITM_TOOLBAR   // ツールバー
   ITM_ACCCLK    // アクセシビリティ経由でのクリック可能な物
   ITM_ACCCLK2   // アクセシビリティ経由でのクリック可能な物（選択可のテキストも含める）
   ITM_ACCTXT    // アクセシビリティ経由でのテキスト
   ITM_BACK     // ITM_ACCCLK、ITM_ACCTXT  指定時にアクティブにしない
 番号：ITM_LIST、ITM_TREEVIEW、ITM_LISTVIEW 複数存在時は左上からの順番を指定（-1にて全コントロール取得）
 リストビュー列： リストビュー指定時のリストビューの列を指定 （-1にてカラム名取得）
 ディセーブル：
    FALSE： ディセーブルな物も取得 （デフォルト）
    TRUE： ディセーブルな物はを取得しない
戻値
 取得した数を返す
 取得した情報は配列変数の ALL_ITEM_LIST[ ] に格納される （配列はゼロから）
''',
'GETSLCTLST': u'''
// COMBOBOX, LISTBOX, ITM_LISTVIEW, ITM_TREEVIEW での選択項目を取得する
戻値 = GETSLCTLST( ID, [番号, リストビュー列] )
引数
 ID： Windowを識別するID
 番号： 左上から数えたエディトコントロールの順番 （１から指定）
 リストビュー列： リストビュー時のリストビューの列を指定
戻値
 選択されている項目 （複数選択されている場合はタブにて結合される）
''',
'SETSLIDER': u'''
// スライダー(トラックバー、スクロールバー)の値を設定する
戻値 = SETSLIDER( ID, 値, [番号] )
引数
 ID： Windowを識別するID
 値： 設定する値
 番号： 左上からのコントロールの順番 （１から指定）
戻値
 TRUE：正常, FALSE：処理不能

 ※ 値として定数 GET_SLIDER が設定された場合には値の取得として機能し値を返す
''',
'GETSLIDER': u'''
// スライダー(トラックバー、スクロールバー)の値を取得する
戻値 = GETSLIDER( ID, [番号, パラメータ] )
引数
 ID： Windowを識別するID
 番号： 左上からのコントロールの順番 （１から指定）
 パラメータ：
   SLD_POS (0)   // 値（デフォルト）
   SLD_MIN     // 最小値
   SLD_MAX     // 最大値
   SLD_PAGE     // 1ページ移動量
   SLD_BAR     // 表示が縦か横か 0:横、1:縦
   SLD_X      // X（クライアント位置）
   SLD_Y      // Y（クライアント位置）
戻値
 取得した値
''',
'SCKEY': u'''
// ショートカットキーの実行
SCKEY( ID, キー, [キー, キー, キー, ...] )
引数
 ID： Windowを識別するID
 キー： アルファベット１文字もしくは仮想キー(VK_*)
 ※ 動作としてVK_SHIFT, VK_CTRL, VK_ALT, VK_WIN のキー指定は押し下げ状態のまま処理する
   指定するウィンドウがない場合には IDに 0を指定
''',
'GETALLWIN': u'''
// 全ウィンドウの IDを取得
戻値 = GETALLWIN( [ID] )
引数
 ID： 指定ウィンドウの子ウィンドウを取得したい場合に、親ウィンドウIDを指定
戻値
 取得したWindowの数
 取得したIDは配列変数の ALL_WIN_ID[ ] に格納される （配列はゼロから）
''',
'STATUS': u'''
// ウィンドウの各種状態を返す
戻値 = STATUS( ID, 取得したいもの )
引数
 ID： Windowを識別するID
 取得したいもの： 以下の定数
   ST_TITLE    // タイトルを返す
   ST_CLASS    // クラス名を返す
   ST_X      // X座標を返す
   ST_Y      // Y座標を返す
   ST_WIDTH    // 幅を返す
   ST_HEIGHT    // 高さを返す
   ST_CLX     // クライアント領域のX座標を返す
   ST_CLY     // クライアント領域のY座標を返す
   ST_CLWIDTH   // クライアント領域の幅を返す
   ST_CLHEIGHT   // クライアント領域の高さを返す
   ST_PARENT    // 親ウィンドウのIDを返す、親が無ければ-1
   ST_ICON     // アイコン状態であればTrue、でなければFalse
   ST_MAXIMIZED  // 最大化状態であればTrue、でなければFalse
   ST_VISIBLE   // 通常の表示状態であればTrue、でなければFalse
   ST_ACTIVE    // アクティブ状態であればTrue、でなければFalse
   ST_BUSY     // ビジー状態であればTrue、でなければFalse
   ST_ISID     // 有効なIDであればTrue、でなければFalse
   ST_WIN64    // 64bitアプリであればTrue、でなければFalse
   ST_PATH     // EXEのパスを返す
   ST_PROCESS   // プロセスIDを返す
   ST_MONITOR   // 表示されているモニタ番号を返す
''',
'MOUSEORG': u'''
// マウス座標を相対座標にする、 またはマウスとキー情報を直接ウィンドウへ送る
MOUSEORG( ID, [基準指定, 画面取得指定 ] )
引数
 ID： Windowを識別するID
 基準指定：
   0 (デフォルト)： ウィンドウ位置
   MORG_CLIENT (1)： クライアント領域の位置を基準にする
   MORG_DIRECT (2)： 指定ウィンドウ(オブジェクト)へマウス、キー情報を直接送る（第1引数はウィンドウIDでもハンドル値でも可）
 画面取得指定： PEEKCOLOR()、CHKIMG()関数にて
   0 (デフォルト)： 指定アプリがフォアグランドかバックグランドかにより検索画面の取得方法を変更
   MORG_FORE   ： フォアグランドとして可視画面(デスクトップ)を検索画面とする
   MORG_BACK   ： バックグランドとしてアプリより画面を取得して検索画面とする（他の画面がオーバーラップしていてもOK）
 ※ 以降のMMV()、BTN()、PEEKCOLOR()、CHKIMG()関数の座標を指定ウィンドウを基準にしたものにする
 ※ 基準指定にて MORG_DIRECTが指定された場合は KBD()、MMV()、BTN()関数の情報は直接ウィンドウ(オブジェクト)へ送る
 ※ スクリーン座標に戻す時はゼロを指定 MOUSEORG(0)
 ※ 有効範囲はスレッド単位
''',
'PEEKCOLOR': u'''
// 指定位置の色を得る
戻値 = PEEKCOLOR( X, Y, [RGB指定, クリップボード指定] )
引数
 X、Y： 座標 X、Y
 RGB指定：
   0：    BGR値にて返す （デフォルト）
   COL_RGB： RGB値にて返す
   COL_R：  赤の成分のみを返す
   COL_G：  緑の成分のみを返す
   COL_B：  青の成分のみを返す
 クリップボード指定：
   FALSE： 画面より （デフォルト）
   TRUE： クリップボードより
戻値
 指定位置の色情報

 ※ BGR値 例) 青：$FF0000、緑：$00FF00、赤：$0000FF、オレンジ：$0080FF、黄：$00FFFF
 ※ RGB値 例) 赤：$FF0000、緑：$00FF00、青：$0000FF、オレンジ：$FF8000、黄：$FFFF00
''',
'CHKIMG': u'''
// 指定画像が画面上にあるかチェック、あればその情報を返す
戻値 = CHKIMG( [画像名, 透過色/色無視, x1, y1, x2, y2, 番号, 色幅] )
引数
 画像名： 画像ファイル名（BMP形式のみ） （画像名を省略した場合はクリップボードから）
 透過色/色無視：
      0： 指定なし （デフォルト）
      1： 左上、2:右上、3:左下、4:右下 の１ピクセルの色を透過色として処理
     -1： 色を無視して形でチェックする
 x1, y1, x2, y2： サーチ範囲
 番号： 複数ある場合に順番を指定 （左上から）
     -1： -1が指定された場合はヒットした数を戻値として返し、座標情報は ALL_IMG_X[], ALL_IMG_Y[] に格納
        （G_IMG_X、 G_IMG_Y には最後にヒットした位置が入る）
 色幅： チェックに色幅を持たせる （色無視指定時もしくは 16bitカラー以下の場合は無効）
     IMG_MSK_BGR1： 各色(BGR)に対し 2/256の色幅を許す
     IMG_MSK_BGR2： 各色(BGR)に対し 4/256の色幅を許す
     IMG_MSK_BGR3： 各色(BGR)に対し 8/256の色幅を許す
     IMG_MSK_BGR4： 各色(BGR)に対し 16/256の色幅を許す
     IMG_MSK_B1, 2, 3, 4 ： 青に対し 2/256, 4/256, 8/256, 16/256の色幅を許す
     IMG_MSK_G1, 2, 3, 4 ： 緑に対し 2/256, 4/256, 8/256, 16/256の色幅を許す
     IMG_MSK_R1, 2, 3, 4 ： 赤に対し 2/256, 4/256, 8/256, 16/256の色幅を許す
      ※ 演算可 例：IMG_MSK_B1 or IMG_MSK_R3（青に対し 2/256の色幅を許す + 赤に対し 8/256の色幅を許す）
戻値
 有ればTRUE、無ければFALSE
 TRUE の場合は見つかった座標を特殊変数 G_IMG_X、 G_IMG_Y に格納
 番号にて -1指定時はヒットした数を返し、座標情報は配列変数 ALL_IMG_X[], ALL_IMG_Y[] に格納（配列はゼロから）
''',
'SAVEIMG': u'''
// 画像の保存
SAVEIMG( [画像名, ID, x, y, 幅, 高さ, クライアント指定, JPEG指定, 画面取得指定] )
引数
 画像名： 保存ファイル名（BMP/JPEG形式） （画像名を省略した場合はクリップボードへ）
 ID： Windowを識別するID （0 であればスクリーン全体）
 X, Y： 位置
 幅, 高さ： 大きさ
 クライアント指定：
   FALSE： 指定ウィンドウ全体 （デフォルト）
   TRUE： クライアント領域
 JPEG指定： 1(高圧縮)～100(低圧縮) までの圧縮率を指定すると JPEGにて保存、 0(デフォルト)は BMPにて保存
 画面取得指定：
   0 (デフォルト)： 指定アプリがフォアグランドかバックグランドかにより画面の取得方法を変更
   IMG_FORE    ： フォアグランドとして可視画面(デスクトップ)より画面を取得
   IMG_BACK    ： バックグランドとしてアプリより画面を取得
''',
'MUSCUR': u'''
// マウスカーソル種別を返す
戻値 = MUSCUR( )
引数 なし
戻値
  CUR_APPSTARTING （1） // 砂時計付き矢印カーソル
  CUR_ARROW （2）    // 標準矢印カーソル
  CUR_CROSS （3）    // 十字カーソル
  CUR_HAND （4）     // ハンドカーソル（Windows2000以降）
  CUR_HELP （5）     // クエスチョンマーク付き矢印カーソル
  CUR_IBEAM （6）    // アイビーム（縦線）カーソル
  CUR_NO （8）      // 禁止カーソル
  CUR_SIZEALL （10）   // ４方向矢印カーソル
  CUR_SIZENESW （11）  // 斜め左下がりの両方向矢印カーソル
  CUR_SIZENS （12）   // 上下両方向矢印カーソル
  CUR_SIZENWSE （13）  // 斜め右下がりの両方向矢印カーソル
  CUR_SIZEWE （14）   // 左右両方向矢印カーソル
  CUR_UPARROW （15）   // 垂直の矢印カーソル
  CUR_WAIT （16）    // 砂時計カーソル
 ※ ユーザー定義カーソルはハンドル値をマイナスにして返す（起動毎に変化）
''',
'POSACC': u'''
// 座標位置の文字（情報）を取得する
戻値 = POSACC( ID, クライアント座標X, クライアント座標Y, [モード] )
引数
 ID： Windowを識別するID （スクリーン全体の場合は 0）
 座標： クライアント座標 （ID= 0 の場合はスクリーン座標）
 モード：
   0         // （デフォルト） ACC_ACCの実行、取得ができなければACC_API を実行
   ACC_ACC      // 表示文字の取得 （アクセシビリティ用インターフェース使用）
   ACC_API      // DrawText, TextOutなどのAPIをトラップ （WinXP以上、64bitアプリNG）
   ACC_NAME      // 名前  （アクセシビリティ用インターフェース使用）
   ACC_VALUE     // 値   （アクセシビリティ用インターフェース使用）
   ACC_ROLE     // 役割  （アクセシビリティ用インターフェース使用）
   ACC_STATE     // 状態  （アクセシビリティ用インターフェース使用）
   ACC_DESCRIPTION  // 説明  （アクセシビリティ用インターフェース使用）
   ACC_LOCATION   // X,Y,幅,高さ（アクセシビリティ用インターフェース使用）
   ACC_BACK      // ウィンドウをアクティブ化しない （他モードに付加して使用）
戻値
 取得した文字（情報）
''',
'INPUT': u'''
// インプットボックス
戻値 = INPUT( 表示メッセージ, [デフォルト値, パスワードフラグ, X, Y] )
引数
 表示メッセージ： インプットボックスに表示するメッセージ
 デフォルト値： デフォルトの値 として表示
 パスワードフラグ： TRUE にすると文字は全てアスタリスク表示 （デフォルト FALSE）
 X, Y： 表示位置 （デフォルトは中央）
戻値
 入力されたデータ
 （キャンセル時はEMPTY）
 ※ ファイルドロップによりファイル名の設定可 （複数選択時はタブにて結合される）
''',
'MSGBOX': u'''
// メッセージボックス
戻値 = MSGBOX( メッセージ, [表示ボタン, X, Y, フォーカスボタン] )
引数
 メッセージ： 表示メッセージ
 表示ボタン： ボタン種別 （複数指定可、デフォルトはBTN_OK）
       BTN_YES, BTN_NO, BTN_OK, BTN_CANCEL, BTN_ABORT(中止), BTN_RETRY(再試行), BTN_IGNORE(無視)
 X、Y： 表示位置 X、Y （デフォルトは画面中央）
 フォーカスボタン： デフォルトとしてフォーカスを与えるボタン種別
戻値
 押されたボタン種別
''',
'SLCTBOX': u'''
// セレクトボックス
戻値 = SLCTBOX( 種別, タイムアウト秒, [メッセージ], 項目, [項目, 項目, ...] )
 もしくは
戻値 = SLCTBOX( 種別, タイムアウト秒, x, y, [メッセージ], 項目, [項目, 項目, ...] )
引数
 種別：
   SLCT_BTN   // ボタン
   SLCT_CHK   // チェックボックス
   SLCT_RDO   // ラジオボタン
   SLCT_CMB   // コンボボックス
   SLCT_LST   // リストボックス
   SLCT_STR   // 戻り値を項目名で返す （他の種別に付加して使用）
   SLCT_NUM   // 戻り値を位置数で返す （他の種別に付加して使用）
 タイムアウト： 指定時間（秒）を過ぎるとゼロを返します （0指定でタイマーは無効）
 x, y： 第3引数と第4引数が数値であれば X位置,Y位置指定と判断します （省略型は中央表示）
 メッセージ： 表示メッセージ
 項目： 選択項目名  （配列変数で渡す事も可）
戻値
 １つ目が選択されたならば SLCT_1 が返される
 ２つ目が選択されたならば SLCT_2 が返される
         ：
 SLCT_CHK （チェックボックス）選択時はビット演算して返される
 SLCT_STR 付加時は項目名で返される （複数選択時はタブにて結合される）
 SLCT_NUM 付加時は位置数で返される （複数選択時はタブにて結合される）
 ※ 閉じボタンによる終了時は-1を返してくる （SLCT_CHKにてビットチェックする場合は注意）
 ※ 項目数は最大31まで （SLCT_STR、SLCT_NUM の場合は制限なし）
''',
'POPUPMENU': u'''
// ポップアップメニュ
戻値 = POPUPMENU( メニュ項目, [X, Y] )
引数
 メニュ項目： 表示メニュ項目を配列変数にて渡す
       （サブメニュは { } にて指定： a,b,{c, d},e の場合は c,dがbのサブメニュになる）
 X、Y： 表示位置 X、Y （デフォルトはマウス位置）
戻値
 選択された項目の配列変数位置
''',
'FUKIDASI': lambda dic: dic['BALLOON'],
'BALLOON': u'''
// 吹出し
BALLOON( メッセージ, x, y, [向き, フォントサイズ, フォント名, 文字色, 背景色, 透明化] )
 もしくは
FUKIDASI( メッセージ, x, y, [向き, フォントサイズ, フォント名, 文字色, 背景色, 透明化] )
引数
 メッセージ： 表示メッセージ
 x, y： 位置
 向き： 0：嘴なし, 1：上嘴, 2：下嘴, 3：左嘴, 4：右嘴
 フォントサイズ： 文字フォントサイズ
 フォント名： フォント名
 文字色： BGR値にて指定
 背景色： BGR値にて指定
 透明化： 0：不透明 ～ 255：透明、 -1：バックを透明化、 -2：外枠も非表示
 BALLOON() 引数無しにて吹出し消去
 ※ 有効範囲はスレッド単位
 ※ 背景色に黒を指定する場合は 0ではなく1を指定（0はデフォルトの黄）
 ※ BGR値 例) 青：$FF0000、緑：$00FF00、赤：$0000FF、オレンジ：$80FF、黄：$FFFF
''',
'LOGPRINT': lambda dic: dic['STOPFORM'],
'STOPFORM': u'''
// UWSCが再生時に出すウィンドウの表示/非表示
STOPFORM( 表示フラグ, [x, y] )        // 再生中に出るSTOPボタンウィンドウ
LOGPRINT( 表示フラグ, [x, y, 幅, 高さ] )  // PRINT文により出るログウィンドウ
引数
 表示フラグ： TRUE：表示、 FALSE：非表示
 x, y： 表示位置
 幅, 高さ： 幅, 高さ
''',
'MONITOR': u'''
// マルチモニタ情報
戻値 = MONITOR( モニタ番号, 取得情報 )
引数
 モニタ番号： モニタ番号を指定 (メインモニタは 0）
 取得情報：
   MON_X      // X座標を返す
   MON_Y      // Y座標を返す
   MON_WIDTH    // 幅を返す
   MON_HEIGHT    // 高さを返す
 ※ MONITOR() 引数なしの場合はモニターの数を返す
''',
'EXEC': u'''
// アプリの起動
戻値 = EXEC( exe名, [同期フラグ, X, Y, 幅, 高さ] )
引数
 exe名： 起動したいアプリ名
 同期フラグ：
   FALSE： 待たない （デフォルト）
   TRUE： そのアプリが終了するまで待つ
 X： Window位置X
 Y： Window位置Y
 幅：  Window幅
 高さ： Window高さ
戻値
 そのWindowを識別するID を返す
 終了待ちが指定された場合は、そのアプリの終了コードを返す
 ※ 注：Explorer等の別プロセスを呼ぶものは、期待どおりに戻値を返さない事がある
''',
'SLEEP': u'''
// スリープ
SLEEP( 秒 )
引数
 秒： スリープする秒数（最小=0.001）
''',
'DOSCMD': u'''
// コマンドライン(コマンドプロンプト)の実行
戻値 = DOSCMD( コマンド, [同期フラグ, 画面表示, UNICODE出力] )
引数
 コマンド： コマンドプロンプトのコマンド
 同期フラグ：
   FALSE： 終了を待つ （デフォルト）
   TRUE： 待たずに戻る
 画面表示：
   FALSE： コマンドプロンプト画面を表示しない （デフォルト）
   TRUE： 表示する
 UNICODE出力：
   FALSE： ANSIにて出力 （デフォルト）
   TRUE： UNICODEにて出力
戻値
 標準出力を返す （同期フラグがTrue、もしくは画面表示がTrueの場合は返しません）
''',
'POWERSHELL': u'''
// POWERSHELLの実行
戻値 = POWERSHELL( コマンド, [同期フラグ, 画面表示] )
引数
 コマンド： POWERSHELLのコマンド
 同期フラグ：
   FALSE： 終了を待つ （デフォルト）
   TRUE： 待たずに戻る
 画面表示：
   FALSE： POWERSHELL画面を表示しない （デフォルト）
   TRUE： 表示する
   2：   最小化状態で起動する
戻値
 標準出力を返す （同期フラグがTrue、もしくは画面表示がTrue,2の場合は返しません）
''',
'SOUND': u'''
// サウンドの再生
SOUND( ファイル名, [同期フラグ] )
引数
 ファイル名： 再生ファイル名 （WAV, MID, AVI等、 'BEEP' 指定にてBEEP音）
        もしくはサウンドにて割り当てられたイベント名（'LowBatteryAlarm', 'MailBeep', 'SystemAsterisk'等）
       （ファイル名を省略すると再生をストップ）
 同期フラグ：
   FALSE： 待たない （デフォルト）
   TRUE： 終了を待つ
 ※ 'BEEP'指定時：32bitOSではPC内部スピーカだが、64bitOSでは通常のサウンド出力
''',
'GETTIME': u'''
// 日付、時間の取得（時間変数に時間を設定する）
戻値 = GETTIME( [±n日, 基準日] )
引数
 ±n日： nを指定すると当日もしくは基準日からプラスマイナス n日とする、小数点以下は時間（デフォルト=0）
 基準日： 指定された日付を基に日付を設定する （デフォルト=当日）
      （"YYYYMMDD" or "YYYY/MM/DD" or "YYYY-MM-DD" or "YYYYMMDDHHNNSS" or "YYYY/MM/DD HH:NN:SS"）
戻値
 2000年１月１日からの秒数を返す
 値がセットされる特殊変数
  G_TIME_YY    // 年
  G_TIME_MM    // 月
  G_TIME_DD    // 日
  G_TIME_HH    // 時
  G_TIME_NN    // 分
  G_TIME_SS    // 秒
  G_TIME_ZZ    // ミリ秒
  G_TIME_WW    // 曜日 （0：日曜....6：土曜）
  G_TIME_YY2   // 年をxxの文字型
  G_TIME_MM2    // 月をxxの文字型
  G_TIME_DD2   // 日をxxの文字型
  G_TIME_HH2   // 時をxxの文字型
  G_TIME_NN2   // 分をxxの文字型
  G_TIME_SS2   // 秒をxxの文字型
  G_TIME_ZZ2   // ミリ秒をxxxの文字型
  G_TIME_YY4   // 年をxxxxの文字型
''',
'POFF': u'''
// 電源断/サスペンド/モニタOff
POFF( コマンド )
引数
 コマンド：
   P_POWEROFF    // 電源断
   P_LOGOFF     // ログオフ
   P_REBOOT     // リブート
   P_SUSPEND     // サスペンド  （休止状態）
   P_SUSPEND2    // サスペンド2 （スタンバイ）
   P_MONIPOWER   // モニターOFF （省電力モード）
   P_MONIPOWER2   // モニターOFF （電源断）
   P_MONIPOWER3   // モニターON
   P_SCREENSAVE   // スクリーンセーバ起動
   P_UWSC_REEXEC  // UWSCの再起動 （第2引数を True指定するとスクリプト再実行）
   P_FORCE      // 強制実行：他コマンド(POWEROFF,LOGOFF,REBOOT)に付加して使用  例）強制電源断：P_POWEROFF or P_FORCE
''',
'KINDOFOS': u'''
// ＯＳ種別
戻値 = KINDOFOS( [64bit確認フラグ] )
引数
 64bit確認フラグ：
   FALSE： OS種別を示す番号を返す（デフォルト）
   TRUE： OSが 32bit / 64bit かを返す
戻値
 64bit確認フラグ=FALSE（デフォルト）： OS種別を示す番号
  10：NT3.5、 11：NT4、 12：Win2000、 13：WinXP、 14：Server2003
  20：Vista、 21：Server2008、 22：Windows 7、 23：Windows 8、 24：Server2012、 25：Windows 8.1
 64bit確認フラグ=TRUE： TRUE（64bit OS）/ FALSE（32bit OS）
''',
'CPUUSERATE': u'''
// CPU使用率
戻値 = CPUUSERATE( )
戻値
 CPU使用率  （分解能１秒）
''',
'GETKEYSTATE': u'''
// キークリック、トグルキー情報
戻値 = GETKEYSTATE( キーコード )
引数
 キーコード： 状態を知りたいキーコード
戻値
 TRUE：クリックがあった、 FALSE：なし
 ※マウスクリック VK_RBUTTON （右）、VK_LBUTTON（左）、VK_MBUTTON（中）
 ※トグルキー状態 TGL_IME （IME）、TGL_NUMLOCK （NumLock）、TGL_CAPSLOCK（CapsLock）
          TGL_SCROLLLOCK （ScrollLock）、TGL_KANALOCK（カタカナ）
''',
'SETHOTKEY': u'''
// ホットキーの設定
戻値 = SETHOTKEY( キーコード, [修飾子キー, Procedure名] )
引数
 キーコード： 使用するキーコード
 修飾子キー： （省略可、複数指定可）
        MOD_ALT(Alt), MOD_CONTROL(Ctrl), MOD_SHIFT(Shift), MOD_WIN(Win)
 Procedure名： UWSC側の呼び出される Procedure名
        省略された場合にはホットキーの解除
戻値
 TRUE：成功、 FALSE：失敗
 ※Procedure内にて変数 HOTKEY_VK にキーコード、HOTKEY_MOD に修飾子キー が格納されている
''',
'LOCKHARD': u'''
// ハードウェア（キーボード、マウス）からの入力禁止
LOCKHARD( 禁止フラグ )
引数
 禁止フラグ： TRUE：入力禁止、 FALSE：解除
 ※ 管理者権限が必要
 ※ 強制解除が必要な場合は Ctrl + Alt + Delete
''',
'LOCKHARDEX': u'''
// キーボード、マウスからの入力禁止
LOCKHARDEX( ID, [モード] )
引数
 ID： 入力禁止にしたいウィンドウID、 0 が指定された場合は全体を禁止
 モード：
   0：      キーボード、マウスとも禁止 （デフォルト）
   LOCK_KEYBOARD：キーボードのみ禁止
   LOCK_MOUSE：  マウスのみ禁止
 LOCKHARDEX() 引数無しにて入力禁止を解除
 ※ 禁止中は KBD, BTN関数は無効
 ※ 強制終了が必要な場合は タスクマネージャを起動(Ctrl+Alt+Delete)して、UWSC.exeを終了
''',
'EVAL': u'''
// 文字列を評価し値を返す
戻値 = EVAL( 文字列 )
引数
 文字列： 評価(実行)する文字列
戻値
 結果得られた値を返す
 ※ A = B は比較演算として処理、代入式の場合は A := B とする
''',
'GETCTLHND': u'''
// ボタン等、オブジェクトのハンドルをゲットする
戻値 = GETCTLHND( ID, アイテム名, [番号] )
引数
 ID： Windowを識別するID
 アイテム名： ボタン類のキャプション文字、もしくはオブジェクトのクラス名
 番号： 同じアイテム名がある場合に番号指定
戻値
 ハンドル値
 ※ GETCTLHND(ID,GET_MENU_HND) とするとメニュハンドルを返す
   GETCTLHND(ID,GET_SYSMENU_HND) とするとシステムメニュハンドルを返す
''',
'HNDTOID': lambda dic: dic['IDTOHND'],
'IDTOHND': u'''
// ID<->ハンドル変換
ハンドル = IDTOHND( ID )   // IDをAPI等で利用する為にハンドル値に変換
ID = HNDTOID( ハンドル )   // ハンドル値をUWSC用にIDに変換
''',
'VARTYPE': u'''
// 変数の型を返す、もしくは型を変換する
戻値 = VARTYPE( 変数, [変換タイプ] )
引数
 変数： 型を調べる変数
 変換タイプ： 型を変換する場合にタイプ指定
戻値
 型
  VAR_EMPTY （0）   // Empty
  VAR_NULL （1）   // Null
  VAR_SMALLINT （2） // ２バイト整数（符号付）
  VAR_INTEGER （3）  // ４バイト整数（符号付）
  VAR_SINGLE （4）  // 単精度浮動小数点値
  VAR_DOUBLE （5）  // 倍精度浮動小数点値
  VAR_CURRENCY （6） // 通貨型
  VAR_DATE （7）   // 日付型
  VAR_BSTR （8）   // 文字列型
  VAR_DISPATCH（9）  // オブジェクト
  VAR_ERROR （10）  // エラー値
  VAR_BOOLEAN （11） // ブール型
  VAR_VARIANT （12） // バリアント
  VAR_UNKNOWN （13） // 未定義のオブジェクト
  VAR_SBYTE （16）  // １バイト整数（符号付）
  VAR_BYTE （17）   // １バイト整数（符号なし）
  VAR_WORD （18）   // ２バイト整数（符号なし）
  VAR_DWORD （19）  // ４バイト整数（符号なし）
  VAR_INT64 （20）  // ８バイト整数（符号付）
  VAR_ARRAY（8192[$2000]） // 配列
 変換タイプが指定された場合には、変換されて値を返す
''',
'MMV': u'''
// マウス移動
MMV( x, y, [ms] )
引数
 x, y： 位置
 ms： 実行までの待ち時間 （ミリセカンド）
''',
'BTN': u'''
// マウスボタン
BTN( ボタン, 状態, [x, y, ms] )
引数
 ボタン：LEFT, RIGHT, MIDDLE, WHEEL(ホイール回転)
 状態：CLICK(0), DOWN(1), UP(2)  WHEEL指定時はノッチ数
 x, y： 位置 （省略時は現在位置にて）
 ms： 実行までの待ち時間 （ミリセカンド）
''',
'BTN': u'''
// キーボード
KBD( 仮想KEY, [状態, ms] )
引数
 仮想KEY： 仮想KEYコード、もしくはUNICODE
 状態：CLICK（0：デフォルト), DOWN(1), UP(2)
 ms： 実行までの待ち時間 （ミリセカンド）
''',
'ACW': u'''
// ウィンドウ状態変更
ACW( ID, x, y, [幅, 高さ, ms] )
引数
 ID： Windowを識別するID
 x, y： Window位置
 幅, 高さ： Window幅, 高さ
''',
'COPYB': lambda dic: dic['COPY'],
'COPY': u'''
// 文字列コピー
戻値 = COPY( 文字列, 開始位置, [コピー文字数] )
引数
 文字列： コピー元の文字列
 開始位置： コピーすべき文字列の開始位置 （１から）
 コピー文字数： コピーすべき文字数 （省略時は最後の文字まで）
戻値
 結果の文字列
 ※ バイト処理の場合は COPYB
''',
'POSB': lambda dic: dic['POS'],
'POS': u'''
// 文字列に指定文字列があるか探す
戻値 = POS( 探す文字, 探される文字列, [n個目] )
引数
 探す文字： 探したい文字列
 探される文字列： 探される文字列
 n個目： nを指定するとn個目の文字位置を返す（マイナス値で指定すると後ろからサーチ）
戻値
 見つかった位置 （１から）
 （見つからなければゼロを返す）
 （大文字,小文字の区別はしません）
 ※ バイト処理の場合は POSB
''',
'LENGTHB': lambda dic: dic['LENGTH'],
'LENGTH': u'''
// 文字数を返す （もしくは配列サイズ）
戻値 = LENGTH( 文字列 )
引数
 文字列： 数える文字列 （もしくは配列変数）
戻値
 文字数 （配列変数時は配列サイズを返す)
 ※ バイト処理の場合は LENGTHB
''',
'CHKNUM': u'''
// 数値であるかをチェック
戻値 = CHKNUM( 文字列 )
引数
 文字列： チェックする文字列
戻値
 数値であればTRUE、でなければFALSE
''',
'VAL': u'''
// 文字型を数値に変える
戻値 = VAL( 文字列, [エラー値] )
引数
 文字列： 数値に変える文字列
 エラー値： 数値に変換できない場合に返す値
戻値
 数値
 数値変換できない場合はエラー値を、デフォルトでは ERR_VALUE （-999999）を返す
''',
'CHGMOJ': lambda dic: dic['REPLACE'],
'REPLACE': u'''
// 指定文字列を置換する
戻値 = REPLACE( 文字列, 置換したい文字, 置換文字 )
 もしくは
戻値 = CHGMOJ( 文字列, 置換したい文字, 置換文字 )
引数
 文字列： 置換したい文字列を含んだ文字列
 置換したい文字： 置換したい文字列
 置換文字： 置換文字列
戻値
 置換された文字列
 （大文字,小文字の区別はしません）
''',
'TRIM': u'''
// 文字の両端の空白と制御文字を取り除く
戻値 = TRIM( 文字列, [全角空白] )
引数
 文字列： 文字列
> 全角空白：
   FALSE： 全角の空白は含めない （デフォルト）
   TRUE： 全角の空白を含めて削除
戻値
 両端の空白と制御文字が取り除かれた文字列
''',
'FORMAT': u'''
// フォーマット
戻値 = FORMAT( 数値, 幅, [小数点桁 or 16進指定] )
引数
 数値： 数値 もしくは文字
 幅： 出力される文字数 （数値より指定幅が大きい時は左側をスペースにて補完）
    数値ではなく文字が指定された場合は その文字で幅分を埋める
 小数点桁 or 16進指定： 表示する小数点桁数、 また -1 が指定された場合は16進数表記にする
戻値
 フォーマットされた文字列
''',
'CHRB': lambda dic: dic['CHR'],
'CHR': u'''
// 文字コードから文字を返す
戻値 = CHR( 文字コード )
引数
 文字コード： UNICODE
戻値
 文字
 ※ バイト処理の場合は CHRB
''',
'ASCB': lambda dic: dic['ASC'],
'ASC': u'''
// 文字から文字コードを返す
戻値 = ASC( 文字 )
引数
 文字： 先頭の１文字を処理
戻値
 UNICODE
 ※ バイト処理の場合は ASCB
''',
'ISUNICODE': u'''
// 文字列にUNICODE専用文字（SJISに無い文字）が含まれているかを調べる
戻値 = ISUNICODE( 文字列 )
引数
 文字列： 調べる文字列
戻値
 TRUE：あり、 FALSE：なし（SJISに変換できる）
''',
'STRCONV': u'''
// 文字列を変換する （大文字小文字、かなカナ、全角半角）
戻値 = STRCONV( 文字列, 変換指定 )
引数
 文字列： 変換する文字列
 変換指定：
   SC_LOWERCASE   // 小文字
   SC_UPPERCASE    // 大文字
   SC_HIRAGANA    // ひらがな
   SC_KATAKANA    // カタカナ
   SC_HALFWIDTH    // 半角文字
   SC_FULLWIDTH    // 全角文字
戻値
 変換された文字列
''',
'TOKEN': u'''
// トークンの切り出し （指定文字で区切ったものを返す）
戻値 = TOKEN( 区切文字, var 文字列, [ 区切方法, ダブルコーテイション ] )
引数
 区切文字： 文字列を区切る文字を指定（1文字単位で認識、"#$%" の場合は '#','$','%' の3つが区切り文字になる）
 文字列： 文字列は区切られた後、残りの文字列を返す
 区切方法：
   FALSE： 区切り文字が連続していた場合でも一つずつ取り出す （デフォルト）
   TRUE： 区切り文字が連続していた場合に連続した部分は削除
 ダブルコーテイション：
   FALSE： "ダブルコーテイション"内も無視して区切る （デフォルト）
   TRUE： "ダブルコーテイション"の文字は区切らない
戻値
 結果の文字列
''',
'BETWEENSTR': u'''
// 指定文字列間の文字列を返す
戻値 = BETWEENSTR( 文字列, 前文字, 後文字, [n個目, 数え方フラグ] )
引数
 文字列： 探す元になる文字列
 前文字： 得たい文字列の前にある文字列 （省略した場合は先頭から）
 後文字： 得たい文字列の後にある文字列 （省略した場合は最後まで）
 n個目： nを指定するとn個目の該当文字列を返す（マイナス値で指定すると後ろからサーチ）
 数え方フラグ：
   FALSE： n個目は後文字以降でカウント （デフォルト）
   TRUE： n個目は前文字以降でカウント
戻値
 前文字と後文字に挟まれている文字列 （取得できなかった場合はEMPTYを返す）
''',
'RESIZE': u'''
// 配列のサイズを変更する
戻値 = RESIZE( 配列変数, [サイズ] )
引数
 配列変数： 配列変数名
 サイズ： 配列の上限値 （多次元配列の場合は一番上の次元に対してのみ）
戻値
 配列の上限値を返す   （配列サイズのみを得る場合に第２引数は省略）
''',
'SETCLEAR': u'''
// 配列を指定された値で埋める
SETCLEAR( var 配列変数, [値] )
引数
 配列変数： 配列変数名
 値： 埋める値   （デフォルトは EMPTY）
''',
'SHIFTARRAY': u'''
// 配列データをシフトする
SHIFTARRAY( var 配列変数, シフト値 )
引数
 配列変数： 配列変数名
 シフト値： 値だけ配列を後ろへシフトする、マイナス値の場合は前方シフト（空いた場所は EMPTYで埋められる）
''',
'CALCARRAY': u'''
// 配列データを計算
戻値 = CALCARRAY( 配列変数, 計算法, [開始, 終了] )
引数
 配列変数： 配列変数名
 計算法：
   CALC_ADD   // 合計値
   CALC_MIN    // 最小値
   CALC_MAX   // 最大値
   CALC_AVR   // 平均値
 開始, 終了： 計算する開始位置、終了位置の添え字を指定
戻値
 計算による値
''',
'SPLIT': u'''
// 文字列を区切り配列を作成し返す
戻値 = SPLIT( 文字列, [区切文字列, 空文字処理フラグ, 数値処理フラグ] )
引数
 文字列： 区切り文字列を含んだ文字列
 区切文字列： 区切る為の文字列 （省略時はスペース）
 空文字処理フラグ：
   FALSE： 空文字も有効 （デフォルト）
   TRUE： 空文字は無効として処理しない
 数値処理フラグ：
   FALSE： 数値以外も有効 （デフォルト）
   TRUE： 数値以外は無効として空文字に変更する
戻値
 作成された一次元配列（SAFEARRAY型）
''',
'JOIN': u'''
// 配列の中身を区切文字で結合し文字列として返す
戻値 = JOIN( 配列変数, [区切文字列, 空文字処理フラグ, 開始, 終了] )
引数
 配列変数： 配列変数名
 区切文字列： 結合に使用する区切文字列 （省略時はスペース）
 空文字処理フラグ：
   FALSE： 空文字も有効 （デフォルト）
   TRUE： 空文字は無効として処理しない
 開始, 終了： 結合する配列の開始位置、終了位置の添え字を指定
戻値
 作成された文字列
''',
'SLICE': u'''
// 配列の中を指定範囲の配列で返す
戻値 = SLICE( 配列変数, [開始, 終了] )
引数
 配列変数： 配列変数名
 開始, 終了： 取り出す配列の開始位置、終了位置の添え字を指定
戻値
 作成された一次元配列（SAFEARRAY型）
''',
'QSORT': u'''
// 配列の中身をソートする
QSORT( var キー配列, [順列, var 配列, var 配列, ...] )
引数
 キー配列： ソートされる配列変数名
 順列：
   0： 昇順 （デフォルト）
   1： 降順
   2： 昇順 （UNICODE文字比較）
   3： 降順 （UNICODE文字比較）
 配列： 配列変数名、キー配列のソートと連動
''',
'FOPEN': u'''
// ファイル オープン
戻値 = FOPEN( ファイル名, [オープンモード] )
引数
 ファイル名： テキストファイル名
 オープンモード： 以下の方法で指定
   F_READ        // 読み専用モード（デフォルト） SJIS、UTF8、UTF16に対応
   F_WRITE      // 書き専用モード（既にファイルがあれば前の情報は消去）
              （UNICODEがある場合に UTF8、無い場合にはSJISになる）
   F_READ or F_WRITE // 読み書き両用指定
   F_EXISTS      // ファイル存在チェック（ファイルオープンせずにファイルが存在するかを返す）
              （ディレクトリをチェックしたい場合は最後に \を付加）
  追加指定
   F_EXCLUSIVE     // 排他制御 （排他制御の読み書き： F_READ or F_WRITE or F_EXCLUSIVE）
   F_TAB        // CSV処理に対しカンマではなくタブを使用
   F_NOCR       // 書き込みにてファイルの最後の改行は付加しない （F_WRITE or F_NOCR）
  ※ 文字コードを指定したい場合は、F_WRITE の代わりに以下を指定する
   F_WRITE8：UTF8、 F_WRITE8B：BOM付きUTF8、 F_WRITE16：UTF16、 F_WRITE1：SJIS
戻値
 ファイルID
 オープンできなかった場合は-1 を返す
 F_EXISTS 指定時は TRUE（在り）/ FALSE（無し）を返す
''',
'FGET': u'''
// ファイル 読み込み
戻値 = FGET( ファイルID, 行, [列, ダブルコーテイション] )
引数
 ファイルID： オープン時に返されたID
 行： 取出したい行 （１から指定）
     F_LINECOUNT  を指定した場合はファイルの行数を返す
     F_ALLTEXT   を指定した場合はファイルの全内容を返す
 列： 取出したい列 （１から指定：,カンマ区切りのCSVファイルに対応）
 ダブルコーテイション：
   FALSE： 両端のダブルコーテイションは削除する （デフォルト）
   TRUE： 削除しない
   2：   CSV処理にて２つ連続ダブルコーティションを１つに (Excel同等処理)
戻値
 取出された値
''',
'FPUT': u'''
// ファイル 書き込み
FPUT( ファイルID, 書込み値, [行, 列] )
引数
 ファイルID： オープン時に返されたID
 書込み値： 書込み内容
 行： 書込み行 （１から指定）
     0 （デフォルト）で行末に追加
     F_ALLTEXT を指定した場合は行ではなくファイルの全内容として書き込む
 列： 書込み列 （１から指定：,カンマ区切りのCSVファイルに対応）
    F_INSERT  を指定した場合は指定行に挿入
 ※ 注：実際にファイルが更新されるのは FCLOSEが呼ばれた時です
''',
'FDELLINE': u'''
// ファイル 指定行の削除
FDELLINE( ファイルID, 行 )
引数
 ファイルID： オープン時に返されたID
 行： 削除行 （１から指定）
''',
'FCLOSE': u'''
// ファイル クローズ
戻値 = FCLOSE( ファイルID, [エラー処理] )
引数
 ファイルID： オープン時に返されたID
 エラー処理：
   FALSE： エラー時はエラーダイアログを出す （デフォルト）
   TRUE： エラーダイアログを出さない
戻値
 TRUE：正常終了、 FALSE：エラー有り
''',
'GETDIR': u'''
// ファイル名の取得
戻値 = GETDIR( ディレクトリ, [ファイル指定, 不可視ファイルフラグ, 取得順番] )
引数
 ディレクトリ： ファイル名の取得のディレクトリ
 ファイル指定： ワイルドカード(*, ?) によるファイル名指定
         "\" を指定するとディレクトリ名の取得
 不可視ファイルフラグ： TRUE：不可視ファイルも含める、 FALSE：含めない（デフォルト）
 取得順番： ファイル並び 0:ファイル名(UNICODE順:デフォルト)、1:サイズ、2:作成日、3:更新日、4:アクセス日、5:ファイル名(ロケール指定順)
戻値
 ゲットした数を返す
 取得した情報は配列変数の GETDIR_FILES[ ] に格納される （配列はゼロから）
''',
'DROPFILE': u'''
// ファイルをウィンドウにドロップする
DROPFILE( ID, ディレクトリ, ファイル名, [ファイル名, ファイル名, ...] )
引数
 ID： ドロップする相手先
 ディレクトリ： ファイルのあるディレクトリ
 ファイル名： ドロップするファイル名 （配列変数で渡す事も可）
''',
'READINI': u'''
// INIファイル 読み込み
戻値 = READINI( セクション, キー, [INIファイル名] )
引数
 セクション： セクション名
 キー： キー名
 INIファイル名： デフォルト(省略時)では、カレントディレクトリに スクリプト名.INI
戻値
 取得した値
''',
'WRITEINI': u'''
// INIファイル 書き込み
WRITEINI( セクション, キー, 値, [INIファイル名] )
引数
 セクション： セクション名
 キー： キー名
 値： 書き込む値
 INIファイル名： デフォルト(省略時)では、カレントディレクトリに スクリプト名.INI
''',
'DELETEINI': u'''
// INIファイル キーの削除
DELETEINI( セクション, [キー, INIファイル名] )
引数
 セクション： セクション名
 キー： 削除するキー名 （キーを指定しなかった場合にはセクションごと削除）
 INIファイル名： デフォルト(省略時)では、カレントディレクトリに スクリプト名.INI
''',
'CREATEOLEOBJ': u'''
// COMオブジェクト生成
戻値 = CREATEOLEOBJ( COMオブジェクト名 )
引数
 COMオブジェクト名： COMオブジェクト名
戻値
 COMオブジェクト
 ※ COMからメソッド使用時に引数に値取得(OUT引数)がある場合は、引数の変数の前に Var を付ける
''',
'GETACTIVEOLEOBJ': u'''
// 既に起動中のCOMオブジェクトに対してのアクセス
戻値 = GETACTIVEOLEOBJ( COMオブジェクト名, [タイトル, 順番] )
引数
 COMオブジェクト名： COMオブジェクト名
 タイトル： 複数時にタイトルで区別(一部でOK)
       Excel, Access, Wordの場合はファイル名を指定  ※IE,Office以外では無効
 順番： IEにてタイトルが同じ時に区別 （-1が指定された時は最新(一番最後に起動)のもの） ※IEのみ有効
戻値
 COMオブジェクト
''',
'GETOLEITEM': u'''
// コレクションの取得
戻値 = GETOLEITEM( コレクションプロパティ名 )
引数
 コレクションプロパティ名： COMオブジェクト.コレクション取得プロパティ名
戻値
 ゲットしたコレクションの数
 取得した物は配列変数の ALL_OLE_ITEM[ ] に格納される （配列はゼロから）
''',
'OLEEVENT': u'''
// イベント処理の定義
OLEEVENT( オブジェクト, インタフェース名, イベント名, Procedure名 )
引数
  オブジェクト： COMオブジェクト
  インタフェース名： ディスパッチ インタフェース名
  イベント名： イベント名
  Procedure名： UWSC側の呼び出される Procedure名
 ※ Procedure内にてイベントの引数は配列変数 EVENT_PRM[ ] に格納されている （配列はゼロから）
''',
'COM_ERR_RET': lambda dic: dic['COM_ERR_IGN'],
'COM_ERR_IGN': u'''
// COMエラーメッセージの抑止
COM_ERR_IGN
  // 何等かのCOM処理
COM_ERR_RET
 ※ COM_ERR_IGN（エラー無視）～ COM_ERR_RET（エラー認識）間でのCOMエラーメッセージを出ないようにする
   この間にエラーが起こった場合は COM_ERR_FLG に TRUE が設定される
 ※ 有効範囲はスレッド単位
''',
'SAFEARRAY': u'''
// SAFEARRAY型の作成
戻値 = SAFEARRAY( 下限, 上限, [二次元下限, 二次元上限] )
引数
 下限： 配列の下限を設定
 上限： 配列の上限を設定
 二次元下限： 二次元配列の下限を設定
 二次元上限： 二次元配列の上限を設定
戻値
 作成されたSAFEARRAY型を返す
''',
'SPEAK': u'''
// 音声合成
SPEAK( 発声文字, [平行処理フラグ, 中断フラグ] )
引数
 発声文字： 発音させたい文字列
 平行処理フラグ：
   FALSE： 発声終了まで待つ （デフォルト）
   TRUE： 終了を待たずに平行処理
 中断フラグ：
   FALSE： 発声中の音があれば終了まで待つ （デフォルト）
   TRUE： 発声中の音がある時はその音は中断する
''',
'RECOSTATE': u'''
// 音声認識 開始/停止
RECOSTATE( 開始フラグ, [単語登録, 単語登録, ...] )
引数
 開始フラグ：
   TRUE： 音声認識開始
   FALSE： 音声認識停止
 単語登録： 認識させたい単語を第２引数以降に記述 （配列変数で与える事も可）
''',
'DICTATE': u'''
// 音声の取得
戻値 = DICTATE( 拾得待ちフラグ )
引数
 拾得待ちフラグ：
   TRUE： 入力があるまで待つ （デフォルト）
   FALSE： 待たず直近の入力を返す
戻値
 拾得音声文字
''',
'IEGETDATA': u'''
// Web上(IE)より値取得
戻値 = IEGETDATA( IE, Name, [Value, 番号] )
引数
 IE： IEオブジェクト
 Name： 値取得するエレメントのName
     もしくはタグ名を記述： "TAG=タグ名"
 Value： Nameが共通の場合に Valueを指定する
     Nameにてタグ名が指定された場合は、そのタグにての順番を指定
 番号： Name, Value が同じ場合に順番指定
戻値
 取得の値 （取得できなかった場合はEMPTYを返す）
 ※ 第二引数にタグ名が指定された場合、第三引数には数字(順番)以外では "ID=xxx"、"innerHTML=xxx"、"innerText=xxx" の指定が可
 ※ TABLEの値を取得したい場合には、IEGETDATA(IE, "TAG=TABLE", Table順番, Y, X) にて取得可
''',
'IESETDATA': u'''
// Web上(IE)に値を設定
戻値 = IESETDATA( IE, 値, Name, [Value, 番号] )
引数
 IE： IEオブジェクト
 値： 設定する値
 Name： 値取得するエレメントのName
     もしくはタグ名を記述： "TAG=タグ名"
 Value： ラジオボタン等で Nameが共通の場合に Valueを指定する
     Nameにてタグ名が指定された場合は、そのタグにての順番を指定
 番号： Name, Value が同じ場合に順番指定
戻値
 TRUE：正常、 FALSE：処理不能

 ※ 第三引数にタグ名が指定された場合、第四引数には数字(順番)以外では "ID=xxx"、"innerHTML=xxx"、"innerText=xxx" の指定が可
 ※ 第三引数に"TAG=IMG"が指定された場合には、第四引数には画像のパスの指定が可
''',
'IEGETSRC': u'''
// Web上(IE)にて指定タグのソースを取得
戻値 = IEGETSRC( IE, タグ名, [番号] )
引数
 IE： IEオブジェクト
 タグ名： ソース取得するタグ名
 番号： タグの順番を指定
戻値
 取得したソース
''',
'IESETSRC': u'''
// IEにて指定タグのソースを書き換え
戻値 = IESETSRC( IE, ソース, タグ名, [番号] )
引数
 IE： IEオブジェクト
 ソース： 書き換えソース
 タグ名： タグ名を指定
 番号： タグの順番を指定
戻値
 TRUE：正常、 FALSE：処理不能
''',
'IELINK': u'''
// Web上(IE)のリンクの選択
戻値 = IELINK( IE, リンク表示文字, [番号, 完全一致フラグ] )
引数
 IE： IEオブジェクト
 リンク表示文字： 表示されているリンク項目 （一部分だけでも可）
 番号： リンク表示文字が同じ場合に順番指定
 完全一致フラグ： Trueの時は完全に一致するものだけを （デフォルト：False）
戻値
 TRUE：正常、 FALSE：処理不能
''',
'ENCODE': u'''
// 文字のエンコード処理
戻値 = ENCODE( 文字列, 変換指定 )
引数
 文字列： エンコードする文字列
 変換指定：
   CODE_URL     // URLエンコード
   CODE_UTF8     // UTF-8に
   CODE_BYTEARRAY  // バイト配列の型に（ANSI）
   CODE_BYTEARRAYW  // バイト配列の型に（UTF16）
戻値
 エンコードされた文字列
''',
'DECODE': u'''
// 文字のデコード処理
戻値 = DECODE( 文字列, 変換指定 )
引数
 文字列： デコードする文字列
 変換指定：
   CODE_URL     // URLデコード
   CODE_UTF8     // UTF-8から戻す
   CODE_BYTEARRAY  // バイト配列から戻す（ANSI）
   CODE_BYTEARRAYW  // バイト配列から戻す（UTF16）
戻値
  デコードされた文字列
''',
'CREATEFORM': u'''
// フォーム画面生成
戻値 = CREATEFORM( HTMLファイル, タイトル, [平行処理フラグ, オプション指定, 幅, 高さ, X, Y] )
引数
 HTMLファイル： フォームとして表示するHTMLファイル名
 タイトル： 表示するタイトル
 平行処理フラグ：
   FALSE： Submit属性のボタンが押されるまで処理を返さない （デフォルト）
   TRUE： 待たない
 オプション指定： (複数指定可)
   FOM_NOICON：     クローズボタンを出さない
   FOM_MINIMIZE：   最小化ボタンを表示する
   FOM_MAXIMIZE：   最大化ボタンを表示する
   FOM_NOHIDE：    Submit属性のボタンが押されても画面を消さない
   FOM_NOSUBMIT：   Submit属性のボタンが押されても Submitに割り当てられた処理をしない
   FOM_NORESIZE：   ウィンドウのサイズ変更不可
   FOM_NOLUNA：     表示をルナ(XP)風にはしない
   FOM_BROWSER：    ターゲット名解決のため、コントロールを最上位レベルのブラウザとする
 幅, 高さ： サイズ
 X, Y： 位置
戻値
 平行処理フラグ=FALSE： 押されたボタンの Name
 平行処理フラグ=TRUE：  フォームの COMオブジェクト
''',
'GETFORMDATA': u'''
// フォームより値取得
戻値 = GETFORMDATA( Name, [Value] )
引数
 Name： オブジェクトのName
 Value： Nameが共通の場合に Valueを指定する
     selectタグにて表示文字ではなく Value値を取得したい場合には FOM_GETVALUE を指定する
戻値
 取得の値
 （押されたSubmit属性のボタンが指定された場合は一度だけ TRUE(１)を返す）
''',
'SETFORMDATA': u'''
// フォームに値を設定
SETFORMDATA( 値, Name, [Value] )
引数
  値： 設定する値
  Name： オブジェクトのName
  Value： ラジオボタン等で Nameが共通の場合に Valueを指定する
''',
'XLOPEN': u'''
// Excelの起動（または OOoのCalcの起動）
戻値 = XLOPEN( [ファイル名, 起動フラグ, パラメータ, パラメータ, ...] )
引数
 ファイル名： 読み込むファイル名、 新規の場合は省略
 起動フラグ：
     0（デフォルト）  // 起動済みのExcelがある場合はそれを、なければ新規にExcelを起動
     XL_NEW, True（1） // 既にExcelが存在しても 新規にExcelを起動
     XL_BOOK      // ExcelにてBOOK単位で制御したい場合（BOOKのオブジェクトを返す）
     XL_OOOC      // OpenOffice.org / LibreOffice の表計算(Calc)の起動
 パラメータ： ファイルオープンに対し追加パラメータがある場合に（"password:=1234", "ReadOnly:= True" 等）
戻値
 ExcelのCOMオブジェクト （XL_OOOC指定時は OOoのCalc のオブジェクト)
''',
'XLCLOSE': u'''
// Excel終了
戻値 = XLCLOSE( Excel, [ファイル名] )
引数
 Excel： Excel(またはOOoのCalc)のCOMオブジェクト
 ファイル名： 保存するファイル名
        ファイル名が付いている場合は省略可
        TRUE を指定した場合は保存せずに終了
戻値
 TRUE：正常、 FALSE：処理不能
''',
'XLACTIVATE': u'''
// Excel シートのアクティブ化
戻値 = XLACTIVATE( Excel, Sheet名, [Book名] )
引数
 Excel： Excel(またはOOoのCalc)のCOMオブジェクト
 Sheet名： アクティブにするシート名（順番での指定も可）
 Book名： アクティブにするブック名
戻値
 TRUE：正常、 FALSE：処理不能
''',
'XLSHEET': u'''
// Excel シートの追加/削除
戻値 = XLSHEET( Excel, Sheet名, [削除フラグ] )
引数
 Excel： Excel(またはOOoのCalc)のCOMオブジェクト
 Sheet名： 追加/削除するシート名
 削除フラグ：
    FALSE： シート追加 （デフォルト）
    TRUE： シート削除
戻値
 TRUE：正常、 FALSE：処理不能
''',
'XLGETDATA': u'''
// Excel セルからの値の取得
戻値 = XLGETDATA( Excel, [セル範囲, Column, Sheet名] )
引数
 Excel： Excel(またはOOoのCalc)のCOMオブジェクト
 セル範囲： A1形式、もしくはR1C1形式の行を指定 （省略された場合は現在の選択セル領域）
 Column： R1C1形式時の列
 Sheet名： 指定シートから取得（指定がなければアクティブシート）
戻値
 値
 ※ 範囲指定された場合は二次元配列(SafeArray)で返される（配列の基底は1から)
''',
'XLSETDATA': u'''
// Excel セルへの値の設定
戻値 = XLSETDATA( Excel, 値, [セル位置, Column, Sheet名] )
引数
 Excel： Excel(またはOOoのCalc)のCOMオブジェクト
 値： 設定する値
 セル位置： A1形式、もしくはR1C1形式の行を指定 （省略された場合は現在の選択セル）
 Column： R1C1形式時の列
 Sheet名： 指定シートへ設定（指定がなければアクティブシート）
戻値
 TRUE：正常、 FALSE：処理不能
 ※ 配列を渡す時にRangeの大きさを指定する必要はありません（ [2,2]の配列を渡す時に"A1B2"ではなく、"A1"だけで可 ）
''',
'ABS': lambda dic: dic['RANDOM'],
'ZCUT': lambda dic: dic['RANDOM'],
'INT': lambda dic: dic['RANDOM'],
'CEIL': lambda dic: dic['RANDOM'],
'ROUND': lambda dic: dic['RANDOM'],
'SQRT': lambda dic: dic['RANDOM'],
'POWER': lambda dic: dic['RANDOM'],
'EXP': lambda dic: dic['RANDOM'],
'LN': lambda dic: dic['RANDOM'],
'LOGN': lambda dic: dic['RANDOM'],
'SIN': lambda dic: dic['RANDOM'],
'COS': lambda dic: dic['RANDOM'],
'TAN': lambda dic: dic['RANDOM'],
'ARCSIN': lambda dic: dic['RANDOM'],
'ARCCOS': lambda dic: dic['RANDOM'],
'ARCTAN': lambda dic: dic['RANDOM'],
'RANDOM': u'''
// 数学関数
 RANDOM(Range)      // 0 <=X <Range の範囲にある乱数を返す
 ABS(引数)        // 絶対値
 ZCUT(引数)       // マイナス値はゼロにする
 INT(引数)        // 少数以下切落とし
 CEIL(引数)       // 正の方向へ切り上げ
 ROUND(引数, [Digit])  // 丸め処理（Digit:丸め桁位置、負で小数点方向)
 SQRT(引数)       // 平方根
 POWER(Base, Exponent)  // 累乗（BaseのExponent乗）
 EXP(引数)        // 指数関数
 LN(引数)        // 自然対数
 LOGN(Base, X)      // Baseを底とするXの対数
 SIN(引数)        // ラジアン単位
 COS(引数)        // ラジアン単位
 TAN(引数)        // ラジアン単位
 ARCSIN(引数)      // ラジアン単位
 ARCCOS(引数)      // ラジアン単位
 ARCTAN(引数)      // ラジアン単位
 ※UWSCではゼロ割算をエラーとはせずにゼロにします
''',
'G_MOUSE_Y': lambda dic: dic['G_MOUSE_X'],
'GET_WIN_DIR': lambda dic: dic['G_MOUSE_X'],
'GET_SYS_DIR': lambda dic: dic['G_MOUSE_X'],
'GET_CUR_DIR': lambda dic: dic['G_MOUSE_X'],
'GET_APPDATA_DIR': lambda dic: dic['G_MOUSE_X'],
'GET_UWSC_DIR': lambda dic: dic['G_MOUSE_X'],
'GET_UWSC_VER': lambda dic: dic['G_MOUSE_X'],
'GET_UWSC_PRO': lambda dic: dic['G_MOUSE_X'],
'GET_UWSC_NAME': lambda dic: dic['G_MOUSE_X'],
'G_SCREEN_W': lambda dic: dic['G_MOUSE_X'],
'G_SCREEN_H': lambda dic: dic['G_MOUSE_X'],
'G_SCREEN_C': lambda dic: dic['G_MOUSE_X'],
'G_MOUSE_X': u'''
// 特殊変数
 G_MOUSE_X      // マウス位置Xを返す特殊変数
 G_MOUSE_Y      // マウス位置Yを返す特殊変数
 GET_WIN_DIR     // Windows ディレクトリ
 GET_SYS_DIR     // System ディレクトリ
 GET_CUR_DIR     // 現在のカレントディレクトリ
 GET_APPDATA_DIR   // Application Data のディレクトリ
 GET_UWSC_DIR    // UWSCのディレクトリ
 GET_UWSC_VER    // UWSCのバージョン
 GET_UWSC_PRO    // Pro版であればTrue、Free版はFalse
 GET_UWSC_NAME    // 実行中のスクリプト名
 G_SCREEN_W     // 画面幅
 G_SCREEN_H     // 画面高
 G_SCREEN_C     // 色数(１ピクセルのビット数)
'''
    }
