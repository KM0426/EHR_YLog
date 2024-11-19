import sys
import datetime
import numpy as np
import tkinter.messagebox as messagebox
from models import ReadCSV, FileDIalog, CountTime
from models.YCodeBranch import branchYCode

def file_select(message, label, allow_multiple):
    """ファイル選択ダイアログを表示してファイルを選択"""
    print(message)
    return FileDIalog.OpenFileDialog(label, allow_multiple)

def read_csv_file(file_path):
    """CSVファイルを読み込む"""
    return ReadCSV.ReadCSV(file_path)

def parse_log_datetime(log_datetime_str):
    """ログの日付文字列をdatetime型に変換"""
    try:
        return datetime.datetime.strptime(log_datetime_str, '%Y/%m/%d %H:%M')
    except ValueError as e:
        message = f"Invalid datetime format: {e}"
        print(message)
        messagebox.showerror("Error", message)
        raise

def create_terminal_dictionaries(terminals_list):
    """端末リストから辞書を作成"""
    terminal_place_dic = {terminal[0]: terminal[1] for terminal in terminals_list}
    terminal_dic = {terminal[0]: [] for terminal in terminals_list}
    return terminal_place_dic, terminal_dic

def process_logs(ylog_list, terminal_dic, terminal_place_dic):
    """ログデータを処理して辞書に格納"""
    for log in ylog_list:
        terminal_id = log[7]
        log_datetime = parse_log_datetime(log[0])

        if terminal_id not in terminal_dic:
            terminal_dic[terminal_id] = []
            terminal_place_dic[terminal_id] = "空白"

        terminal_dic[terminal_id].append([log_datetime, branchYCode(log[8])])

def analyze_data(terminal_dic, terminal_place_dic):
    """データを解析して集計結果を作成"""
    calc_counts = [['端末番号', '名称'] + [f"{hour}時" for hour in range(24)]]

    for terminal_id, logs in terminal_dic.items():
        if not logs:
            continue

        base_count_time = CountTime.CountDic(terminal_id)
        base_count_time.timeTable[1] = terminal_place_dic[terminal_id]
        list_count_time = []
        is_logged_in = False
        current_datetime = logs[0][0]

        count_time = CountTime.CountDic(terminal_id)

        for log_datetime, log_type in logs:
            if is_logged_in:
                while current_datetime <= log_datetime:
                    count_time.timeTable[current_datetime.hour + 2] = 1
                    current_datetime += datetime.timedelta(hours=1)

            if log_type in {'IN', 'ScreenOFF'}:
                is_logged_in = True
                count_time.timeTable[log_datetime.hour + 2] = 1
            elif log_type in {'OUT', 'ScreenON'}:
                is_logged_in = False
                count_time.timeTable[log_datetime.hour + 2] = 1

            current_datetime = log_datetime

        list_count_time.append(count_time.timeTable)

        for daily_count in list_count_time:
            for hour in range(2, 26):
                base_count_time.timeTable[hour] += daily_count[hour]

        calc_counts.append(base_count_time.timeTable)

    return calc_counts

def save_to_csv(file_name, data):
    """データをCSVファイルに保存"""
    with open(file_name, "w", encoding="utf-8-sig", newline="") as f:
        np.savetxt(f, data, delimiter=",", fmt='%s')

def main():
    """メイン処理"""
    terminal_file_name = file_select(
        "ファイル選択ダイアログでファイルを選択してください...（瞬快の端末一覧を選択）",
        "瞬快の端末一覧を選択(アクセスログ【yyyymmdd】)",
        True
    )
    if not terminal_file_name:
        sys.exit()

    ylog_file_name = file_select(
        "ファイル選択ダイアログでファイルを選択してください...（クエリ(Y全て)_yyyymmdd-mmdd）",
        "クエリ(Y全て)_yyyymmdd-mmdd",
        False
    )
    if not ylog_file_name:
        sys.exit()

    print("ファイルを読み込んでいます...")
    terminals_list = read_csv_file(terminal_file_name)
    ylog_list = read_csv_file(ylog_file_name)

    print("データを辞書に加工中...")
    terminal_place_dic, terminal_dic = create_terminal_dictionaries(terminals_list)

    try:
        process_logs(ylog_list, terminal_dic, terminal_place_dic)
    except Exception:
        sys.exit()

    print("データを解析・集計中...")
    calc_counts = analyze_data(terminal_dic, terminal_place_dic)

    print("結果をファイルに書き出しています...")
    save_to_csv("outnp.csv", calc_counts)

    print("完了しました！")
    input("エンターを入力するか、コンソールを閉じて終了してください")

if __name__ == "__main__":
    main()
