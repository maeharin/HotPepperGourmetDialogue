# -*- coding: utf-8 -*-
from modules.LanguageUnderstanding.DialogueActType.predictor import DialogueActTypePredictor, sent2features_
from modules.LanguageUnderstanding.NamedEntityExtraction.extractor import NamedEntityExtractor
from modules.LanguageUnderstanding.utils.utils import sent2features
from training_data_generator.scripts.analyzer import analyze_morph


class LanguageUnderstanding(object):

    def __init__(self):
        self.__predictor = DialogueActTypePredictor()
        self.__extractor = NamedEntityExtractor()

    def execute(self, sent):
        # 対話行為タイプの推定開始
        # 4タイプ
        # - genre: イタリアンとか
        # - location: 新宿とか
        # - money: 1万円とか
        # - other: その他
        features = sent2features_(sent)
        #print("送信されたテキストから変換したfeatures:", features)
        act_type = self.__predictor.predict([features])
        print("featureから予測したact_type:", act_type)
        # 対話行為タイプの推定完了

        # 属性抽出
        # ジャンルに対して文字を抽出。イタリアンとか中華とか

        surfaces, features = analyze_morph(sent)
        print("surfaces:", surfaces)
        print("features:", features)
        morphed_sent = [[surfaces[i]] + features[i].split(',') for i in range(len(surfaces))]
        print("morphed_sent", morphed_sent)
        features = sent2features(morphed_sent)
        named_entity = self.__extractor.extract(features, morphed_sent)

        dialogue_act = {'user_act_type': act_type}
        # ここで属性を追加
        dialogue_act.update(dict(named_entity))

        return dialogue_act


if __name__ == '__main__':
    sent = 'ラーメンを食べたい'
    language_understanding = LanguageUnderstanding()
    language_understanding.execute(sent)
    sent = '西新宿'
    language_understanding.execute(sent)
    sent = '新宿近辺'
    language_understanding.execute(sent)