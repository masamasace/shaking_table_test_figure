# ライブラリのインポート
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# グラフ初期化用の関数
def setup_figure(num_row=1, num_col=1, width=6, height=6, left=0.125, right=0.9, hspace=0.2, wspace=0.2):
    fig, axes = plt.subplots(num_row, num_col, figsize=(width, height))
    fig.subplots_adjust(left=left, right=right, hspace=hspace, wspace=wspace)
    return (fig, axes)

# 必要な定数
skiprows_list = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13] # skiprowのリスト(異なる機器の場合には変更する必要あり)
plt.rcParams["font.family"] = "Times New Roman"             # グラフで使用するフォント
plt.rcParams["mathtext.fontset"] = "dejavuserif"            # グラフで使用する数式フォント
plt.rcParams['font.size'] = 14                               # グラフで使用するデフォルトのフォントサイズ
gravitational_acceleration = 981                            # 重力加速度(gal)

# 解析データのパス、グラフの作成範囲、グラフのy軸の指定
# グラフの作成範囲は[0, 0]だと全範囲、[100, 200]だと100行目から199行目を抜き出す
# グラフのy軸の設定は[0, 0]だと自動設定。[-100, 100]だと最小値が-100で最大値が100になる。                                                                                        DT      LS     Acc      PW
data = [[r"E:\Shiga Dropbox\01_work\04_2021-_assistant professor\14_to others\15_ito\02_shaking table test\20220310\06_numeric record\20220310_experiment0004.CSV", [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        [r"E:\Shiga Dropbox\01_work\04_2021-_assistant professor\14_to others\15_ito\02_shaking table test\20220310\06_numeric record\20220310_experiment0005.CSV", [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]]


# forループ(dataの中の一つ一つについて以下の処理を行う)
for data_temp in data:
    data_path = Path(data_temp[0])
    data_range = data_temp[1]
    data_dt_ylim = data_temp[2]
    data_ls_ylim = data_temp[3]
    data_acc_ylim = data_temp[3]
    data_pore_ylim = data_temp[4]
    
    # 結果保存フォルダの作成
    result_dir_path_fig = data_path.parent / "res" / data_path.stem
    if result_dir_path_fig.exists():
        for p in result_dir_path_fig.iterdir():
            if p.is_file():
                p.unlink()
    else:
        result_dir_path_fig.mkdir()
    
    # データの読み込み
    data_csv = pd.read_csv(data_path, skiprows=skiprows_list, header=0, encoding='Shift_JIS')
    data_csv.rename(columns={"CH名称":"Time"}, inplace=True)
    
    # データの抜き出し
    if data_range != [0, 0] and data_range[0] < data_range[1]:
        data_csv = data_csv.iloc[data_range[0]:data_range[1], :]
    
    # グラフの描画のforループ(data_csvの各列に対して以下の処理を行う)
    for col_name in data_csv.columns[1:]:

        # 描画の準備とプロットの挿入
        fig, axes = setup_figure()
        axes.plot(data_csv["Time"], data_csv[col_name] * gravitational_acceleration, linewidth=0.5, color="k")
        
        # ラベルの設定(上は影用)
        label_col_name = textwrap.fill(col_name, 15) 
        label_loc = [0.05, 0.85]
        axes.text(label_loc[0] + 0.01, label_loc[1] - 0.01, label_col_name, fontsize=14, transform=axes.transAxes, bbox=dict(facecolor='k', edgecolor='k', linewidth=0.5, boxstyle="round", pad=0.5))
        axes.text(label_loc[0], label_loc[1], label_col_name, fontsize=14, transform=axes.transAxes, bbox=dict(facecolor='w', edgecolor='k', linewidth=0.5, boxstyle="round", pad=0.5))
        
        # y軸の範囲の決定
        if col_name[:2] == "DT":   
            if data_dt_ylim != [0, 0] and data_dt_ylim[0] < data_dt_ylim[1]:
                axes.set_ylim(data_dt_ylim)
        elif col_name[:2] == "LS":
            if data_ls_ylim != [0, 0] and data_ls_ylim[0] < data_ls_ylim[1]:
                axes.set_ylim(data_ls_ylim) 
        elif col_name[0] == "A":
            if data_acc_ylim != [0, 0] and data_acc_ylim[0] < data_acc_ylim[1]:
                axes.set_ylim(data_acc_ylim)   
        elif col_name[:2] == "PW":
            if data_pore_ylim != [0, 0] and data_pore_ylim[0] < data_pore_ylim[1]:
                axes.set_ylim(data_pore_ylim)   
        
        # 個別にy軸の範囲を設定したかったら次のコードのコメントアウトを外してね
        """
        if col_name == "A1 On the Shaking table":
            axes.set_ylim([-100, 100])
        """
        
        # 画像の保存
        figure_path = result_dir_path_fig / (col_name + ".jpeg")
        fig.savefig(figure_path, format="jpeg", dpi=600, bbox_inches='tight')
        plt.clf()
        plt.close()
        