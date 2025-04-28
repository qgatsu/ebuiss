import pandas as pd

class DataHandler:
    def __init__(self, factor_df: pd.DataFrame):
        """
        Parameters:
            factor_df: MultiIndex(index=["date", "ticker"]), columns=[各ファクター名]
        """
        self.factor_df = factor_df.copy()
        self.factor_names = list(factor_df.columns)

    def get_columnlist(self):
        """使用可能なファクター名一覧"""
        return self.factor_names

    def get(self, date, factor_name):
        """指定日・ファクターのスコアを Series (index=ticker) で取得"""
        return self.factor_df.loc[date, factor_name]

    def get_panel(self, date):
        """指定日の全ファクターを DataFrame(index=ticker, columns=factor) で取得"""
        return self.factor_df.loc[date]

    def get_wide_data(self, factor_name):
        """Backtester 用：wide形式 (index=date, columns=ticker) に変換して返す"""
        return self.factor_df[factor_name].unstack()

    def describe(self, factor_name):
        """ファクターの統計情報を返す"""
        return self.factor_df[factor_name].describe()

    def rank(self, date, factor_name, ascending=True):
        """指定日・ファクターのランク（昇順 or 降順）"""
        return self.get(date, factor_name).rank(ascending=ascending)
    
    def shift(self, shift=1, columns=None):
        """
        指定ファクター列を ticker ごとに groupby して shift した列を追加する。

        Parameters:
            shift (int): シフト量（正の整数）
            columns (list or None): 対象とするファクター列。None の場合は全列。
        """
        columns = columns or self.factor_names

        for col in columns:
            shifted = (
                self.factor_df[col]
                .groupby(level="ticker")
                .shift(shift)
                .rename(f"{col}_lag{shift}")
            )
            self.factor_df[f"{col}_lag{shift}"] = shifted
            # ファクター名一覧も更新
            self.factor_names.append(f"{col}_lag{shift}")

